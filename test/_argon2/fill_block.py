import unittest
from argon2.Block import Block
from argon2.const import ARGON2_QWORDS_IN_BLOCK
from argon2.fill_block import copy_block, xor_block, fill_block
import os

class TestFillBlock(unittest.TestCase):

    def load_block_from_file(self, filename):
        with open(filename, "rb") as f:
            data = f.read()
        return Block.from_bytes(data)

    def test_fill_block(self):
        # Créer des blocs pour le test
        current_dir = os.path.dirname(os.path.abspath(__file__))

        prev_block_filename = os.path.join(current_dir, 'example_of_blocks', 'prev_block_dump.bin')
        ref_block_filename = os.path.join(current_dir, 'example_of_blocks', 'ref_block_dump.bin')
        next_block_filename = os.path.join(current_dir, 'example_of_blocks', 'next_block_dump.bin')

        prev_block = self.load_block_from_file(prev_block_filename)
        ref_block = self.load_block_from_file(ref_block_filename)
        next_block = Block([0] * ARGON2_QWORDS_IN_BLOCK)
        next_block_expected = self.load_block_from_file(next_block_filename)

        # Remplir le bloc next_block
        fill_block(prev_block, ref_block, next_block, with_xor=False)

        # Comparer le résultat avec le bloc attendu
        self.assertEqual(next_block.v, next_block_expected.v)


