import unittest
from blake2b.Blake2Generator import Blake2Generator
from superscalar.RegisterInfo import RegisterInfo
from superscalar.selectRegister import selectRegister

class TestSelectRegister(unittest.TestCase):

    def test_selectRegister(self):
        seed = b"12345678901234567890123456789012"
        gen = Blake2Generator(seed, len(seed))

        registers = [RegisterInfo() for _ in range(8)]
        available_registers = [0, 1, 2, 3, 4, 5, 6, 7]

        selected_register = selectRegister(available_registers, gen, registers)
        self.assertEqual(selected_register, 6)

    def test_selectRegister_utility(self):
        seed = bytearray(b"test_seed_for_select_register")
        gen = Blake2Generator(seed, len(seed))

        available_registers = [0, 1, 2, 3]
        registers = [RegisterInfo() for _ in range(8)]

        # Test si selectRegister retourne un registre disponible
        selected_register = selectRegister(available_registers, gen, registers)
        self.assertEqual(selected_register, 0)
        self.assertIn(selected_register, available_registers, "Le registre sélectionné doit être dans les registres disponibles")


