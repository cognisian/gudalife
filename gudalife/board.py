import time
import threading
import numpy as np

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib


class GudaLifeBoard:
    def __init__(self, width=None, height=None, update=None):

        self._width = width
        self._height = height

        self._step = 0
        self._cancel = None

        # create a bit array with width x height bits, but a byte per entry
        # so the array entries are x = (width // 8) + 1,
        #                          y = height
        arr_width = (width // 8) + 1
        arr_height = height

        self._curr_state = np.zeros((arr_height, arr_width), dtype=np.uint8)
        self._next_state = None

        self._update = update

    def alive(self, row, col):
        # Mark row,col as alive (1)
        # This means setting to 1 (=0b00000010 when col = 6) when curr value = 0
        # Since we are storing an uint8 the left most bit would represent the
        # next bit in col, we use 128 and right shift the bit to calc mask for
        # proper column
        self._curr_state[row, col // 8] |= (128 >> (col % 8))

    def dead(self, row, col):
        # Mark row,col as dead (0)
        # This means setting to 0 (=0b11111101 when x = 6) when curr value = 255
        # Since we are storing an uint8 the left most bit would represent the
        # next bit in col, we use 128 and right shift the bit to calc mask for
        # proper column, we use compliment to turn 1 to 0 and all else to 1 so that the bitwise and will only switch to zero the value in col
        self._curr_state[row, col // 8] &= ~(128 >> (col % 8))

    def is_alive(self, row, col):
        return (self._curr_state[row, col // 8] & (128 >> (col % 8))) != 0

    def will_be_alive(self, row, col):
        # Calculate if the cell located at row, col will be alive or dead next # round

        start_row = row - 1
        if (start_row < 0):
            start_row = 0

        end_row = row + 1
        if (end_row >= self._height):
            end_row = self._height - 1

        start_col = col - 1
        if (start_col < 0):
            start_col = 0

        end_col = col + 1
        if (end_col >= self._width):
            end_col = self._width - 1

        neighbours = np.zeros((end_row - start_row + 1,
                               end_col - start_col + 1), dtype=np.bool)
        i = 0
        for check_row in range(start_row, end_row + 1):
            j = 0
            for check_col in range(start_col, end_col + 1):
                col_idx = check_col // 8
                neighbours[i, j] = (self._curr_state[check_row, col_idx] & (
                    128 >> (check_col % 8))) != 0
                j += 1

            i += 1

        alive_next = False
        count = np.count_nonzero(neighbours)
        if count >= 2 or count <= 3:
            alive_next = True

        return alive_next

    def is_cancelled(self):
        return self._cancel.isSet()

    def cancel(self):
        if self._cancel:
            self._cancel.set()

    def turn(self):

        self._cancel = threading.Event()

        print("Starting Run")
        while not self.is_cancelled():

            # Create new empty array to hold next frame
            self._next_state = np.zeros_like(self._curr_state)

            # Perform one update of entire GoL board
            for row in range(self._height):
                if self.is_cancelled():
                    print("Stopping Run on row")
                    break

                for col in range(self._width):
                    if self.is_cancelled():
                        print("Stopping Run on col")
                        break

                    alive = self.will_be_alive(row, col)
                    if alive:
                        self._next_state[row, col // 8] |= (128 >> (col % 8))

            # Uppdate step counter and set current state
            self._step += 1
            self._curr_state = self._next_state

            # notify listeners of update
            if not self.is_cancelled():
                GLib.idle_add(
                    self._update,
                    self._step, self._curr_state,
                    priority=GLib.PRIORITY_LOW)
                time.sleep(0.5)

        print("Stopped")
