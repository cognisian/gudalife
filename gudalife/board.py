import time
import threading
import pprint
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib


class GudaLifeDict:
    """ Implement a GudaLife state (alive/dead) interface using a dictionary as a sparse matrix implementation
    """
    def __init__(self, width=None, height=None):

        self.width = width
        self.height = height

        self._state = {}

    def set_state(self, row, col, value=False):
        """ Set the alive(true)/dead(false) state at row,col """
        if row < 0 or row >= self.height:
            raise IndexError

        if col < 0 or col >= self.width:
            raise IndexError

        # Set a single bit to indicate alive/dead at row,col
        # This means setting to 1 (=b00000010 when col = 6) when curr value = 0
        # Since we are storing an uint8 the left most bit would represent the
        # next bit in col, we use 128 and right shift the bit to calc mask for
        # proper column
        # We use the get() method on dict to ensure a default value is used as
        # there are no keys when setting for first time
        state = self._state.get((row, col // 8), 0)
        if value:
            state |= (128 >> (col % 8))
        else:
            state &= ~(128 >> (col % 8))
        self._state[row, col // 8] = state

    def get_state(self, row, col):
        """ Get the alive/dead state at row,col """
        return (self._state.get((row, col // 8), 0) & (128 >> (col % 8))) != 0

    def get_neighbours(self, row, col):
        """ Get the set of neighbours for row, col """

        # Check the bounds (no wrap around) of the neighbourhood or row,col
        start_row = row - 1
        if (start_row < 0):
            start_row = 0

        end_row = row + 1
        if (end_row >= self.height):
            end_row = self.height - 1

        start_col = col - 1
        if (start_col < 0):
            start_col = 0

        end_col = col + 1
        if (end_col >= self.width):
            end_col = self.width - 1

        # Loop over the neighbours to cell row,col and add to array
        rows = end_row - start_row + 1
        cols = end_col - start_col + 1
        neighbours = [[0] * cols for _ in range(rows)]

        i = 0
        for check_row in range(start_row, end_row + 1):
            j = 0
            for check_col in range(start_col, end_col + 1):
                # Add current value to neighbours array
                neighbours[i][j] = self.get_state(check_row, check_col)
                # Do not add the row,col cell state we are checking to
                # neighbours list
                if check_col == col and check_row == row:
                    neighbours[i][j] = False

                j += 1
            i += 1

        return neighbours


class GudaLifeBoard:
    def __init__(self, width=None, height=None, update_func=None):

        self._step = 0
        self._cancel = threading.Event()

        self._curr_state = GudaLifeDict(width, height)
        self._next_state = None

        self._update = update_func

    def width(self):
        return self._curr_state.width

    def height(self):
        return self._curr_state.height

    def alive(self, row, col):
        # Mark row,col as alive (1)
        self._curr_state.set_state(row, col, True)

    def dead(self, row, col):
        # Mark row,col as dead (0)
        self._curr_state.set_state(row, col, False)

    def is_alive(self, row, col):
        return self._curr_state.get_state(row, col)

    def will_be_alive(self, row, col):
        """ Calculate if the cell located at row, col will be alive or dead next round
        """

        # Get neighbour list
        neighbours = self._curr_state.get_neighbours(row, col)

        # Initialize the neighbour array to boolean
        alive_next = False
        alive_count = 0

        # Loop over the neighbours and count the number of alive neighbours
        for check_row in neighbours:
            for check_col in check_row:
                if check_col:
                    alive_count += 1

        # Check if the current cell is alive
        if self.is_alive(row, col):
            if alive_count >= 2 and alive_count <= 3:
                alive_next = True
        else:
            if alive_count == 3:
                alive_next = True

        return alive_next

    def is_cancelled(self):
        return self._cancel.isSet()

    def cancel(self):
        if self._cancel:
            step = 0
            self._cancel.set()

    def loop(self):
        """ Perform one loop of the GoL board to generate next state """

        # Create new empty array to hold next frame
        next_state = GudaLifeDict(self._curr_state.width,
                                  self._curr_state.height)

        # Perform one update of entire GoL board
        for row in range(self._curr_state.height):
            if self.is_cancelled():
                break

            for col in range(self._curr_state.width):
                if self.is_cancelled():
                    break

                # Check if current cell will be alive, if so set to 1
                alive = self.will_be_alive(row, col)
                if alive:
                    next_state.set_state(row, col, True)

        # Set updated state to be current
        self._curr_state = next_state

    def turn(self):
        """ Animate Game of Life until cancelled """

        while not self.is_cancelled():
            # Perform one loop update
            self.loop()
            self._step += 1

            # notify listeners of update
            if self._update is not None and not self.is_cancelled:
                GLib.idle_add(
                    self._update,
                    self._step,
                    priority=GLib.PRIORITY_LOW)
                time.sleep(0.5)
