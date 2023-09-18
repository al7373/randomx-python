from .rx_vec_i128 import rx_set_int_vec_i128, rx_load_vec_i128, rx_store_vec_i128
from .soft_aesdec import soft_aesdec
from .soft_aesenc import soft_aesenc

AES_HASH_1R_STATE0 = (0xd7983aad, 0xcc82db47, 0x9fa856de, 0x92b52c0d)
AES_HASH_1R_STATE1 = (0xace78057, 0xf59e125a, 0x15c7b798, 0x338d996e)
AES_HASH_1R_STATE2 = (0xe8a07ce4, 0x5079506b, 0xae62c7d0, 0x6a770017)
AES_HASH_1R_STATE3 = (0x7e994948, 0x79a10005, 0x07ad828d, 0x630a240c)

AES_HASH_1R_XKEY0 = (0x06890201, 0x90dc56bf, 0x8b24949f, 0xf6fa8389)
AES_HASH_1R_XKEY1 = (0xed18f99b, 0xee1043c6, 0x51f4e03c, 0x61b263d1)

def hashAes1Rx4(_input: bytearray, inputSize: int, _hash: bytearray) -> None:
    assert len(_input) % 64 == 0
    inptr = 0
    inputEnd = inputSize

    state0 = rx_set_int_vec_i128(*AES_HASH_1R_STATE0)
    state1 = rx_set_int_vec_i128(*AES_HASH_1R_STATE1)
    state2 = rx_set_int_vec_i128(*AES_HASH_1R_STATE2)
    state3 = rx_set_int_vec_i128(*AES_HASH_1R_STATE3)

    # process 64 bytes at a time in 4 lanes
    while inptr < inputEnd:
        in0 = rx_load_vec_i128(_input[inptr : inptr+16])
        in1 = rx_load_vec_i128(_input[inptr+16 : inptr+32])
        in2 = rx_load_vec_i128(_input[inptr+32 : inptr+48])
        in3 = rx_load_vec_i128(_input[inptr+48 : inptr+64])

        state0 = soft_aesenc(state0, in0)
        state1 = soft_aesdec(state1, in1)
        state2 = soft_aesenc(state2, in2)
        state3 = soft_aesdec(state3, in3)

        inptr += 64

    # two extra rounds to achieve full diffusion
    xkey0 = rx_set_int_vec_i128(*AES_HASH_1R_XKEY0)
    xkey1 = rx_set_int_vec_i128(*AES_HASH_1R_XKEY1)

    state0 = soft_aesenc(state0, xkey0)
    state1 = soft_aesdec(state1, xkey0)
    state2 = soft_aesenc(state2, xkey0)
    state3 = soft_aesdec(state3, xkey0)

    state0 = soft_aesenc(state0, xkey1)
    state1 = soft_aesdec(state1, xkey1)
    state2 = soft_aesenc(state2, xkey1)
    state3 = soft_aesdec(state3, xkey1)

    # output hash
    rx_store_vec_i128(_hash, 0, state0)
    rx_store_vec_i128(_hash, 16, state1)
    rx_store_vec_i128(_hash, 32, state2)
    rx_store_vec_i128(_hash, 48, state3)

