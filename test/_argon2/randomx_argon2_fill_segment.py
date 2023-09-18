import unittest
from argon2.rxa2_fill_first_blocks import rxa2_fill_first_blocks
from argon2.randomx_argon2_fill_segment import randomx_argon2_fill_segment
from argon2.rxa2_initial_hash import rxa2_initial_hash
from argon2.Argon2Type import Argon2Type
from argon2.Argon2Position import Argon2Position 
from argon2.const import ARGON2_PREHASH_SEED_LENGTH, ARGON2_SYNC_POINTS
import os
import hashlib
from .create_argon2_instance import create_argon2_instance


class TestRandomxArgon2FillSegment(unittest.TestCase):

    def test_argon2_instance_memory(self):
        instance, context = create_argon2_instance()

        blockhash = bytearray(ARGON2_PREHASH_SEED_LENGTH)

        rxa2_initial_hash(blockhash, context, Argon2Type.Argon2_d)

        rxa2_fill_first_blocks(blockhash, instance)

        # Appeler la fonction randomx_argon2_fill_segment pour chaque passe, voie et point de synchronisation
        for r in range(instance.passes):
            for s in range(ARGON2_SYNC_POINTS):
                for l in range(instance.lanes):
                    position = Argon2Position(r, l, s, 0)
                    randomx_argon2_fill_segment(instance, position)

        # Générer le hash SHA-256 du contenu du memory de l'instance
        memory_hash = hashlib.sha256()
        for block in instance.memory:
            memory_hash.update(block.to_bytes())

        # Charger le contenu de memory_1.bin
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'memory_1.bin'), 'rb') as f:
            memory_file_content = f.read()

        # Générer le hash SHA-256 du contenu de memory_file.txt
        memory_file_hash = hashlib.sha256(memory_file_content)

        # Comparer les deux hashes
        self.assertEqual(memory_hash.digest(), memory_file_hash.digest())


