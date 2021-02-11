import unittest
from test_minmax import TestMinMax

def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestMinMax))
    return test_suite

mySuit = suite()

runner = unittest.TextTestRunner()
runner.run(mySuit)


