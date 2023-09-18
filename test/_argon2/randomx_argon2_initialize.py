import unittest
import os
import hashlib
from .create_argon2_instance import create_argon2_instance 
from argon2.randomx_argon2_initialize import randomx_argon2_initialize

class TestRandomxArgon2Initialize(unittest.TestCase):

    def test_argon2_instance_memory(self):

        instance, context = create_argon2_instance()

        randomx_argon2_initialize(instance, context)

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

