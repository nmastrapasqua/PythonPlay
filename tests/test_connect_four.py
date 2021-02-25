import unittest
from games.connect_four import ConnectFourGame, EMPTY, RED, YELLOW



class TestConnectFourClass(unittest.TestCase):

    def setUp(self):
        self.game = ConnectFourGame(RED, YELLOW)
    
    def test_is_moves_left(self):
        self.assertEqual(self.game.is_moves_left(), True)

        for row in range(0, 6):
            for col in range (0, 7):
                self.game.do_move(col, RED)

        self.assertEqual(self.game.is_moves_left(), False)

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
        self.assertEqual(board[0][4], RED)

        self.game.undo()
        self.assertEqual(board[0][4], EMPTY)

        self.game.do_move(4, RED)
        self.game.do_move(5, RED)
        self.game.do_move(6, YELLOW)
        self.game.do_move(6, YELLOW)
        self.assertEqual(board[0][4], RED)
        self.assertEqual(board[0][5], RED)
        self.assertEqual(board[0][6], YELLOW)
        self.assertEqual(board[1][6], YELLOW)

        for i in range(3):
            self.game.undo()

        self.assertEqual(board[0][4], RED)
        self.assertEqual(board[0][5], EMPTY)
        self.assertEqual(board[0][6], EMPTY)
        self.assertEqual(board[1][6], EMPTY)

        self.game.undo()
        self.assertEqual(board[0][4], EMPTY)

    def test_get_winner(self):
        self.game.do_move(0, RED)
        self.game.do_move(0, RED)
        self.game.do_move(0, RED)
        self.game.do_move(0, RED)
        self.assertEqual(self.game.check_win(RED), True)
        self.assertEqual(self.game.check_win(YELLOW), False)

        for i in range(4):
            self.game.undo()
        
        self.assertEqual(self.game.check_win(RED), False)
        self.assertEqual(self.game.check_win(YELLOW), False)

        for i in range(0, 4):
            self.game.do_move(i, YELLOW)

        self.assertEqual(self.game.check_win(RED), False)
        self.assertEqual(self.game.check_win(YELLOW), True)

        for i in range(4):
            self.game.undo()
        
        self.assertEqual(self.game.check_win(RED), False)
        self.assertEqual(self.game.check_win(YELLOW), False)

        self.game.do_move(0, YELLOW)
        self.game.do_move(1, YELLOW)
        self.game.do_move(1, YELLOW)
        self.game.do_move(2, YELLOW)
        self.game.do_move(2, YELLOW)
        self.game.do_move(2, YELLOW)

        self.game.do_move(3, RED)
        self.game.do_move(3, RED)
        self.game.do_move(3, RED)
        self.game.do_move(3, YELLOW)

        self.assertEqual(self.game.check_win(RED), False)
        self.assertEqual(self.game.check_win(YELLOW), True)

if __name__ == '__main__':
    unittest.main()