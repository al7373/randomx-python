from .Block import Block
from .const import ARGON2_QWORDS_IN_BLOCK
from blake2b.BLAKE2_ROUND_NOMSG import BLAKE2_ROUND_NOMSG

def copy_block(dst: Block, src: Block):
    dst.v = src.v.copy()

def xor_block(dst: Block, src: Block):
    for i in range(ARGON2_QWORDS_IN_BLOCK):
        dst.v[i] ^= src.v[i]

def fill_block(prev_block: Block, ref_block: Block, next_block: Block, with_xor: bool) -> None:
    blockR = Block(ref_block.v.copy())
    xor_block(blockR, prev_block)
    block_tmp = Block(blockR.v.copy())

    if with_xor:
        xor_block(block_tmp, next_block)

    # Apply Blake2 on columns of 64-bit words
    for i in range(8):
        results = BLAKE2_ROUND_NOMSG(
            blockR.v[16 * i], blockR.v[16 * i + 1], blockR.v[16 * i + 2], blockR.v[16 * i + 3],
            blockR.v[16 * i + 4], blockR.v[16 * i + 5], blockR.v[16 * i + 6], blockR.v[16 * i + 7],
            blockR.v[16 * i + 8], blockR.v[16 * i + 9], blockR.v[16 * i + 10], blockR.v[16 * i + 11],
            blockR.v[16 * i + 12], blockR.v[16 * i + 13], blockR.v[16 * i + 14], blockR.v[16 * i + 15]
        )
        blockR.v[16 * i:16 * (i + 1)] = list(results)

    # Apply Blake2 on rows of 64-bit words
    for i in range(8):
        results = BLAKE2_ROUND_NOMSG(
            blockR.v[2 * i], blockR.v[2 * i + 1], blockR.v[2 * i + 16], blockR.v[2 * i + 17],
            blockR.v[2 * i + 32], blockR.v[2 * i + 33], blockR.v[2 * i + 48], blockR.v[2 * i + 49],
            blockR.v[2 * i + 64], blockR.v[2 * i + 65], blockR.v[2 * i + 80], blockR.v[2 * i + 81],
            blockR.v[2 * i + 96], blockR.v[2 * i + 97], blockR.v[2 * i + 112], blockR.v[2 * i + 113]
        )
        blockR.v[2 * i], blockR.v[2 * i + 1], blockR.v[2 * i + 16], blockR.v[2 * i + 17], \
        blockR.v[2 * i + 32], blockR.v[2 * i + 33], blockR.v[2 * i + 48], blockR.v[2 * i + 49], \
        blockR.v[2 * i + 64], blockR.v[2 * i + 65], blockR.v[2 * i + 80], blockR.v[2 * i + 81], \
        blockR.v[2 * i + 96], blockR.v[2 * i + 97], blockR.v[2 * i + 112], blockR.v[2 * i + 113] = results

    copy_block(next_block, block_tmp)
    xor_block(next_block, blockR)

