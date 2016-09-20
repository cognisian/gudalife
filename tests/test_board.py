import unittest
from gudalife.board import GudaLifeDict, GudaLifeBoard


class TestGudaLifeDict(unittest.TestCase):
    def setUp(self):
        self.board = GudaLifeDict(3, 3)

    def test_set_alive(self):
        self.board.set_state(1, 1, True)
        self.assertEqual(self.board.get_state(1, 1), True)

    def test_set_dead(self):
        # Set everything to alive
        for row in range(0, 3):
            for col in range(0, 3):
                self.board.set_state(row, col, True)

        # Set test condition
        self.board.set_state(1, 1, False)

        self.assertEqual(self.board.get_state(1, 1), False)

    def test_get_neighbours(self):
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


class TestGudaLifeBoard(unittest.TestCase):
    def setUp(self):
        self.gol = GudaLifeBoard(3, 3, print)

    def test_update_alive_2(self):
        # Set 2 neighbour cell to be alive
        self.gol.alive(0, 0)
        self.gol.alive(2, 2)

        # Check if center cell will be alive next turn
        alive = self.gol.will_be_alive(1, 1)

        self.assertEqual(alive, True)

    def test_update_alive_3(self):
        # Set 3 neighbour cell to be alive
        self.gol.alive(0, 0)
        self.gol.alive(0, 2)
        self.gol.alive(2, 2)

        # Check if center cell will be alive next turn
        alive = self.gol.will_be_alive(1, 1)

        self.assertEqual(alive, True)

    def test_update_dead_1(self):
        # Set 1 neighbour cell to be alive
        self.gol.alive(0, 0)

        # Check if center cell will be alive next turn
        self.gol.will_be_alive(1, 1)

        self.assertEqual(self.gol.is_alive(1, 1), False)

    def test_update_dead_4(self):
        # Set 4 neighbour cell to be alive
        self.gol.alive(0, 0)
        self.gol.alive(0, 1)
        self.gol.alive(0, 2)
        self.gol.alive(2, 0)

        # Check if center cell will be alive next turn
        self.gol.will_be_alive(1, 1)

        self.assertEqual(self.gol.is_alive(1, 1), False)


if __name__ == '__main__':
    unittest.main()
