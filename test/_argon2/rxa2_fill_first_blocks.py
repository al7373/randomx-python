import unittest
from argon2.rxa2_fill_first_blocks import rxa2_fill_first_blocks 
from argon2.rxa2_initial_hash import rxa2_initial_hash  
from argon2.Argon2Instance import Argon2Instance 
from argon2.Argon2Context import Argon2Context 
from argon2.Argon2Type import Argon2Type   
from argon2.Block import Block
from argon2.const import ARGON2_PREHASH_SEED_LENGTH, ARGON2_PREHASH_SEED_LENGTH, ARGON2_SYNC_POINTS, ARGON2_QWORDS_IN_BLOCK
import os
import hashlib
from .create_argon2_instance import create_argon2_instance


class TestRxa2FillFirstBlocks(unittest.TestCase):

    def test_rxa2_fill_first_blocks(self):
        # Initialisation des valeurs
        blockhash = bytearray(ARGON2_PREHASH_SEED_LENGTH)
        memory_blocks = 8
        lane_length = memory_blocks // ARGON2_SYNC_POINTS
        lanes = 2

        # Remplir 'blockhash' avec des valeurs arbitraires pour les besoins du test
        for i in range(ARGON2_PREHASH_SEED_LENGTH):
            blockhash[i] = i % 256

        # Créer une instance d'Argon2 avec des valeurs par défaut
        memory = [Block([0] * ARGON2_QWORDS_IN_BLOCK) for _ in range(memory_blocks * lanes)]

        instance = Argon2Instance(
            memory=memory,
            version=0x13,
            passes=3,
            memory_blocks=memory_blocks,
            segment_length=memory_blocks // (lanes * ARGON2_SYNC_POINTS),
            lane_length=lane_length,
            lanes=lanes,
            threads=1,
            argon2_type=None,
            print_internals=0,
            context_ptr=None,
            randomx_argon2_impl=None
        )

        # Appeler la fonction rxa2_fill_first_blocks
        rxa2_fill_first_blocks(blockhash, instance)

        # Vérifier si les premiers blocs de chaque voie sont correctement remplis
        for l in range(lanes):
            first_block = instance.memory[l * lane_length]
            second_block = instance.memory[l * lane_length + 1]

            # Vérifiez que les blocs ne sont pas vides
            self.assertTrue(any(first_block.v))
            self.assertTrue(any(second_block.v))

            # Vérifiez que les blocs ne sont pas identiques
            self.assertNotEqual(first_block.v, second_block.v)

    def test_argon2_instance_memory(self):
        instance, context = create_argon2_instance()

        blockhash = bytearray(ARGON2_PREHASH_SEED_LENGTH)

        rxa2_initial_hash(blockhash, context, Argon2Type.Argon2_d)

        rxa2_fill_first_blocks(blockhash, instance)

        # Générer le hash SHA-256 du contenu du memory de l'instance
        memory_hash = hashlib.sha256()
        for block in instance.memory:
            memory_hash.update(block.to_bytes())

        # Charger le contenu de memory_file.txt
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'memory.bin'), 'rb') as f:
            memory_file_content = f.read()

        # Générer le hash SHA-256 du contenu de memory_file.txt
        memory_file_hash = hashlib.sha256(memory_file_content)

        # Comparer les deux hashes
        self.assertEqual(memory_hash.digest(), memory_file_hash.digest())

