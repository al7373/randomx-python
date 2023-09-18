from .Argon2Instance import Argon2Instance
from .const import ARGON2_BLOCK_SIZE, ARGON2_PREHASH_DIGEST_LENGTH, ARGON2_PREHASH_SEED_LENGTH
from blake2b.store32 import store32
from .load_block import load_block
from blake2b.blake2b_long import blake2b_long

def rxa2_fill_first_blocks(blockhash: bytearray, instance: Argon2Instance):
    blockhash_bytes = bytearray(ARGON2_BLOCK_SIZE)
    
    for l in range(instance.lanes):
        # Générer le premier bloc (G(H0||0||i)) pour chaque voie
        store32(blockhash, ARGON2_PREHASH_DIGEST_LENGTH, 0)
        store32(blockhash, ARGON2_PREHASH_DIGEST_LENGTH + 4, l)
        blake2b_long(blockhash_bytes, ARGON2_BLOCK_SIZE, blockhash, ARGON2_PREHASH_SEED_LENGTH)
        load_block(instance.memory[l * instance.lane_length], blockhash_bytes)

        # Générer le deuxième bloc (G(H0||1||i)) pour chaque voie
        store32(blockhash, ARGON2_PREHASH_DIGEST_LENGTH, 1)
        blake2b_long(blockhash_bytes, ARGON2_BLOCK_SIZE, blockhash, ARGON2_PREHASH_SEED_LENGTH)
        load_block(instance.memory[l * instance.lane_length + 1], blockhash_bytes)

