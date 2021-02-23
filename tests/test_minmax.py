import unittest
from tests.test_game import get_tree_1_game, get_tree_2_game, get_tree_3_game, get_tree_4_game
from tests.test_game import get_tree_5_game, get_tree_6_game

class TestMinMax(unittest.TestCase):

    def test_tree_1(self):
        game, expected_score, expected_move, player = get_tree_1_game()
        score, move = player.do_move(game)
        self.assertEqual(score, expected_score)
        self.assertEqual(move, expected_move)

    def test_tree_2(self):
        game, expected_score, expected_move, player = get_tree_2_game()
        score, move = player.do_move(game)
        self.assertEqual(score, expected_score)
        self.assertEqual(move, expected_move)

    def test_tree_3(self):
        game, expected_score, expected_move, player = get_tree_3_game()
        score, move = player.do_move(game)
        self.assertEqual(score, expected_score)
        self.assertEqual(move, expected_move)

    def test_tree_4(self):
        game, expected_score, expected_move, player = get_tree_4_game()
        score, move = player.do_move(game)
        self.assertEqual(score, expected_score)
        self.assertEqual(move, expected_move)

    def test_tree_5(self):
        game, expected_score, expected_move, player = get_tree_5_game()
        score, move = player.do_move(game)
        self.assertEqual(score, expected_score)
        self.assertEqual(move, expected_move)

    def test_tree_6(self):
        game, expected_score, expected_move, player = get_tree_6_game()
        score, move = player.do_move(game)
        self.assertEqual(score, expected_score)
        self.assertEqual(move, expected_move)

if __name__ == '__main__':
    unittest.main()