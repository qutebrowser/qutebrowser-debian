# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:
# Copyright 2017-2021 Florian Bruhin (The Compiler) <mail@qutebrowser.org>

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

import sys
import os
import logging

import pytest

from qutebrowser import qutebrowser
from qutebrowser.config import qtargs
from qutebrowser.utils import usertypes
from helpers import utils


class TestQtArgs:

    @pytest.fixture
    def parser(self, mocker):
        """Fixture to provide an argparser.

        Monkey-patches .exit() of the argparser so it doesn't exit on errors.
        """
        parser = qutebrowser.get_argparser()
        mocker.patch.object(parser, 'exit', side_effect=Exception)
        return parser

    @pytest.fixture(autouse=True)
    def reduce_args(self, monkeypatch, config_stub):
        """Make sure no --disable-shared-workers/referer argument get added."""
        monkeypatch.setattr(qtargs.qtutils, 'qVersion', lambda: '5.15.0')
        config_stub.val.content.headers.referer = 'always'

    @pytest.mark.parametrize('args, expected', [
        # No Qt arguments
        (['--debug'], [sys.argv[0]]),
        # Qt flag
        (['--debug', '--qt-flag', 'reverse'], [sys.argv[0], '--reverse']),
        # Qt argument with value
        (['--qt-arg', 'stylesheet', 'foo'],
         [sys.argv[0], '--stylesheet', 'foo']),
        # --qt-arg given twice
        (['--qt-arg', 'stylesheet', 'foo', '--qt-arg', 'geometry', 'bar'],
         [sys.argv[0], '--stylesheet', 'foo', '--geometry', 'bar']),
        # --qt-flag given twice
        (['--qt-flag', 'foo', '--qt-flag', 'bar'],
         [sys.argv[0], '--foo', '--bar']),
    ])
    def test_qt_args(self, monkeypatch, config_stub, args, expected, parser):
        """Test commandline with no Qt arguments given."""
        # Avoid scrollbar overlay argument
        config_stub.val.scrolling.bar = 'never'
        # Avoid WebRTC pipewire feature
        monkeypatch.setattr(qtargs.utils, 'is_linux', False)

        parsed = parser.parse_args(args)
        assert qtargs.qt_args(parsed) == expected

    def test_qt_both(self, config_stub, parser):
        """Test commandline with a Qt argument and flag."""
        args = parser.parse_args(['--qt-arg', 'stylesheet', 'foobar',
                                  '--qt-flag', 'reverse'])
        qt_args = qtargs.qt_args(args)
        assert qt_args[0] == sys.argv[0]
        assert '--reverse' in qt_args
        assert '--stylesheet' in qt_args
        assert 'foobar' in qt_args

    def test_with_settings(self, config_stub, parser):
        parsed = parser.parse_args(['--qt-flag', 'foo'])
        config_stub.val.qt.args = ['bar']
        args = qtargs.qt_args(parsed)
        assert args[0] == sys.argv[0]
        for arg in ['--foo', '--bar']:
            assert arg in args

    @pytest.mark.parametrize('backend, expected', [
        (usertypes.Backend.QtWebEngine, True),
        (usertypes.Backend.QtWebKit, False),
    ])
    def test_shared_workers(self, config_stub, monkeypatch, parser,
                            backend, expected):
        monkeypatch.setattr(qtargs.qtutils, 'qVersion', lambda: '5.14.0')
        monkeypatch.setattr(qtargs.objects, 'backend', backend)
        parsed = parser.parse_args([])
        args = qtargs.qt_args(parsed)
        assert ('--disable-shared-workers' in args) == expected

    @pytest.mark.parametrize('backend, version_check, debug_flag, expected', [
        # Qt >= 5.12.3: Enable with -D stack, do nothing without it.
        (usertypes.Backend.QtWebEngine, True, True, True),
        (usertypes.Backend.QtWebEngine, True, False, None),
        # Qt < 5.12.3: Do nothing with -D stack, disable without it.
        (usertypes.Backend.QtWebEngine, False, True, None),
        (usertypes.Backend.QtWebEngine, False, False, False),
        # QtWebKit: Do nothing
        (usertypes.Backend.QtWebKit, True, True, None),
        (usertypes.Backend.QtWebKit, True, False, None),
        (usertypes.Backend.QtWebKit, False, True, None),
        (usertypes.Backend.QtWebKit, False, False, None),
    ])
    def test_in_process_stack_traces(self, monkeypatch, parser, backend,
                                     version_check, debug_flag, expected):
        monkeypatch.setattr(qtargs.qtutils, 'version_check',
                            lambda version, compiled=False, exact=False: version_check)
        monkeypatch.setattr(qtargs.objects, 'backend', backend)
        parsed = parser.parse_args(['--debug-flag', 'stack'] if debug_flag
                                   else [])
        args = qtargs.qt_args(parsed)

        if expected is None:
            assert '--disable-in-process-stack-traces' not in args
            assert '--enable-in-process-stack-traces' not in args
        elif expected:
            assert '--disable-in-process-stack-traces' not in args
            assert '--enable-in-process-stack-traces' in args
        else:
            assert '--disable-in-process-stack-traces' in args
            assert '--enable-in-process-stack-traces' not in args

    @pytest.mark.parametrize('flags, args', [
        ([], []),
        (['--debug-flag', 'chromium'], ['--enable-logging', '--v=1']),
        (['--debug-flag', 'wait-renderer-process'], ['--renderer-startup-dialog']),
    ])
    def test_chromium_flags(self, monkeypatch, parser, flags, args):
        monkeypatch.setattr(qtargs.objects, 'backend',
                            usertypes.Backend.QtWebEngine)
        parsed = parser.parse_args(flags)
        args = qtargs.qt_args(parsed)

        if args:
            for arg in args:
                assert arg in args
        else:
            assert '--enable-logging' not in args
            assert '--v=1' not in args
            assert '--renderer-startup-dialog' not in args

    @pytest.mark.parametrize('config, added', [
        ('none', False),
        ('qt-quick', False),
        ('software-opengl', False),
        ('chromium', True),
    ])
    def test_disable_gpu(self, config, added,
                         config_stub, monkeypatch, parser):
        monkeypatch.setattr(qtargs.objects, 'backend',
                            usertypes.Backend.QtWebEngine)
        config_stub.val.qt.force_software_rendering = config
        parsed = parser.parse_args([])
        args = qtargs.qt_args(parsed)
        assert ('--disable-gpu' in args) == added

    @pytest.mark.parametrize('policy, arg', [
        ('all-interfaces', None),

        ('default-public-and-private-interfaces',
         '--force-webrtc-ip-handling-policy='
         'default_public_and_private_interfaces'),

        ('default-public-interface-only',
         '--force-webrtc-ip-handling-policy='
         'default_public_interface_only'),

        ('disable-non-proxied-udp',
         '--force-webrtc-ip-handling-policy='
         'disable_non_proxied_udp'),
    ])
    def test_webrtc(self, config_stub, monkeypatch, parser,
                    policy, arg):
        monkeypatch.setattr(qtargs.objects, 'backend',
                            usertypes.Backend.QtWebEngine)
        config_stub.val.content.webrtc_ip_handling_policy = policy

        parsed = parser.parse_args([])
        args = qtargs.qt_args(parsed)

        if arg is None:
            assert not any(a.startswith('--force-webrtc-ip-handling-policy=')
                           for a in args)
        else:
            assert arg in args

    @pytest.mark.parametrize('canvas_reading, added', [
        (True, False),  # canvas reading enabled
        (False, True),
    ])
    def test_canvas_reading(self, config_stub, monkeypatch, parser,
                            canvas_reading, added):
        monkeypatch.setattr(qtargs.objects, 'backend',
                            usertypes.Backend.QtWebEngine)

        config_stub.val.content.canvas_reading = canvas_reading
        parsed = parser.parse_args([])
        args = qtargs.qt_args(parsed)
        assert ('--disable-reading-from-canvas' in args) == added

    @pytest.mark.parametrize('process_model, added', [
        ('process-per-site-instance', False),
        ('process-per-site', True),
        ('single-process', True),
    ])
    def test_process_model(self, config_stub, monkeypatch, parser,
                           process_model, added):
        monkeypatch.setattr(qtargs.objects, 'backend',
                            usertypes.Backend.QtWebEngine)

        config_stub.val.qt.process_model = process_model
        parsed = parser.parse_args([])
        args = qtargs.qt_args(parsed)

        if added:
            assert '--' + process_model in args
        else:
            assert '--process-per-site' not in args
            assert '--single-process' not in args
            assert '--process-per-site-instance' not in args
            assert '--process-per-tab' not in args

    @pytest.mark.parametrize('low_end_device_mode, arg', [
        ('auto', None),
        ('always', '--enable-low-end-device-mode'),
        ('never', '--disable-low-end-device-mode'),
    ])
    def test_low_end_device_mode(self, config_stub, monkeypatch, parser,
                                 low_end_device_mode, arg):
        monkeypatch.setattr(qtargs.objects, 'backend',
                            usertypes.Backend.QtWebEngine)

        config_stub.val.qt.low_end_device_mode = low_end_device_mode
        parsed = parser.parse_args([])
        args = qtargs.qt_args(parsed)

        if arg is None:
            assert '--enable-low-end-device-mode' not in args
            assert '--disable-low-end-device-mode' not in args
        else:
            assert arg in args

    @pytest.mark.parametrize('qt_version, referer, arg', [
        # 'always' -> no arguments
        ('5.15.0', 'always', None),

        # 'never' is handled via interceptor for most Qt versions
        ('5.12.3', 'never', '--no-referrers'),
        ('5.12.4', 'never', None),
        ('5.13.0', 'never', '--no-referrers'),
        ('5.13.1', 'never', None),
        ('5.14.0', 'never', None),
        ('5.15.0', 'never', None),

        # 'same-domain' - arguments depend on Qt versions
        ('5.13.0', 'same-domain', '--reduced-referrer-granularity'),
        ('5.14.0', 'same-domain', '--enable-features=ReducedReferrerGranularity'),
        ('5.15.0', 'same-domain', '--enable-features=ReducedReferrerGranularity'),
    ])
    def test_referer(self, config_stub, monkeypatch, parser, qt_version, referer, arg):
        monkeypatch.setattr(qtargs.objects, 'backend', usertypes.Backend.QtWebEngine)
        monkeypatch.setattr(qtargs.qtutils, 'qVersion', lambda: qt_version)

        # Avoid WebRTC pipewire feature
        monkeypatch.setattr(qtargs.utils, 'is_linux', False)
        # Avoid overlay scrollbar feature
        config_stub.val.scrolling.bar = 'never'

        config_stub.val.content.headers.referer = referer
        parsed = parser.parse_args([])
        args = qtargs.qt_args(parsed)

        if arg is None:
            assert '--no-referrers' not in args
            assert '--reduced-referrer-granularity' not in args
            assert '--enable-features=ReducedReferrerGranularity' not in args
        else:
            assert arg in args

    @pytest.mark.parametrize('dark, qt_version, added', [
        (True, "5.13", False),  # not supported
        (True, "5.14", True),
        (True, "5.15.0", True),
        (True, "5.15.1", True),
        (True, "5.15.2", False),  # handled via blink setting

        (False, "5.13", False),
        (False, "5.14", False),
        (False, "5.15.0", False),
        (False, "5.15.1", False),
        (False, "5.15.2", False),
    ])
    @utils.qt514
    def test_prefers_color_scheme_dark(self, config_stub, monkeypatch, parser,
                                       dark, qt_version, added):
        monkeypatch.setattr(qtargs.objects, 'backend',
                            usertypes.Backend.QtWebEngine)
        monkeypatch.setattr(qtargs.qtutils, 'qVersion', lambda: qt_version)

        config_stub.val.colors.webpage.prefers_color_scheme_dark = dark

        parsed = parser.parse_args([])
        args = qtargs.qt_args(parsed)

        assert ('--force-dark-mode' in args) == added

    @pytest.mark.parametrize('bar, is_mac, added', [
        # Overlay bar enabled
        ('overlay', False, True),
        # No overlay on mac
        ('overlay', True, False),
        # Overlay disabled
        ('when-searching', False, False),
        ('always', False, False),
        ('never', False, False),
    ])
    def test_overlay_scrollbar(self, config_stub, monkeypatch, parser,
                               bar, is_mac, added):
        monkeypatch.setattr(qtargs.objects, 'backend',
                            usertypes.Backend.QtWebEngine)
        monkeypatch.setattr(qtargs.utils, 'is_mac', is_mac)
        # Avoid WebRTC pipewire feature
        monkeypatch.setattr(qtargs.utils, 'is_linux', False)

        config_stub.val.scrolling.bar = bar

        parsed = parser.parse_args([])
        args = qtargs.qt_args(parsed)

        assert ('--enable-features=OverlayScrollbar' in args) == added

    @pytest.fixture
    def feature_flag_patch(self, monkeypatch):
        """Patch away things affecting feature flags."""
        monkeypatch.setattr(qtargs.objects, 'backend',
                            usertypes.Backend.QtWebEngine)
        monkeypatch.setattr(qtargs.qtutils, 'version_check',
                            lambda version, exact=False, compiled=True:
                            True)
        monkeypatch.setattr(qtargs.utils, 'is_mac', False)
        # Avoid WebRTC pipewire feature
        monkeypatch.setattr(qtargs.utils, 'is_linux', False)

    @pytest.mark.parametrize('via_commandline', [True, False])
    @pytest.mark.parametrize('overlay, passed_features, expected_features', [
        (True,
         'CustomFeature',
         'CustomFeature,OverlayScrollbar'),
        (True,
         'CustomFeature1,CustomFeature2',
         'CustomFeature1,CustomFeature2,OverlayScrollbar'),
        (False,
         'CustomFeature',
         'CustomFeature'),
    ])
    def test_overlay_features_flag(self, config_stub, parser, feature_flag_patch,
                                   via_commandline, overlay, passed_features,
                                   expected_features):
        """If enable-features is already specified, we should combine both."""
        config_flag = qtargs._ENABLE_FEATURES.lstrip('-') + passed_features

        config_stub.val.scrolling.bar = 'overlay' if overlay else 'never'
        config_stub.val.qt.args = ([] if via_commandline else [config_flag])

        parsed = parser.parse_args(['--qt-flag', config_flag]
                                   if via_commandline else [])
        args = qtargs.qt_args(parsed)

        overlay_flag = qtargs._ENABLE_FEATURES + 'OverlayScrollbar'
        combined_flag = qtargs._ENABLE_FEATURES + expected_features

        enable_features_args = [
            arg for arg in args
            if arg.startswith(qtargs._ENABLE_FEATURES)
        ]
        assert len(enable_features_args) == 1
        assert combined_flag in args
        assert overlay_flag not in args

    @pytest.mark.parametrize('via_commandline', [True, False])
    @pytest.mark.parametrize('passed_features', [
        ['CustomFeature'],
        ['CustomFeature1', 'CustomFeature2'],
    ])
    def test_disable_features_passthrough(self, config_stub, parser, feature_flag_patch,
                                          via_commandline, passed_features):
        flag = qtargs._DISABLE_FEATURES + ','.join(passed_features)

        config_flag = flag.lstrip('-')
        config_stub.val.qt.args = ([] if via_commandline else [config_flag])
        parsed = parser.parse_args(['--qt-flag', config_flag]
                                   if via_commandline else [])
        args = qtargs.qt_args(parsed)

        disable_features_args = [
            arg for arg in args
            if arg.startswith(qtargs._DISABLE_FEATURES)
        ]
        assert len(disable_features_args) == 1
        features = set(disable_features_args[0].split('=')[1].split(','))
        features -= {'InstalledApp'}
        assert features == set(passed_features)

    @pytest.mark.parametrize('qt_version, has_workaround', [
        ('5.14.0', False),
        ('5.15.1', False),
        ('5.15.2', True),
        ('5.15.3', False),
        ('6.0.0', False),
    ])
    def test_installedapp_workaround(self, parser, monkeypatch, qt_version, has_workaround):
        monkeypatch.setattr(qtargs.qtutils, 'qVersion', lambda: qt_version)
        monkeypatch.setattr(qtargs.objects, 'backend',
                            usertypes.Backend.QtWebEngine)

        parsed = parser.parse_args([])
        args = qtargs.qt_args(parsed)
        disable_features_args = [
            arg for arg in args
            if arg.startswith(qtargs._DISABLE_FEATURES)
        ]

        expected = ['--disable-features=InstalledApp'] if has_workaround else []
        assert disable_features_args == expected

    def test_blink_settings(self, config_stub, monkeypatch, parser):
        from qutebrowser.browser.webengine import darkmode
        monkeypatch.setattr(qtargs.objects, 'backend',
                            usertypes.Backend.QtWebEngine)
        monkeypatch.setattr(darkmode, '_variant',
                            lambda: darkmode.Variant.qt_515_2)

        config_stub.val.colors.webpage.darkmode.enabled = True

        parsed = parser.parse_args([])
        args = qtargs.qt_args(parsed)

        expected = ('--blink-settings=forceDarkModeEnabled=true,'
                    'forceDarkModeImagePolicy=2')

        assert expected in args


class TestEnvVars:

    @pytest.mark.parametrize('config_opt, config_val, envvar, expected', [
        ('qt.force_software_rendering', 'software-opengl',
         'QT_XCB_FORCE_SOFTWARE_OPENGL', '1'),
        ('qt.force_software_rendering', 'qt-quick',
         'QT_QUICK_BACKEND', 'software'),
        ('qt.force_software_rendering', 'chromium',
         'QT_WEBENGINE_DISABLE_NOUVEAU_WORKAROUND', '1'),
        ('qt.force_platform', 'toaster', 'QT_QPA_PLATFORM', 'toaster'),
        ('qt.force_platformtheme', 'lxde', 'QT_QPA_PLATFORMTHEME', 'lxde'),
        ('window.hide_decoration', True,
         'QT_WAYLAND_DISABLE_WINDOWDECORATION', '1')
    ])
    def test_env_vars(self, monkeypatch, config_stub,
                      config_opt, config_val, envvar, expected):
        """Check settings which set an environment variable."""
        monkeypatch.setattr(qtargs.objects, 'backend',
                            usertypes.Backend.QtWebEngine)
        monkeypatch.setenv(envvar, '')  # to make sure it gets restored
        monkeypatch.delenv(envvar)

        config_stub.set_obj(config_opt, config_val)
        qtargs.init_envvars()

        assert os.environ[envvar] == expected

    @pytest.mark.parametrize('init_val, config_val', [
        (   # Test changing a set variable
            {'QT_SCALE_FACTOR': '2'},
            {'QT_SCALE_FACTOR': '4'},
        ),
        (   # Test setting an unset variable
            {'QT_SCALE_FACTOR': None},
            {'QT_SCALE_FACTOR': '3'},
        ),
        (   # Test unsetting a variable which is set
            {'QT_SCALE_FACTOR': '3'},
            {'QT_SCALE_FACTOR': None},
        ),
        (   # Test unsetting a variable which is unset
            {'QT_SCALE_FACTOR': None},
            {'QT_SCALE_FACTOR': None},
        ),
        (   # Test setting multiple variables
            {'QT_SCALE_FACTOR': '0', 'QT_PLUGIN_PATH': '/usr/bin', 'QT_NEWVAR': None},
            {'QT_SCALE_FACTOR': '3', 'QT_PLUGIN_PATH': '/tmp/', 'QT_NEWVAR': 'newval'},
        )
    ])
    def test_environ_settings(self, monkeypatch, config_stub,
                              init_val, config_val):
        """Test setting environment variables using qt.environ."""
        for var, val in init_val.items():
            if val is None:
                monkeypatch.setenv(var, '0')
                monkeypatch.delenv(var, raising=False)
            else:
                monkeypatch.setenv(var, val)

        config_stub.val.qt.environ = config_val
        qtargs.init_envvars()

        for var, result in config_val.items():
            if result is None:
                assert var not in os.environ
            else:
                assert os.environ[var] == result

    @pytest.mark.parametrize('new_qt', [True, False])
    def test_highdpi(self, monkeypatch, config_stub, new_qt):
        """Test HighDPI environment variables.

        Depending on the Qt version, there's a different variable which should
        be set...
        """
        new_var = 'QT_ENABLE_HIGHDPI_SCALING'
        old_var = 'QT_AUTO_SCREEN_SCALE_FACTOR'

        monkeypatch.setattr(qtargs.objects, 'backend',
                            usertypes.Backend.QtWebEngine)
        monkeypatch.setattr(qtargs.qtutils, 'version_check',
                            lambda version, exact=False, compiled=True:
                            new_qt)

        for envvar in [new_var, old_var]:
            monkeypatch.setenv(envvar, '')  # to make sure it gets restored
            monkeypatch.delenv(envvar)

        config_stub.set_obj('qt.highdpi', True)
        qtargs.init_envvars()

        envvar = new_var if new_qt else old_var

        assert os.environ[envvar] == '1'

    def test_env_vars_webkit(self, monkeypatch, config_stub):
        monkeypatch.setattr(qtargs.objects, 'backend',
                            usertypes.Backend.QtWebKit)
        qtargs.init_envvars()

    @pytest.mark.parametrize('backend, value, expected', [
        (usertypes.Backend.QtWebKit, None, None),
        (usertypes.Backend.QtWebKit, '--test', None),

        (usertypes.Backend.QtWebEngine, None, None),
        (usertypes.Backend.QtWebEngine, '', "''"),
        (usertypes.Backend.QtWebEngine, '--xyz', "'--xyz'"),
    ])
    def test_qtwe_flags_warning(self, monkeypatch, config_stub, caplog,
                                backend, value, expected):
        monkeypatch.setattr(qtargs.objects, 'backend', backend)
        if value is None:
            monkeypatch.delenv('QTWEBENGINE_CHROMIUM_FLAGS', raising=False)
        else:
            monkeypatch.setenv('QTWEBENGINE_CHROMIUM_FLAGS', value)

        with caplog.at_level(logging.WARNING):
            qtargs.init_envvars()

        if expected is None:
            assert not caplog.messages
        else:
            assert len(caplog.messages) == 1
            msg = caplog.messages[0]
            assert msg.startswith(f'You have QTWEBENGINE_CHROMIUM_FLAGS={expected} set')
