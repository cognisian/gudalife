import unittest
from gudalife.board import GudaLifeDict, GudaLifeBoard


class TestGudaLifeDict(unittest.TestCase):
    def setUp(self):
        self.board = GudaLifeDict(3, 3)

    def test_set_alive(self):
        """ Test to ensure that setting cell to alive is alive """
        self.board.set_state(1, 1, True)
        self.assertEqual(self.board.get_state(1, 1), True)

    def test_set_dead(self):
        """ Test to ensure that setting cell to dead is dead """
        # Set everything to alive
        for row in range(0, 3):
            for col in range(0, 3):
                self.board.set_state(row, col, True)

        # Set test condition
        self.board.set_state(1, 1, False)

        self.assertEqual(self.board.get_state(1, 1), False)

    def test_get_neighbours_centre(self):
        """ Test that neighbours are returned in 3x3 arr when cell in middle """
        # Set the diagonal to be alive
        self.board.set_state(0, 0, True)
        self.board.set_state(1, 1, True)
        self.board.set_state(2, 2, True)

        # Set test condition, get neighbours of cell (1,1)
        neighbours = self.board.get_neighbours(1, 1)

        # Assert
        self.assertEqual(neighbours[0][0], 1)
        # The current cell we are checking (1,1) value is not added to
        # neighbours array
        self.assertEqual(neighbours[1][1], 0)
        self.assertEqual(neighbours[2][2], 1)

        # Everything else is dead
        self.assertEqual(neighbours[0][1], 0)
        self.assertEqual(neighbours[0][2], 0)
        self.assertEqual(neighbours[1][0], 0)
        self.assertEqual(neighbours[1][2], 0)
        self.assertEqual(neighbours[2][0], 0)
        self.assertEqual(neighbours[2][1], 0)

    def test_get_neighbours_edge(self):
        """ Test that neighbours are returned in 2x3 arr when cell on edge """
        # Set the diagonal to be alive
        self.board.set_state(0, 0, True)
        self.board.set_state(1, 1, True)
        self.board.set_state(2, 2, True)

        # Set test condition, get neighbours of cell (0,1)
        neighbours = self.board.get_neighbours(0, 1)

        # Assert neighbours array is sized correctly
        # As we are on edge there should only be 2 rows and 3 cols returned
        self.assertEqual(len(neighbours), 2)
        self.assertEqual(len(neighbours[0]), 3)
        self.assertEqual(len(neighbours[1]), 3)
        with self.assertRaises(IndexError):
            neighbours[2][0]

        # Assert neighbours returned properly
        self.assertEqual(neighbours[0][0], 1)
        # The current cell we are checking (0,1) value is not added to
        # neighbours array
        self.assertEqual(neighbours[0][1], 0)
        self.assertEqual(neighbours[0][2], 0)
        self.assertEqual(neighbours[1][0], 0)
        self.assertEqual(neighbours[1][1], 1)
        self.assertEqual(neighbours[1][2], 0)

    def test_get_neighbours_corner(self):
        """ Test that neighbours are returned in 2x2 arr when cell on corner """
        # Set the diagonal to be alive
        self.board.set_state(0, 0, True)
        self.board.set_state(1, 1, True)
        self.board.set_state(2, 2, True)

        # Set test condition, get neighbours of cell (0,0)
        neighbours = self.board.get_neighbours(0, 0)

        # Assert neighbours array is sized correctly
        # As we are on edge there should only be 2 rows and 2 cols returned
        self.assertEqual(len(neighbours), 2)
        self.assertEqual(len(neighbours[0]), 2)
        self.assertEqual(len(neighbours[1]), 2)
        with self.assertRaises(IndexError):
            neighbours[2][0]

        # Assert neighbours returned properly
        self.assertEqual(neighbours[0][0], 0)
        # The current cell we are checking (0,1) value is not added to
        # neighbours array
        self.assertEqual(neighbours[0][1], 0)
        self.assertEqual(neighbours[1][0], 0)
        self.assertEqual(neighbours[1][1], 1)


class TestGudaLifeBoard(unittest.TestCase):
    def setUp(self):
        self.gol = GudaLifeBoard(3, 3, print)

    def test_update_alive_with_2_neighbours(self):
        # Set check cell to be alive
        self.gol.alive(1, 1)

        # Set 2 neighbour cell to be alive
        self.gol.alive(0, 0)
        self.gol.alive(2, 2)

        # Check if center cell will be alive next turn
        alive = self.gol.will_be_alive(1, 1)

        self.assertEqual(alive, True)

    def test_update_alive_with_3_neighbours(self):

        # Set check cell to be alive
        self.gol.alive(1, 1)

        # Set 3 neighbour cell to be alive
        self.gol.alive(0, 0)
        self.gol.alive(0, 2)
        self.gol.alive(2, 2)

        # Check if center cell will be alive next turn
        alive = self.gol.will_be_alive(1, 1)

        self.assertEqual(alive, True)

    def test_update_alive_with_4_neighbours(self):

        # Set check cell to be alive
        self.gol.alive(1, 1)

        # Set 3 neighbour cell to be alive
        self.gol.alive(0, 0)
        self.gol.alive(0, 1)
        self.gol.alive(0, 2)
        self.gol.alive(2, 2)

        # Check if center cell will be dead next turn
        alive = self.gol.will_be_alive(1, 1)

        self.assertEqual(alive, False)

    def test_update_dead_with_2_neighbours(self):
        # Set 2 neighbour cell to be alive
        self.gol.alive(0, 0)
        self.gol.alive(0, 2)

        # Check if center cell will be dead next turn
        alive = self.gol.will_be_alive(1, 1)

        self.assertEqual(alive, False)

    def test_update_dead_with_3_neighbours(self):
        # Set 3 neighbour cell to be alive
        self.gol.alive(0, 0)
        self.gol.alive(0, 2)
        self.gol.alive(2, 0)

        # Check if center cell will be dead next turn
        alive = self.gol.will_be_alive(1, 1)

        # Assert center is dead
        self.assertEqual(alive, True)


class TestGudaLifeAnimation(unittest.TestCase):
    def setUp(self):
        self.gol = GudaLifeBoard(6, 6)

    def test_update_block(self):
        """ Test that a 2x2 block will be same through 3 frames of update """
        # Create 2x2 block
        self.gol.alive(1, 1)
        self.gol.alive(1, 2)
        self.gol.alive(2, 1)
        self.gol.alive(2, 2)

        for i in range(3):
            self.gol.loop()
            self.assertGoLBlock()

    def test_update_blinker(self):
        """ Test that a vertical blinker will animate through 3 frames of update """
        # Create vertical blinker
        self.gol.alive(1, 1)
        self.gol.alive(2, 1)
        self.gol.alive(3, 1)

        self.gol.loop()
        # Should be horizontal
        self.assertRowAlive(2, 0, 3)

        self.gol.loop()
        # Should be back to vertical
        self.assertColAlive(1, 1, 3)

        self.gol.loop()
        # Should be horizontal
        self.assertRowAlive(2, 0, 3)

    def test_update_glider(self):
        """ Test that a glider will animate through 6 frames of update and have
            original shape but be located down one row and over one col
        """
        # Create glider
        self.gol.alive(1, 3)
        self.gol.alive(2, 4)
        self.gol.alive(3, 2)
        self.gol.alive(3, 3)
        self.gol.alive(3, 4)

        self.gol.loop()
        self.assertGliderFrame1(1, 2)

        self.gol.loop()
        self.assertGliderFrame2(1, 2)

        self.gol.loop()
        self.assertGliderFrame3(1, 2)

        self.gol.loop()
        self.assertGliderFrame4(1, 2)

    def assertRowAlive(self, check_row, start_col, cols):
        """ Assert row at check_row of cells of length cols starting at start_col are alive """
        check = [[False] * self.gol.width()
                 for _ in range(self.gol.height())]

        for j in range(start_col, start_col + cols):
            check[check_row][j] = True

        for row in range(self.gol.height()):
            for col in range(self.gol.width()):
                if self.gol._curr_state.get_state(row, col) != check[row][col]:
                    raise AssertionError

    def assertColAlive(self, check_col, start_row, rows):
        """ Assert col at check_col of cells of length rows starting at start_row are alive """
        check = [[False] * self.gol.width()
                 for _ in range(self.gol.height())]

        for i in range(start_row, start_row + rows):
            check[i][check_col] = True

        # Match entire current GoL board with the purpose built check array
        for row in range(self.gol.height()):
            for col in range(self.gol.width()):
                if self.gol._curr_state.get_state(row, col) != check[row][col]:
                    raise AssertionError

    def assertGliderFrame1(self, top, left):
        """ Assert current state matches the first frame of glider ie that the
            glider changed to first

            @top: The row of top left corner of the location of original glider
            @left: The col of top left corner of the location of original glider
        """

        # Build the glider frame
        check = [[False] * self.gol.width()
                 for _ in range(self.gol.height())]
        check[top + 1][left] = True
        check[top + 1][left + 1] = False
        check[top + 1][left + 2] = True
        check[top + 2][left] = False
        check[top + 2][left + 1] = True
        check[top + 2][left + 2] = True
        check[top + 3][left] = False
        check[top + 3][left + 1] = True
        check[top + 3][left + 2] = False

        # Match entire current GoL board with the purpose built check array
        for row in range(self.gol.height()):
            for col in range(self.gol.width()):
                if self.gol._curr_state.get_state(row, col) != check[row][col]:
                    raise AssertionError('At (%i,%i) %r != %r' % (row, col, self.gol._curr_state.get_state(row, col), check[row][col]))

    def assertGliderFrame2(self, top, left):
        """ Assert current state matches the 2nd frame of glider ie that the
            glider changed to second animate state

            @top: The row of top left corner of the location of original glider
            @left: The col of top left corner of the location of original glider
        """

        # Build the glider frame
        check = [[False] * self.gol.width()
                 for _ in range(self.gol.height())]
        check[top + 1][left] = False
        check[top + 1][left + 1] = False
        check[top + 1][left + 2] = True
        check[top + 2][left] = True
        check[top + 2][left + 1] = False
        check[top + 2][left + 2] = True
        check[top + 3][left] = False
        check[top + 3][left + 1] = True
        check[top + 3][left + 2] = True

        # Match entire current GoL board with the purpose built check array
        for row in range(self.gol.height()):
            for col in range(self.gol.width()):
                if self.gol._curr_state.get_state(row, col) != check[row][col]:
                    raise AssertionError('At (%i,%i) %r != %r' % (row, col, self.gol._curr_state.get_state(row, col), check[row][col]))

    def assertGliderFrame3(self, top, left):
        """ Assert current state matches the 3rd frame of glider ie that the
            glider changed to third animate state

            @top: The row of top left corner of the location of original glider
            @left: The col of top left corner of the location of original glider
        """

        # Build the glider frame
        check = [[False] * self.gol.width()
                 for _ in range(self.gol.height())]
        check[top + 1][left + 1] = True
        check[top + 1][left + 2] = False
        check[top + 1][left + 3] = False
        check[top + 2][left + 1] = False
        check[top + 2][left + 2] = True
        check[top + 2][left + 3] = True
        check[top + 3][left + 1] = True
        check[top + 3][left + 2] = True
        check[top + 3][left + 3] = False

        # Match entire current GoL board with the purpose built check array
        for row in range(self.gol.height()):
            for col in range(self.gol.width()):
                if self.gol._curr_state.get_state(row, col) != check[row][col]:
                    raise AssertionError('At (%i,%i) %r != %r' % (row, col, self.gol._curr_state.get_state(row, col), check[row][col]))

    def assertGliderFrame4(self, top, left):
        """ Assert current state matches the last frame of glider ie that the
            glider returned to original shape

            @top: The row to start building glider
            @left: The col to start building glider
        """

        # Build the glider frame
        check = [[False] * self.gol.width()
                 for _ in range(self.gol.height())]
        check[top + 1][left + 1] = False
        check[top + 1][left + 2] = True
        check[top + 1][left + 3] = False
        check[top + 2][left + 1] = False
        check[top + 2][left + 2] = False
        check[top + 2][left + 3] = True
        check[top + 3][left + 1] = True
        check[top + 3][left + 2] = True
        check[top + 3][left + 3] = True

        # Match entire current GoL board with the purpose built check array
        for row in range(self.gol.height()):
            for col in range(self.gol.width()):
                if self.gol._curr_state.get_state(row, col) != check[row][col]:
                    raise AssertionError('At (%i,%i) %r != %r' % (row, col, self.gol._curr_state.get_state(row, col), check[row][col]))

    def assertGoLBlock(self):
        # Check the block
        for i in range(1, 3):
            for j in range(1, 3):
                self.assertEqual(self.gol.is_alive(i, j), True)

        # Check the edges around block
        self.assertEqual(self.gol.is_alive(1, 0), False)
        self.assertEqual(self.gol.is_alive(1, 3), False)
        self.assertEqual(self.gol.is_alive(1, 4), False)
        self.assertEqual(self.gol.is_alive(1, 5), False)
        self.assertEqual(self.gol.is_alive(2, 0), False)
        self.assertEqual(self.gol.is_alive(2, 3), False)
        self.assertEqual(self.gol.is_alive(2, 4), False)
        self.assertEqual(self.gol.is_alive(2, 5), False)

        # Check the empty rows
        for i in range(6):
            self.assertEqual(self.gol.is_alive(0, i), False)
            self.assertEqual(self.gol.is_alive(3, i), False)
            self.assertEqual(self.gol.is_alive(4, i), False)
            self.assertEqual(self.gol.is_alive(5, i), False)


if __name__ == '__main__':
    unittest.main()
