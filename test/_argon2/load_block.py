import unittest
from typing import List
from argon2.load_block import load_block
from argon2.const import ARGON2_QWORDS_IN_BLOCK, ARGON2_BLOCK_SIZE 
from argon2.Block import Block
from blake2b.load64 import load64

class TestLoadBlock(unittest.TestCase):

    def test_load_block(self):
        # Définir les valeurs de test
        input_string = b'This is a test input string for load_block function. Please ensure it is long enough!'
        input_data = input_string * (ARGON2_BLOCK_SIZE // len(input_string))

        # Générer les valeurs attendues
        expected_values = []
        for i in range(0, ARGON2_BLOCK_SIZE, 8):
            value = load64(input_data[i:i+8])
            expected_values.append(value)

        # Créer un bloc vide
        block = Block([0 for _ in range(ARGON2_QWORDS_IN_BLOCK)])

        # Appeler la fonction load_block
        load_block(block, input_data)

        # Vérifier si les valeurs sont correctes
        self.assertEqual(block.v, expected_values)

