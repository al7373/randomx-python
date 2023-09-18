from .Block import Block
from .const import ARGON2_QWORDS_IN_BLOCK
from blake2b.load64 import load64

def load_block(dst: Block, input: bytes):
    for i in range(ARGON2_QWORDS_IN_BLOCK):
        dst.v[i] = load64(input[i * 8:i * 8 + 8])

