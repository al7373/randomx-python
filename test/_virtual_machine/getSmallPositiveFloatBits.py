import unittest
from virtual_machine.getSmallPositiveFloatBits import getSmallPositiveFloatBits 

class TestGetSmallPositiveFloatBits(unittest.TestCase):

    def test_getSmallPositiveFloatBits(self):
        self.assertEqual(getSmallPositiveFloatBits(18221569025469959029), 4746798940377434997)
        self.assertEqual(getSmallPositiveFloatBits(6540525175208166347), 4658020530967299019)
        self.assertEqual(getSmallPositiveFloatBits(11284897593959090804), 4696131339116055156)
        self.assertEqual(getSmallPositiveFloatBits(1859849227501142954), 4625059398706627498)
        self.assertEqual(getSmallPositiveFloatBits(5759946197137768062), 4652060688804626046)
        self.assertEqual(getSmallPositiveFloatBits(8426952128535686356), 4670950039308692692)
        self.assertEqual(getSmallPositiveFloatBits(15435530889885022921), 4725970975997983433)
        self.assertEqual(getSmallPositiveFloatBits(17706436732194723147), 4745077004622435659)

