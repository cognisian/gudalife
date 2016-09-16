import unittest
from gudalife.board import GudaLifeBoard


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = GudaLifeBoard(3, 3)

    def test_set_alive(self):
        self.board.alive(1, 1)
        self.assertEqual(self.board.is_alive(1, 1), True)

    def test_set_dead(self):
        # Set everything to alive
        for row in range(0, 3):
            for col in range(0, 3):
                self.board.alive(row, col)

        # Set test condition
        self.board.dead(1, 1)

        self.assertEqual(self.board.is_alive(1, 1), False)

    def test_update_alive_2(self):
        # Set 2 neighbour cell to be alive
        self.board.alive(0, 0)
        self.board.alive(2, 2)

        # Check if center cell will be alive next turn
        alive = self.board.will_be_alive(1, 1)

        self.assertEqual(alive, True)

    def test_update_alive_3(self):
        # Set 3 neighbour cell to be alive
        self.board.alive(0, 0)
        self.board.alive(0, 2)
        self.board.alive(2, 2)

        # Check if center cell will be alive next turn
        alive = self.board.will_be_alive(1, 1)

        self.assertEqual(alive, True)

    def test_update_dead_1(self):
        # Set 1 neighbour cell to be alive
        self.board.alive(0, 0)

        # Check if center cell will be alive next turn
        self.board.will_be_alive(1, 1)

        self.assertEqual(self.board.is_alive(1, 1), False)

    def test_update_dead_4(self):
        # Set 4 neighbour cell to be alive
        self.board.alive(0, 0)
        self.board.alive(0, 1)
        self.board.alive(0, 2)
        self.board.alive(2, 0)

        # Check if center cell will be alive next turn
        self.board.will_be_alive(1, 1)

        self.assertEqual(self.board.is_alive(1, 1), False)


if __name__ == '__main__':
    unittest.main()
