from .Argon2Type import Argon2Type
from .Argon2Context import Argon2Context
from .const import ARGON2_PREHASH_DIGEST_LENGTH

from blake2b.blake2b_init import blake2b_init
from blake2b.blake2b_update import blake2b_update
from blake2b.blake2b_final import blake2b_final
from blake2b.Blake2bState import Blake2bState
from blake2b.store32 import store32

def rxa2_initial_hash(blockhash: bytearray, context: Argon2Context, argon2_type: Argon2Type):
    BlakeHash = Blake2bState()
    value = bytearray(4)

    if context is None or blockhash is None:
        return

    blake2b_init(BlakeHash, ARGON2_PREHASH_DIGEST_LENGTH)

    store32(value, 0, context.lanes)
    blake2b_update(BlakeHash, value, len(value))

    store32(value, 0, context.outlen)
    blake2b_update(BlakeHash, value, len(value))

    store32(value, 0, context.m_cost)
    blake2b_update(BlakeHash, value, len(value))

    store32(value, 0, context.t_cost)
    blake2b_update(BlakeHash, value, len(value))

    store32(value, 0, context.version)
    blake2b_update(BlakeHash, value, len(value))

    store32(value, 0, argon2_type.value)
    blake2b_update(BlakeHash, value, len(value))

    store32(value, 0, context.pwdlen)
    blake2b_update(BlakeHash, value, len(value))

    if context.pwd is not None:
        blake2b_update(BlakeHash, context.pwd, context.pwdlen)

    store32(value, 0, context.saltlen)
    blake2b_update(BlakeHash, value, len(value))

    if context.salt is not None:
        blake2b_update(BlakeHash, context.salt, context.saltlen)

    store32(value, 0, context.secretlen)
    blake2b_update(BlakeHash, value, len(value))

    if context.secret is not None:
        blake2b_update(BlakeHash, context.secret, context.secretlen)

    store32(value, 0, context.adlen)
    blake2b_update(BlakeHash, value, len(value))

    if context.ad is not None:
        blake2b_update(BlakeHash, context.ad, context.adlen)

    blake2b_final(BlakeHash, blockhash, ARGON2_PREHASH_DIGEST_LENGTH)

