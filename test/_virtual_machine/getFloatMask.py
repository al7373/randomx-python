import unittest
from virtual_machine.getFloatMask import getFloatMask 

class TestGetFloatMask(unittest.TestCase):

    def test_getFloatMask(self):
        self.assertEqual(getFloatMask(9713811302651988593), 4035225266128095857)
        self.assertEqual(getFloatMask(17049312405384313502), 4467570830353087134)

