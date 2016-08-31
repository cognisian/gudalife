
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

    def draw_pixel(self, widget, x, y):
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

    def on_mouse_move(self, widget, event=None):
        (window, x, y, state) = event.window.get_pointer()
        if state & Gdk.ModifierType.BUTTON1_MASK:
            self.draw_pixel(widget, x, y)

        self._status.push(1, '(%i, %i)' % (x, y))

    def on_mouse_release(self, widget, event=None):
        if self._surface is None:
            return False

        if event.button == 1:
            self.draw_pixel(widget, event.x, event.y)
