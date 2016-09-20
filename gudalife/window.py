import threading

import numpy as np

import cairo
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, Gdk


class GudaLifeWindowHandler(GObject.GObject):
    def __init__(self, window=None):
        self._window = window

        self._app = self._window.get_application()

        self._status = self._app.builder.get_object('status')
        self._status.push(1, 'Welcome to GudaLife')

        self._surface = None
        self._drawing = True
        self._update_thd = None

    def draw_pixel(self, widget, x, y):
        if self._drawing:
            # Create the "pixel" only if not running animatiion
            update_rect = Gdk.Rectangle()
            update_rect.x = x
            update_rect.y = y
            update_rect.width = 1
            update_rect.height = 1

            cairo_ctx = cairo.Context(self._surface)

            Gdk.cairo_rectangle(cairo_ctx, update_rect)
            cairo_ctx.set_source_rgb(1, 1, 1)
            cairo_ctx.fill()

            self._app.board.alive(x, y)

            widget.get_window().invalidate_rect(update_rect, False)

            # print("Draw Pixel %ix%i" % (x, y))

    def on_quit(self, widget, event=None):
        # Cancel the GoL board update thread
        if self._update_thd and self._update_thd.is_alive():
            self._app.board.cancel()
            self._update_thd.join()

        self._window.destroy()

    def on_draw(self, widget, event=None):
        event.set_source_surface(self._surface, 0, 0)
        event.paint()

    def on_config_drawarea(self, widget, event=None):
        allocation = widget.get_allocation()

        # Create the drawing surface and context
        self._surface = widget.get_window().create_similar_surface(
            cairo.CONTENT_COLOR,
            allocation.width,
            allocation.height)

        cairo_ctx = cairo.Context(self._surface)
        cairo_ctx.set_source_rgb(0, 0, 0)
        cairo_ctx.paint()

    def on_life_draw(self, widget, event=None):
        if widget.get_active():
            self._app.draw_state = True
        else:
            self._app.draw_state = False

        # print("Life Draw %ix%i" % (x, y))

    def on_life_play(self, widget, event=None):
        widget.set_sensitive(False)

        app = self._window.get_application()

        toggle = self._app.builder.get_object('draw')
        toggle.set_active(False)
        toggle.set_sensitive(False)

        button = self._app.builder.get_object('stop')
        button.set_sensitive(True)

        # Update GoL
        if not self._update_thd or not self._update_thd.is_alive():
            self._update_thd = threading.Thread(target=self._app.board.turn)
        self._update_thd.start()

    def on_life_update(self, step, arr):

        shape = arr.shape
        if shape[0] != self._app.board._height:
            print("Rows %i %i" % (shape[0], self._app.height))
            return
        if (shape[1] * 8) != self._app.board._width + 1:
            print("Cols %i %i" % (shape[1] * 8, self._app.board._width))
            return

        draw_rect = Gdk.Rectangle()
        draw_rect.x = 0
        draw_rect.y = 0
        draw_rect.width = self._app.board._width
        draw_rect.height = self._app.board._height

        for row in range(shape[0]):
            for col in range(shape[1]):
                for col_bit in range(8):
                    update_rect = Gdk.Rectangle()
                    update_rect.x = row
                    update_rect.y = col + col_bit
                    update_rect.width = 1
                    update_rect.height = 1

                    cairo_ctx = cairo.Context(self._surface)

                    Gdk.cairo_rectangle(cairo_ctx, update_rect)
                    cairo_ctx.set_source_rgb(0, 0, 1)
                    cairo_ctx.fill()

            # Allow GUI updates
            while Gtk.events_pending():
                Gtk.main_iteration_do(False)

        widget = self._app.builder.get_object('life')
        widget.get_window().invalidate_rect(draw_rect, False)

        # print("Update %i" % step)
        # print("Board %i" % board.size)

    def on_life_stop(self, widget, event=None):
        # Cancel the GoL board update thread
        if self._update_thd and self._update_thd.is_alive():
            self._app.board.cancel()
            self._update_thd.join()

        # Update GUI
        widget.set_sensitive(False)

        app = self._window.get_application()

        toggle = self._app.builder.get_object('draw')
        toggle.set_active(True)
        toggle.set_sensitive(True)

        button = self._app.builder.get_object('play')
        button.set_sensitive(True)

    def on_mouse_move(self, widget, event=None):
        (window, x, y, state) = event.window.get_pointer()

        if self._app.draw_state:
            if state & Gdk.ModifierType.BUTTON1_MASK:
                self.draw_pixel(widget, x, y)

        self._status.push(1, '(%i, %i)' % (x, y))
        # print("Move %ix%i" % (x, y))

    def on_mouse_release(self, widget, event=None):
        if self._surface is None:
            return False

        (window, x, y, state) = event.window.get_pointer()
        if self._app.draw_state & (event.button == 1):
            self.draw_pixel(widget, x, y)

        # print("Release %ix%i" % (x, y))
