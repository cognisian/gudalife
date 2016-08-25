import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

from gudalife.window import GudaLifeWindow


class GudaLife(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self, application_id='com.cognisian.gudalife', flags=Gio.ApplicationFlags.FLAGS_NONE)

        GLib.set_application_name('GudaLife')
        GLib.set_prgname('gudalife')

        self._window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

        # Build AppMenu
        builder = Gtk.Builder()
        builder.add_from_resource('/com/cognisian/gudalife/gtk/menus.ui')

    def do_activate(self):
        if not self._window:
            self._window = GudaLifeWindow(self)

        self._window.present()

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

    def on_quit(self, action, param=None):
        self._window.destroy()
        self.quit()

    def on_about(self, action, param=None):
        pass

    def on_about_response(self, widget, response):
        widget.destroy()
