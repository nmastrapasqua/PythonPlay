import unittest
from games.connect_four import ConnectFourGame, MiniMaxPlayer, EMPTY, AI_PIECE, PLAYER_PIECE



class TestConnectFourClass(unittest.TestCase):

    def setUp(self):
        self.game = ConnectFourGame(AI_PIECE, PLAYER_PIECE)
        self.aiPlayer = MiniMaxPlayer(AI_PIECE)
    
    def test_is_moves_left(self):
        self.assertEqual(self.game.is_moves_left(), True)

        for row in range(0, 6):
            for col in range (0, 7):
                self.game.do_move(col, AI_PIECE)

        self.assertEqual(self.game.is_moves_left(), False)

    def test_valid_moves(self):
        expected = [0, 1, 2, 3 , 4, 5, 6]
        moves = self.game.valid_moves()
        self.assertListEqual(moves, expected)

        for i in range (6):
            self.game.do_move(0, AI_PIECE)
        expected = [1, 2, 3 , 4, 5, 6]
        moves = self.game.valid_moves()
        self.assertListEqual(moves, expected)

        self.game.do_move(1, PLAYER_PIECE)
        moves = self.game.valid_moves()
        self.assertListEqual(moves, expected)

        for i in range (5):
            self.game.do_move(1, PLAYER_PIECE)
        expected = [2, 3 , 4, 5, 6]
        moves = self.game.valid_moves()
        self.assertListEqual(moves, expected)

        for i in range (6):
            self.game.do_move(4, AI_PIECE)
        expected = [2, 3 , 5, 6]
        moves = self.game.valid_moves()
        self.assertListEqual(moves, expected)

    def test_undo(self):
        self.game.do_move(4, AI_PIECE)

        board = self.game.get_board()
        self.assertEqual(board[0][4], AI_PIECE)

        self.game.undo()
        self.assertEqual(board[0][4], EMPTY)

        self.game.do_move(4, AI_PIECE)
        self.game.do_move(5, AI_PIECE)
        self.game.do_move(6, PLAYER_PIECE)
        self.game.do_move(6, PLAYER_PIECE)
        self.assertEqual(board[0][4], AI_PIECE)
        self.assertEqual(board[0][5], AI_PIECE)
        self.assertEqual(board[0][6], PLAYER_PIECE)
        self.assertEqual(board[1][6], PLAYER_PIECE)

        for i in range(3):
            self.game.undo()

        self.assertEqual(board[0][4], AI_PIECE)
        self.assertEqual(board[0][5], EMPTY)
        self.assertEqual(board[0][6], EMPTY)
        self.assertEqual(board[1][6], EMPTY)

        self.game.undo()
        self.assertEqual(board[0][4], EMPTY)

    def test_get_winner(self):
        self.game.do_move(0, AI_PIECE)
        self.game.do_move(0, AI_PIECE)
        self.game.do_move(0, AI_PIECE)
        self.game.do_move(0, AI_PIECE)
        self.assertEqual(self.game.check_win(AI_PIECE), True)
        self.assertEqual(self.game.check_win(PLAYER_PIECE), False)

        for i in range(4):
            self.game.undo()
        
        self.assertEqual(self.game.check_win(AI_PIECE), False)
        self.assertEqual(self.game.check_win(PLAYER_PIECE), False)

        for i in range(0, 4):
            self.game.do_move(i, PLAYER_PIECE)

        self.assertEqual(self.game.check_win(AI_PIECE), False)
        self.assertEqual(self.game.check_win(PLAYER_PIECE), True)

        for i in range(4):
            self.game.undo()
        
        self.assertEqual(self.game.check_win(AI_PIECE), False)
        self.assertEqual(self.game.check_win(PLAYER_PIECE), False)

        self.game.do_move(0, PLAYER_PIECE)
        self.game.do_move(1, PLAYER_PIECE)
        self.game.do_move(1, PLAYER_PIECE)
        self.game.do_move(2, PLAYER_PIECE)
        self.game.do_move(2, PLAYER_PIECE)
        self.game.do_move(2, PLAYER_PIECE)

        self.game.do_move(3, AI_PIECE)
        self.game.do_move(3, AI_PIECE)
        self.game.do_move(3, AI_PIECE)
        self.game.do_move(3, PLAYER_PIECE)

        self.assertEqual(self.game.check_win(AI_PIECE), False)
        self.assertEqual(self.game.check_win(PLAYER_PIECE), True)

        for i in range(10):
            self.game.undo()

        self.assertEqual(self.game.check_win(AI_PIECE), False)
        self.assertEqual(self.game.check_win(PLAYER_PIECE), False)

        self.game.do_move(6, PLAYER_PIECE)
        self.game.do_move(6, PLAYER_PIECE)
        self.game.do_move(6, PLAYER_PIECE)
        self.game.do_move(6, AI_PIECE)

        self.game.do_move(5, PLAYER_PIECE)
        self.game.do_move(5, PLAYER_PIECE)
        self.game.do_move(5, AI_PIECE)

        self.game.do_move(4, PLAYER_PIECE)
        self.game.do_move(4, AI_PIECE)

        self.game.do_move(3, AI_PIECE)

        self.assertEqual(self.game.check_win(AI_PIECE), True)
        self.assertEqual(self.game.check_win(PLAYER_PIECE), False)

    def test_evaluate(self):
        self.assertEqual(self.aiPlayer.evaluate(self.game, 0), 0)

        self.game.do_move(3, self.aiPlayer.get_id())
        self.assertEqual(self.aiPlayer.evaluate(self.game, 0), 7)
        self.game.do_move(3, self.aiPlayer.get_id())
        self.assertEqual(self.aiPlayer.evaluate(self.game, 0), 17)

        self.game.undo()
        self.game.undo()

        self.game.do_move(6, AI_PIECE)
        self.game.do_move(6, AI_PIECE)
        self.game.do_move(6, AI_PIECE)
        self.game.do_move(6, PLAYER_PIECE)

        self.game.do_move(5, AI_PIECE)
        self.game.do_move(5, AI_PIECE)
        self.game.do_move(5, PLAYER_PIECE)

        self.game.do_move(4, AI_PIECE)
        self.game.do_move(4, PLAYER_PIECE)

        self.game.do_move(2, AI_PIECE)
        self.game.do_move(2, AI_PIECE)

        self.assertEqual(self.aiPlayer.evaluate(self.game, 0), 13)

if __name__ == '__main__':
    unittest.main()