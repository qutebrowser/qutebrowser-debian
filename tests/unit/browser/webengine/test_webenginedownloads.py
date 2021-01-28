# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# Copyright 2016-2021 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <https://www.gnu.org/licenses/>.

import os.path
import base64

import pytest
pytest.importorskip('PyQt5.QtWebEngineWidgets')
from PyQt5.QtWebEngineWidgets import QWebEngineProfile

from qutebrowser.utils import urlutils, usertypes
from qutebrowser.browser.webengine import webenginedownloads


@pytest.mark.parametrize('path, expected', [
    ('foo(1)', 'foo'),
    ('foo (1)', 'foo'),
    ('foo - 1970-01-01T00:00:00.000Z', 'foo'),
    ('foo(a)', 'foo(a)'),
    ('foo1', 'foo1'),
    ('foo%20bar', 'foo%20bar'),
    ('foo%2Fbar', 'foo%2Fbar'),
])
def test_strip_suffix(path, expected):
    assert webenginedownloads._strip_suffix(path) == expected


class TestDataUrlWorkaround:

    """With data URLs, we get rather weird base64 filenames back from QtWebEngine.

    See https://bugreports.qt.io/browse/QTBUG-90355
    """

    @pytest.fixture(params=[True, False])
    def pdf_bytes(self, request):
        with_slash = request.param

        # https://stackoverflow.com/a/17280876/2085149
        pdf_source = [
            '%PDF-1.0',
            '1 0 obj<</Pages 2 0 R>>endobj',
            '2 0 obj<</Kids[3 0 R]/Count 1>>endobj',
            '3 0 obj<</MediaBox[0 0 3 3]>>endobj',
            'trailer<</Root 1 0 R>>',
        ]

        if with_slash:
            pdf_source.insert(1, '% ?')  # this results in a slash in base64

        return '\n'.join(pdf_source).encode('ascii')

    @pytest.fixture
    def pdf_url(self, pdf_bytes):
        return urlutils.data_url('application/pdf', pdf_bytes)

    @pytest.fixture
    def webengine_profile(self, qapp):
        profile = QWebEngineProfile.defaultProfile()
        profile.setParent(qapp)
        return profile

    @pytest.fixture
    def download_manager(self, qapp, qtbot, webengine_profile, download_tmpdir,
                         config_stub):
        config_stub.val.downloads.location.suggestion = 'filename'
        manager = webenginedownloads.DownloadManager(parent=qapp)
        manager.install(webengine_profile)
        yield manager
        webengine_profile.downloadRequested.disconnect()

    def test_workaround(self, webengine_tab, message_mock, qtbot,
                        pdf_url, download_manager):
        """Verify our workaround works properly."""
        with qtbot.waitSignal(message_mock.got_question):
            webengine_tab.load_url(pdf_url)

        question = message_mock.get_question()
        assert question.default == 'download.pdf'

    def test_explicit_filename(self, webengine_tab, message_mock, qtbot,
                               pdf_url, download_manager):
        """If a website sets an explicit filename, we should respect that."""
        pdf_url_str = pdf_url.toDisplayString()
        html = f'<a href="{pdf_url_str}" download="filename.pdf" id="link">'

        with qtbot.waitSignal(webengine_tab.load_finished):
            webengine_tab.set_html(html)

        with qtbot.waitSignal(message_mock.got_question):
            webengine_tab.elements.find_id(
                "link",
                lambda elem: elem.click(usertypes.ClickTarget.normal),
            )

        question = message_mock.get_question()
        assert question.default == 'filename.pdf'

    @pytest.fixture
    def expected_wrong_filename(self, pdf_bytes):
        with_slash = b'% ?' in pdf_bytes
        base64_data = base64.b64encode(pdf_bytes).decode('ascii')

        if with_slash:
            assert '/' in base64_data
            return base64_data.split('/')[1]
        else:
            assert '/' not in base64_data
            return 'pdf'  # from the mimetype

    def test_workaround_needed(self, qtbot, webengineview,
                               pdf_url, expected_wrong_filename, webengine_profile):
        """Verify that our workaround for this is still needed.

        In other words, check whether we get those base64-filenames rather than a
        "download.pdf" like with Chromium.
        """
        def check_item(item):
            assert item.mimeType() == 'application/pdf'
            assert item.url().scheme() == 'data'
            assert os.path.basename(item.path()) == expected_wrong_filename
            return True

        with qtbot.waitSignal(webengine_profile.downloadRequested,
                              check_params_cb=check_item):
            webengineview.load(pdf_url)
