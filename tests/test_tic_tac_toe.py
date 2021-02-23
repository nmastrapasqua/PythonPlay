import unittest
from games.tic_tac_toe import TicTacToeGame, SimpleMiniMaxPlayer
from games.game import RandomPlayer, Match, DRAW

class TestTicTacToeClass(unittest.TestCase):

    def setUp(self):
        minMaxplayer = SimpleMiniMaxPlayer('X')
        self.playerId = minMaxplayer.get_id()
        self.opponentId = RandomPlayer('O').get_id()
        self.game = TicTacToeGame(self.playerId, self.opponentId)
        self.eval = minMaxplayer.evaluate

    def test_evaluate(self):
        
        self.game.do_move(0, self.playerId)
        self.game.do_move(4, self.playerId)
        self.game.do_move(8, self.playerId)
        self.assertEqual(self.eval(self.game, 0), 10)
        self.assertEqual(self.eval(self.game, 2), 8)
        
        self.game.undo()
        self.game.undo()
        self.game.undo()
        self.assertEqual(self.eval(self.game, 0), 0)
        self.assertEqual(self.eval(self.game, 2), 0)

        self.game.do_move(0, self.opponentId)
        self.game.do_move(1, self.opponentId)
        self.game.do_move(2, self.opponentId)
        self.assertEqual(self.eval(self.game, 0), -10)
        self.assertEqual(self.eval(self.game, 2), -8)

    def test_valid_moves(self):
        moves = self.game.valid_moves()
        expected = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.assertListEqual(moves, expected)
        
        self.game.do_move(2, self.opponentId)
        moves = self.game.valid_moves()
        expected = [0, 1, 3, 4, 5, 6, 7, 8]
        self.assertListEqual(moves, expected)

        self.game.do_move(8, self.playerId)
        moves = self.game.valid_moves()
        expected = [0, 1, 3, 4, 5, 6, 7]
        self.assertListEqual(moves, expected)

    def test_is_moves_left(self):
        self.assertEqual(self.game.is_moves_left(), True)

        self.game.do_move(0, self.playerId)
        self.assertEqual(self.game.is_moves_left(), True)

        for i in range(1, 9):
            self.assertEqual(self.game.is_moves_left(), True)
            self.game.do_move(i, self.playerId)

        self.assertEqual(self.game.is_moves_left(), False)

    def test_undo(self):
        self.game.do_move(0, self.playerId)
        moves = self.game.valid_moves()
        expected = [1, 2, 3, 4, 5, 6, 7, 8]
        self.assertListEqual(moves, expected)

        self.game.undo()
        expected = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        moves = self.game.valid_moves()
        self.assertListEqual(moves, expected)

        self.game.do_move(0, self.playerId)
        self.game.do_move(1, self.playerId)
        self.game.do_move(2, self.playerId)
        moves = self.game.valid_moves()
        expected = [3, 4, 5, 6, 7, 8]
        self.assertListEqual(moves, expected)

        self.game.undo()
        moves = self.game.valid_moves()
        expected = [2, 3, 4, 5, 6, 7, 8]
        self.assertListEqual(moves, expected)

        self.game.undo()
        moves = self.game.valid_moves()
        expected = [1, 2, 3, 4, 5, 6, 7, 8]
        self.assertListEqual(moves, expected)

        self.game.undo()
        moves = self.game.valid_moves()
        expected = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.assertListEqual(moves, expected)

    def test_check_win(self):
        self.game.do_move(0, self.playerId)
        self.game.do_move(4, self.playerId)
        self.game.do_move(8, self.playerId)
        self.assertEqual(self.game.check_win(self.playerId), True)
        self.assertEqual(self.game.check_win(self.opponentId), False)

        self.game.undo()
        self.assertEqual(self.game.check_win(self.playerId), False)
        self.assertEqual(self.game.check_win(self.opponentId), False)

    def test_ai_vs_ai(self):
        player1 = SimpleMiniMaxPlayer('X')
        player2 = SimpleMiniMaxPlayer('O')

        game = TicTacToeGame(player1.get_id(), player2.get_id())

        match = Match(game, player1, player2)
        outcome = match.run()

        self.assertEqual(outcome, DRAW)

    def test_ai_vs_random(self):
        player1 = SimpleMiniMaxPlayer('X')
        player2 = RandomPlayer('O')

        game = TicTacToeGame(player1.get_id(), player2.get_id())

        match = Match(game, player1, player2)
        outcome = match.run()

        self.assertFalse(outcome == player2.get_id())

    @unittest.expectedFailure
    def test_not_allowed_move(self):
        self.game.do_move(0, self.playerId)
        self.game.do_move(0, self.opponentId)

if __name__ == '__main__':
    unittest.main()
