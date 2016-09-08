
import cairo
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, Gdk


class GudaLifeWindowHandler(GObject.GObject):
    def __init__(self, window=None):
        self._window = window

        app = self._window.get_application()
        self._status = app.builder.get_object('status')
        self._status.push(1, 'Welcome to GudaLife')

        self._draw_state = True
        self._run_state = False

    def draw_pixel(self, widget, x, y):

        # Create the "pixel"
        update_rect = Gdk.Rectangle()
        update_rect.x = x
        update_rect.y = y
        update_rect.width = 1
        update_rect.height = 1

        cairo_ctx = cairo.Context(self._surface)

        Gdk.cairo_rectangle(cairo_ctx, update_rect)
        cairo_ctx.set_source_rgb(1, 1, 1)
        cairo_ctx.fill()

        widget.get_window().invalidate_rect(update_rect, False)

    def on_quit(self, widget, event=None):
        self._window.destroy()

    def on_draw(self, widget, event=None):
        event.set_source_surface(self._surface, 0, 0)
        event.paint()

    def on_config_drawarea(self, widget, event=None):
        allocation = widget.get_allocation()
        self._surface = widget.get_window().create_similar_surface(
            cairo.CONTENT_COLOR,
            allocation.width,
            allocation.height)

        cairo_ctx = cairo.Context(self._surface)
        cairo_ctx.set_source_rgb(0, 0, 0)
        cairo_ctx.paint()

    def on_life_draw(self, widget, event=None):
        if widget.get_active():
            self._draw_state = True
        else:
            self._draw_state = False

    def on_life_play(self, widget, event=None):
        widget.set_sensitive(False)

        app = self._window.get_application()

        toggle = app.builder.get_object('draw')
        toggle.set_active(False)
        toggle.set_sensitive(False)

        button = app.builder.get_object('stop')
        button.set_sensitive(True)

    def on_life_stop(self, widget, event=None):
        widget.set_sensitive(False)

        app = self._window.get_application()

        toggle = app.builder.get_object('draw')
        toggle.set_active(True)
        toggle.set_sensitive(True)

        button = app.builder.get_object('play')
        button.set_sensitive(True)

    def on_mouse_move(self, widget, event=None):
        (window, x, y, state) = event.window.get_pointer()

        if self._draw_state:
            if state & Gdk.ModifierType.BUTTON1_MASK:
                self.draw_pixel(widget, x, y)

        self._status.push(1, '(%i, %i)' % (x, y))

    def on_mouse_release(self, widget, event=None):
        if self._surface is None:
            return False

        if self._draw_state & event.button == 1:
            self.draw_pixel(widget, event.x, event.y)
