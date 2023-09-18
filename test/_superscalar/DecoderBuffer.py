import unittest
from blake2b.Blake2Generator import Blake2Generator
from superscalar.SuperscalarInstructionType import SuperscalarInstructionType
from superscalar.DecoderBuffer import DecoderBuffer  

class TestDecoderBuffer(unittest.TestCase):

    def test_initialization(self):
        db = DecoderBuffer("4,8,4", 0, [4, 8, 4])
        self.assertEqual(db.get_name(), "4,8,4")
        self.assertEqual(db.get_index(), 0)
        self.assertEqual(db.get_counts(), [4, 8, 4])
        self.assertEqual(db.get_size(), 3)

    def test_fetch_next(self):
        # Créez une instance de Blake2Generator avec des données de test
        seed_data = bytes([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        gen = Blake2Generator(seed_data, len(seed_data))

        buffer = DecoderBuffer.default

        next_buffer = buffer.fetch_next(SuperscalarInstructionType.IMUL_R, 1, 1, gen)
        self.assertEqual(next_buffer.get_name(), '4,4,4,4')
        self.assertEqual(next_buffer.get_index(), 4)
        self.assertEqual(next_buffer.get_size(), 4)
        self.assertEqual(next_buffer.get_counts(), [4,4,4,4])

        next_buffer = buffer.fetch_next(SuperscalarInstructionType.IMUL_RCP, 1, 1, gen)
        self.assertEqual(next_buffer.get_name(), '4,4,4,4')
        self.assertEqual(next_buffer.get_index(), 4)
        self.assertEqual(next_buffer.get_size(), 4)
        self.assertEqual(next_buffer.get_counts(), [4,4,4,4])

        next_buffer = buffer.fetch_next(SuperscalarInstructionType.IMULH_R, 1, 1, gen)
        self.assertEqual(next_buffer.get_name(), '3,3,10')
        self.assertEqual(next_buffer.get_index(), 5)
        self.assertEqual(next_buffer.get_size(), 3)
        self.assertEqual(next_buffer.get_counts(), [3,3,10])

        next_buffer = buffer.fetch_next(SuperscalarInstructionType.ISMULH_R, 1, 1, gen)
        self.assertEqual(next_buffer.get_name(), '3,3,10')
        self.assertEqual(next_buffer.get_index(), 5)
        self.assertEqual(next_buffer.get_size(), 3)
        self.assertEqual(next_buffer.get_counts(), [3,3,10])


