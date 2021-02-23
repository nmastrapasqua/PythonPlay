import unittest
from tests.test_minmax import TestMinMax
from tests.test_tic_tac_toe import TestTicTacToeClass
from tests.test_connect_four import TestConnectFourClass
import sys

def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    #print(f'sys.path = {sys.path}')
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestMinMax))
    test_suite.addTest(unittest.makeSuite(TestTicTacToeClass))
    test_suite.addTest(unittest.makeSuite(TestConnectFourClass))
    return test_suite

mySuit = suite()

runner = unittest.TextTestRunner()
runner.run(mySuit)


