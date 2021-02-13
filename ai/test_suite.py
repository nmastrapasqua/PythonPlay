import unittest
from test_minmax import TestMinMax
from test_tic_tac_toe_class import TestTicTacToeClass

def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestMinMax))
    #test_suite.addTest(unittest.makeSuite(TestTicTacToeClass))
    return test_suite

mySuit = suite()

runner = unittest.TextTestRunner()
runner.run(mySuit)


