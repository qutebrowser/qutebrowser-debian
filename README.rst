===========
qutebrowser
===========


|qutebrowser logo| **A keyboard-driven, vim-like browser based on PyQt5
and Qt.**

|Build Status| |AppVeyor build status| |coverage badge|

`website <https://www.qutebrowser.org>`__ \|
`blog <https://blog.qutebrowser.org>`__ \|
`FAQ <https://github.com/qutebrowser/qutebrowser/blob/master/doc/faq.asciidoc>`__
\| `contributing <https://www.qutebrowser.org/doc/contributing.html>`__
\| `releases <https://github.com/qutebrowser/qutebrowser/releases>`__ \|
`installing <https://github.com/qutebrowser/qutebrowser/blob/master/doc/install.asciidoc>`__

qutebrowser is a keyboard-focused browser with a minimal GUI. It’s based
on Python and PyQt5 and free software, licensed under the GPL.

It was inspired by other browsers/addons like dwb and
Vimperator/Pentadactyl.


Screenshots
===========

|screenshot 1| |screenshot 2| |screenshot 3| |screenshot 4|


Downloads
=========

See the `github releases
page <https://github.com/qutebrowser/qutebrowser/releases>`__ for
available downloads and the `INSTALL <doc/install.asciidoc>`__ file for
detailed instructions on how to get qutebrowser running on various
platforms.


Documentation
=============

In addition to the topics mentioned in this README, the following
documents are available:

-  | `Key binding
     cheatsheet <https://raw.githubusercontent.com/qutebrowser/qutebrowser/master/doc/img/cheatsheet-big.png>`__:
   | |qutebrowser key binding cheatsheet|

-  `Quick start guide <doc/quickstart.asciidoc>`__

-  `Free training
   course <https://www.shortcutfoo.com/app/dojos/qutebrowser>`__ to
   remember those key bindings

-  `Frequently asked questions <doc/faq.asciidoc>`__

-  `Configuring qutebrowser <doc/help/configuring.asciidoc>`__

-  `Contributing to qutebrowser <doc/contributing.asciidoc>`__

-  `Installing qutebrowser <doc/install.asciidoc>`__

-  `Change Log <doc/changelog.asciidoc>`__

-  `Reporting segfaults <doc/stacktrace.asciidoc>`__

-  `How to write userscripts <doc/userscripts.asciidoc>`__


Getting help
============

You can get help in the IRC channel
```#qutebrowser`` <irc://irc.freenode.org/#qutebrowser>`__ on
`Freenode <https://freenode.net/>`__
(`webchat <https://webchat.freenode.net/?channels=#qutebrowser>`__), or
by writing a message to the
`mailinglist <https://lists.schokokeks.org/mailman/listinfo.cgi/qutebrowser>`__
at qutebrowser@lists.qutebrowser.org.

There’s also an `announce-only
mailinglist <https://lists.schokokeks.org/mailman/listinfo.cgi/qutebrowser-announce>`__
at qutebrowser-announce@lists.qutebrowser.org (the announcements also
get sent to the general qutebrowser@ list).

If you’re a reddit user, there’s a
`/r/qutebrowser <https://www.reddit.com/r/qutebrowser/>`__ subreddit
there.


Contributions / Bugs
====================

You want to contribute to qutebrowser? Awesome! Please read `the
contribution guidelines <doc/contributing.asciidoc>`__ for details and
useful hints.

If you found a bug or have a feature request, you can report it in
several ways:

-  Use the built-in ``:report`` command or the automatic crash dialog.

-  Open an issue in the Github issue tracker.

-  Write a mail to the
   `mailinglist <https://lists.schokokeks.org/mailman/listinfo.cgi/qutebrowser>`__
   at qutebrowser@lists.qutebrowser.org.

For security bugs, please contact me directly at mail@qutebrowser.org,
GPG ID `0x916eb0c8fd55a072 <https://www.the-compiler.org/pubkey.asc>`__.


Requirements
============

The following software and libraries are required to run qutebrowser:

-  `Python <https://www.python.org/>`__ 3.5 or newer (3.6 recommended)

-  `Qt <https://www.qt.io/>`__ 5.7.1 or newer (5.11 recommended, support
   for < 5.9 will be dropped soon) with the following modules:

   -  QtCore / qtbase

   -  QtQuick (part of qtbase in some distributions)

   -  QtSQL (part of qtbase in some distributions)

   -  QtOpenGL

   -  QtWebEngine, or

   -  alternatively QtWebKit - support for QtWebKit will be dropped
      soon, and only the `updated
      fork <https://github.com/annulen/webkit/wiki>`__ (5.212) is
      supported

-  `PyQt <https://www.riverbankcomputing.com/software/pyqt/intro>`__
   5.7.0 or newer (5.11 recommended, support for < 5.9 will be dropped
   soon) for Python 3

-  `pkg_resources/setuptools <https://pypi.python.org/pypi/setuptools/>`__

-  `pyPEG2 <https://fdik.org/pyPEG/>`__

-  `jinja2 <http://jinja.pocoo.org/>`__

-  `pygments <http://pygments.org/>`__

-  `PyYAML <https://github.com/yaml/pyyaml>`__

-  `attrs <https://www.attrs.org/>`__

The following libraries are optional:

-  `cssutils <http://cthedot.de/cssutils/>`__ (for an improved
   ``:download --mhtml`` with QtWebKit).

-  On Windows, `colorama <https://pypi.python.org/pypi/colorama/>`__ for
   colored log output.

-  `asciidoc <http://asciidoc.org/>`__ to generate the documentation for
   the ``:help`` command, when using the git repository (rather than a
   release).

See `the documentation <doc/install.asciidoc>`__ for directions on how
to install qutebrowser and its dependencies.


Donating
========

Working on qutebrowser is a very rewarding hobby, but like (nearly) all
hobbies it also costs some money. Namely I have to pay for the server
and domain, and do occasional hardware upgrades  [1]_.

If you want to give me a beer or a pizza back, I’m trying to make it as
easy as possible for you to do so. If some other way would be easier for
you, please get in touch!

-  PayPal: me@the-compiler.org

-  Bitcoin:
   `1PMzbcetAHfpxoXww8Bj5XqquHtVvMjJtE <bitcoin:1PMzbcetAHfpxoXww8Bj5XqquHtVvMjJtE>`__


Sponsors
========

Thanks a lot to `MacStadium <https://www.macstadium.com/>`__ for
supporting qutebrowser with a free hosted Mac Mini via their `Open
Source Project <https://www.macstadium.com/opensource>`__.

(They don’t require including this here - I’ve just been very happy with
their offer, and without them, no macOS releases or tests would exist)

Thanks to the `HSR Hochschule für Technik
Rapperswil <https://www.hsr.ch/>`__, which made it possible to work on
qutebrowser extensions as a student research project.

|powered by MacStadium| |HSR Hochschule für Technik Rapperswil|


Authors
=======

qutebrowser’s primary author is Florian Bruhin (The Compiler), but
qutebrowser wouldn’t be what it is without the help of `hundreds of
contributors <https://github.com/qutebrowser/qutebrowser/graphs/contributors>`__!

Additionally, the following people have contributed graphics:

-  Jad/\ `yelo <https://yelostudio.com>`__ (new icon)

-  WOFall (original icon)

-  regines (key binding cheatsheet)

Also, thanks to everyone who contributed to one of qutebrowser’s
`crowdfunding campaigns <doc/backers.asciidoc>`__!


Similar projects
================

Many projects with a similar goal as qutebrowser exist. Most of them
were inspirations for qutebrowser in some way, thanks for that!


Active
------

-  `vimb <https://fanglingsu.github.io/vimb/>`__ (C, GTK+ with WebKit2)

-  `luakit <https://luakit.github.io/luakit/>`__ (C/Lua, GTK+ with
   WebKit2)

-  `surf <https://surf.suckless.org/>`__ (C, GTK+ with WebKit1/WebKit2)

-  `next <https://github.com/next-browser/next/>`__ (Lisp, Emacs-like,
   GTK+ with WebKit)

-  `webmacs <https://github.com/parkouss/webmacs/>`__ (Python,
   Emacs-like with QtWebEngine)

-  Chrome/Chromium addons: `Vimium <https://vimium.github.io/>`__,
   `Surfingkeys <https://github.com/brookhong/Surfingkeys>`__,

-  Firefox addons (based on WebExtensions):
   `Vimium-FF <https://addons.mozilla.org/en-GB/firefox/addon/vimium-ff/>`__
   (experimental), `Vim
   Vixen <https://github.com/ueokande/vim-vixen>`__,
   `VVimpulation <https://github.com/amedama41/vvimpulation>`__,
   `Tridactyl <https://github.com/cmcaine/tridactyl>`__ (working on a
   `better API <https://bugzilla.mozilla.org/show_bug.cgi?id=1215061>`__
   for keyboard integration in Firefox).


Inactive
--------

-  `dwb <https://bitbucket.org/portix/dwb>`__ (C, GTK+ with WebKit1,
   `unmaintained <https://bitbucket.org/portix/dwb/pull-requests/22/several-cleanups-to-increase-portability/diff>`__
   - main inspiration for qutebrowser)

-  `vimprobable <https://sourceforge.net/p/vimprobable/wiki/Home/>`__
   (C, GTK+ with WebKit1)

-  `jumanji <https://wiki.archlinux.org/index.php?title=Jumanji>`__ (C,
   GTK+ with WebKit1, original site is gone but Arch Linux has some
   data)

-  `conkeror <http://conkeror.org/>`__ (Javascript, Emacs-like,
   XULRunner/Gecko)

-  `uzbl <https://www.uzbl.org/>`__ (C, GTK+ with WebKit1/WebKit2)

-  Firefox addons (not based on WebExtensions or no recent activity):
   `Vimperator <http://www.vimperator.org/>`__,
   `Pentadactyl <http://bug.5digits.org/pentadactyl/index>`__,
   `VimFx <https://github.com/akhodakivskiy/VimFx>`__, `Saka
   Key <https://key.saka.io>`__,
   `QuantumVim <https://github.com/shinglyu/QuantumVim>`__,

-  Chrome/Chromium addons:
   `ViChrome <https://chrome.google.com/webstore/detail/vichrome/gghkfhpblkcmlkmpcpgaajbbiikbhpdi?hl=en>`__,
   `Vrome <https://github.com/jinzhu/vrome>`__ `Saka
   Key <https://key.saka.io>`__,
   `cVim <https://github.com/1995eaton/chromium-vim>`__,


License
=======

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along
with this program. If not, see https://www.gnu.org/licenses/gpl-3.0.txt.


pdf.js
======

qutebrowser optionally uses
`pdf.js <https://github.com/mozilla/pdf.js/>`__ to display PDF files in
the browser. Windows releases come with a bundled pdf.js.

pdf.js is distributed under the terms of the Apache License. You can
find a copy of the license in ``qutebrowser/3rdparty/pdfjs/LICENSE`` (in
the Windows release or after running
``scripts/dev/update_3rdparty.py``), or online
`here <https://www.apache.org/licenses/LICENSE-2.0.html>`__.

.. [1]
   It turned out a 160 GB SSD is rather small - the VMs and custom Qt
   builds I use for testing/developing qutebrowser need about 100 GB of
   space

.. |qutebrowser logo| image:: icons/qutebrowser-64x64.png
.. |Build Status| image:: https://travis-ci.org/qutebrowser/qutebrowser.svg?branch=master
.. |AppVeyor build status| image:: https://ci.appveyor.com/api/projects/status/5pyauww2k68bbow2/branch/master?svg=true
.. |coverage badge| image:: https://codecov.io/github/qutebrowser/qutebrowser/coverage.svg?branch=master
.. |screenshot 1| image:: doc/img/main.png
.. |screenshot 2| image:: doc/img/downloads.png
.. |screenshot 3| image:: doc/img/completion.png
.. |screenshot 4| image:: doc/img/hints.png
.. |qutebrowser key binding cheatsheet| image:: https://raw.githubusercontent.com/qutebrowser/qutebrowser/master/doc/img/cheatsheet-small.png
.. |powered by MacStadium| image:: .github/img/macstadium.png
.. |HSR Hochschule für Technik Rapperswil| image:: .github/img/hsr.png
