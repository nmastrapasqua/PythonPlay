import unittest
from games.connect_four import ConnectFourGame, NONE

RED = 'R'
YELLOW = 'Y'

class TestConnectFourClass(unittest.TestCase):

    def setUp(self):
        self.game = ConnectFourGame(RED, YELLOW)
    
    def test_is_moves_left(self):
        self.assertEqual(self.game.is_moves_left(), True)

    def test_valid_moves(self):
        expected = [0, 1, 2, 3 , 4, 5, 6]
        moves = self.game.valid_moves()
        self.assertListEqual(moves, expected)

        for i in range (6):
            self.game.do_move(0, RED)
        expected = [1, 2, 3 , 4, 5, 6]
        moves = self.game.valid_moves()
        self.assertListEqual(moves, expected)

        self.game.do_move(1, YELLOW)
        moves = self.game.valid_moves()
        self.assertListEqual(moves, expected)

        for i in range (5):
            self.game.do_move(1, YELLOW)
        expected = [2, 3 , 4, 5, 6]
        moves = self.game.valid_moves()
        self.assertListEqual(moves, expected)

        for i in range (6):
            self.game.do_move(4, RED)
        expected = [2, 3 , 5, 6]
        moves = self.game.valid_moves()
        self.assertListEqual(moves, expected)

    def test_undo(self):
        self.game.do_move(4, RED)

        board = self.game.get_board()
        self.assertEqual(board[4][5], RED)

        self.game.undo()
        self.assertEqual(board[4][5], NONE)


if __name__ == '__main__':
    unittest.main()