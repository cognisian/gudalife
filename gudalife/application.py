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
        self._prefs_handler = None
        self._datadir = datadir

        self.builder = None

        self.settings = None
        self.board = None
        self.draw_state = True

    def do_startup(self):
        Gtk.Application.do_startup(self)

        # Load resources
        resource = Gio.resource_load(
            self._datadir + '/gudalife-resources.gresource')
        Gio.Resource._register(resource)

        # Load app settings
        # schema_source = Gio.SettingsSchemaSource.new_from_directory(
        #     DIRECTORY, Gio.SettingsSchemaSource.get_default(), False)
        # schema = Gio.SettingsSchemaSource.lookup(
        #     schema_source, schema_id, False)
        #
        # if not schema:
        #     raise Exception("Cannot get GSettings  schema")
        #
        # instance = Gio.Settings.new_full(schema, None, path)
        self.settings = Gio.Settings('com.cognisian.gudalife')

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

        simpleAction = Gio.SimpleAction.new('preferences', None)
        simpleAction.connect('activate', self.on_preferences)
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

    def on_preferences(self, action, param=None):
        self.builder.add_from_resource(
            '/com/cognisian/gudalife/ui/preferences.ui')
        prefs = self.builder.get_object('prefs')
        prefs.set_transient_for(self._window)
        prefs.set_response_sensitive(1, True)

        # Set values based on schema values
        width_widget = self.builder.get_object('width')
        width = self.settings.get_int('width')
        width_widget.set_value(width)

        height_widget = self.builder.get_object('height')
        height = self.settings.get_int('height')
        height_widget.set_value(height)

        # Show Prefs dialog
        resp = prefs.run()

        # Process response_id from dialog
        if resp == 1:
            self.settings.set_int('width', width_widget.get_value())
            self.settings.set_int('height', height_widget.get_value())
            self.settings.sync()

        prefs.destroy()
