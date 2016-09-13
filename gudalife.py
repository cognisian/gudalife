#!/usr/bin/env python
import os
import sys
import locale
import gettext
import signal

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

datadir = '/usr/share'
localedir = '/usr/share/locale'
pkgdatadir = '/usr/share/gudalife'
appdatadir = '/usr/share/gudalife'
iconsrootdir = '/usr/share/icons'

srcdir = os.path.abspath(os.path.dirname(__file__))
if os.path.exists(os.path.join(srcdir, 'gudalife.doap')):
    print('Running from source tree, using local files')
    datadir = os.path.join(srcdir, 'data')
    pkgdatadir = datadir
    appdatadir = os.path.join(datadir, 'resources')
    iconsrootdir = os.path.join(datadir, 'pixmaps')
    if not os.environ.get('GSETTINGS_SCHEMA_DIR'):
        os.environ['GSETTINGS_SCHEMA_DIR'] = pkgdatadir + '/schemas'


def install_excepthook():
    """ Make sure we exit when an unhandled exception occurs. """
    old_hook = sys.excepthook

    def new_hook(etype, evalue, etb):
        old_hook(etype, evalue, etb)
        while Gtk.main_level():
            Gtk.main_quit()
        sys.exit()
    sys.excepthook = new_hook

if __name__ == "__main__":
    install_excepthook()

    locale.bindtextdomain('gudalife', localedir)
    locale.textdomain('gudalife')
    gettext.bindtextdomain('gudalife', localedir)
    gettext.textdomain('gudalife')

    from gudalife.application import GudaLife

    app = GudaLife(appdatadir)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
