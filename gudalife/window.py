import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


class GudaLifeWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self,
                                       application=app,
                                       title="GudaLife")
        self.set_icon_name('gudalife')
