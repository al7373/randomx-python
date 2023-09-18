import unittest
from superscalar.SuperscalarProgram import SuperscalarProgram
from randomx.const import SuperscalarMaxSize 

class TestSuperscalarProgram(unittest.TestCase):

    def test_program_buffer(self):
        sp = SuperscalarProgram()

        # Test the program buffer size
        self.assertEqual(len(sp.programBuffer), SuperscalarMaxSize)

    def test_set_size(self):
        sp = SuperscalarProgram()
        sp.setSize(4)

        self.assertEqual(sp.getSize(), 4)

    def test_set_address_register(self):
        sp = SuperscalarProgram()
        sp.setAddressRegister(3)

        self.assertEqual(sp.getAddressRegister(), 3)

    def test_call(self):
        sp = SuperscalarProgram()
        sp.setSize(1)

        # Test accessing the first instruction in the program buffer
        self.assertIsNotNone(sp(0))
