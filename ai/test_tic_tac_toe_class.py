import unittest
from tic_tac_toe_game import TicTacToeGame

class TestTicTacToeClass(unittest.TestCase):

    def test_evaluate(self):
        game = TicTacToeGame('X', 'O', 2)
        game.do_move(0, True)
        #self.assertEqual(game.evaluate(True), 30)
        #self.assertEqual(game.evaluate(False), -30)
        game.do_move(4, True)
        #self.assertEqual(game.evaluate(True), 150)
        #self.assertEqual(game.evaluate(False), -150)
        game.do_move(8, True)
        #self.assertEqual(game.evaluate(True), 1070)
        #self.assertEqual(game.evaluate(False), -1070)

        game.undo()
        game.undo()
        game.undo()

        game.do_move(0, False)
        game.do_move(4, True)
        game.do_move(3, False)
        game.do_move(2, True)
        game.maximizing_turn(False)
        print(f"TRUE {game.evaluate(True)}")
        print(f"FALSE {game.evaluate(False)}")


    def test_valid_moves(self):
        game = TicTacToeGame('X', 'O', 2)
        moves = game.valid_moves()
        expected = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.assertListEqual(moves, expected)
        
        game.do_move(2, False)
        moves = game.valid_moves()
        expected = [0, 1, 3, 4, 5, 6, 7, 8]
        self.assertListEqual(moves, expected)

        game.do_move(8, True)
        moves = game.valid_moves()
        expected = [0, 1, 3, 4, 5, 6, 7]
        self.assertListEqual(moves, expected)

    def test_is_moves_left(self):
        game = TicTacToeGame('X', 'O', 2)
        self.assertEqual(game.is_moves_left(), True)

        game.do_move(0, True)
        self.assertEqual(game.is_moves_left(), True)

        for i in range(1, 9):
            self.assertEqual(game.is_moves_left(), True)
            game.do_move(i, True)

        self.assertEqual(game.is_moves_left(), False)

    def test_undo(self):
        game = TicTacToeGame('X', 'O', 2)
        game.do_move(0, True)
        moves = game.valid_moves()
        expected = [1, 2, 3, 4, 5, 6, 7, 8]
        self.assertListEqual(moves, expected)

        game.undo()
        expected = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        moves = game.valid_moves()
        self.assertListEqual(moves, expected)

        game.do_move(0, True)
        game.do_move(1, True)
        game.do_move(2, True)
        moves = game.valid_moves()
        expected = [3, 4, 5, 6, 7, 8]
        self.assertListEqual(moves, expected)

        game.undo()
        moves = game.valid_moves()
        expected = [2, 3, 4, 5, 6, 7, 8]
        self.assertListEqual(moves, expected)

        game.undo()
        moves = game.valid_moves()
        expected = [1, 2, 3, 4, 5, 6, 7, 8]
        self.assertListEqual(moves, expected)

        game.undo()
        moves = game.valid_moves()
        expected = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.assertListEqual(moves, expected)

    def test_check_win(self):
        game = TicTacToeGame('X', 'O', 2)
        game.do_move(0, True)
        game.do_move(4, True)
        game.do_move(8, True)
        self.assertEqual(game.check_win(True), True)
        self.assertEqual(game.check_win(False), False)

        game.undo()
        self.assertEqual(game.check_win(True), False)
        self.assertEqual(game.check_win(False), False)

    @unittest.expectedFailure
    def test_not_allowed_move(self):
        game = TicTacToeGame('X', 'O', 2)
        game.do_move(0, True)
        game.do_move(0, False)



