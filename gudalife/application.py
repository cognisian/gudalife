import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

from gudalife.window import GudaLifeWindowHandler
from gudalife.board import GudaLifeBoard


class GudaLife(Gtk.Application):
    def __init__(self, datadir):
        Gtk.Application.__init__(self, application_id='com.cognisian.gudalife', flags=Gio.ApplicationFlags.FLAGS_NONE)

        GLib.set_application_name('GudaLife')
        GLib.set_prgname('gudalife')

        self._window = None
        self._window_handler = None
        self._datadir = datadir

        self.board = None

        self.draw_state = True

        self.width = 0
        self.height = 0

    def do_startup(self):
        Gtk.Application.do_startup(self)

        # Load resources
        resource = Gio.resource_load(
            self._datadir + '/gudalife-resources.gresource')
        Gio.Resource._register(resource)

        self.builder = Gtk.Builder()

        # Build AppMenu
        self.builder.add_from_resource('/com/cognisian/gudalife/ui/app-menu.ui')
        appmenu = self.builder.get_object('app-menu')
        self.builder.connect_signals(self)
        self.set_app_menu(appmenu)

        simpleAction = Gio.SimpleAction.new('quit', None)
        simpleAction.connect('activate', self.on_quit)
        self.add_action(simpleAction)

        simpleAction = Gio.SimpleAction.new('about', None)
        simpleAction.connect('activate', self.on_about)
        self.add_action(simpleAction)

    def do_activate(self):
        if not self._window:
            self.builder.add_from_resource('/com/cognisian/gudalife/ui/main.ui')
            self._window = self.builder.get_object('main')
            self._window.set_application(self)
            self._window_handler = GudaLifeWindowHandler(self._window)
            self.builder.connect_signals(self._window_handler)

        # Show Window
        self._window.present()

        # Create GoL board to match drawing area
        drawarea = self.builder.get_object('life')
        rect = drawarea.get_allocation()
        self.board = GudaLifeBoard(
            rect.width,
            rect.height,
            self._window_handler.on_life_update)

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

    def on_quit(self, action, param=None):
        if self.board and not self.draw_state:
            self.board.cancel_turn()

        if self._window:
            self._window.destroy()

        self.quit()

    def on_about(self, action, param=None):
        self.builder.add_from_resource('/com/cognisian/gudalife/ui/about.ui')
        about = self.builder.get_object('about')
        about.set_transient_for(self._window)
        about.show()
