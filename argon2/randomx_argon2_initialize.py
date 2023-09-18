
from .const import ARGON2_PREHASH_SEED_LENGTH, ARGON2_OK, ARGON2_INCORRECT_PARAMETER
from .Argon2Instance import Argon2Instance
from .Argon2Context import Argon2Context
from .rxa2_initial_hash import rxa2_initial_hash
from .rxa2_fill_first_blocks import rxa2_fill_first_blocks 

def randomx_argon2_initialize(instance: Argon2Instance, context: Argon2Context) -> int:
    blockhash = bytearray(ARGON2_PREHASH_SEED_LENGTH)

    result = ARGON2_OK

    if instance is None or context is None:
        return ARGON2_INCORRECT_PARAMETER
    instance.context_ptr = context

    # 1. Initial hashing
    # H_0 + 8 extra bytes to produce the first blocks
    # uint8_t blockhash[ARGON2_PREHASH_SEED_LENGTH];
    # Hashing all inputs
    rxa2_initial_hash(blockhash, context, instance.type)

    # 2. Creating first blocks, we always have at least two blocks in a slice
    rxa2_fill_first_blocks(blockhash, instance)

    return ARGON2_OK

