from .const import AES_GEN_4R_KEY0, AES_GEN_4R_KEY1, AES_GEN_4R_KEY2, AES_GEN_4R_KEY3, AES_GEN_4R_KEY4, AES_GEN_4R_KEY5, AES_GEN_4R_KEY6, AES_GEN_4R_KEY7
from .rx_vec_i128 import rx_vec_i128, rx_set_int_vec_i128, rx_load_vec_i128, rx_store_vec_i128
from .soft_aesdec import soft_aesdec
from .soft_aesenc import soft_aesenc
import struct

def fillAes4Rx4(state: bytearray, outputSize: int, buf: bytearray) -> None:
    assert outputSize % 64 == 0
    outptr = 0
    outputEnd = outputSize

    key0 = rx_set_int_vec_i128(*AES_GEN_4R_KEY0)
    key1 = rx_set_int_vec_i128(*AES_GEN_4R_KEY1)
    key2 = rx_set_int_vec_i128(*AES_GEN_4R_KEY2)
    key3 = rx_set_int_vec_i128(*AES_GEN_4R_KEY3)
    key4 = rx_set_int_vec_i128(*AES_GEN_4R_KEY4)
    key5 = rx_set_int_vec_i128(*AES_GEN_4R_KEY5)
    key6 = rx_set_int_vec_i128(*AES_GEN_4R_KEY6)
    key7 = rx_set_int_vec_i128(*AES_GEN_4R_KEY7)

    state0 = rx_load_vec_i128(state[0:16])
    state1 = rx_load_vec_i128(state[16:32])
    state2 = rx_load_vec_i128(state[32:48])
    state3 = rx_load_vec_i128(state[48:64])

    while outptr < outputEnd:
        state0 = soft_aesdec(state0, key0)
        state1 = soft_aesenc(state1, key0)
        state2 = soft_aesdec(state2, key4)
        state3 = soft_aesenc(state3, key4)

        state0 = soft_aesdec(state0, key1)
        state1 = soft_aesenc(state1, key1)
        state2 = soft_aesdec(state2, key5)
        state3 = soft_aesenc(state3, key5)

        state0 = soft_aesdec(state0, key2)
        state1 = soft_aesenc(state1, key2)
        state2 = soft_aesdec(state2, key6)
        state3 = soft_aesenc(state3, key6)

        state0 = soft_aesdec(state0, key3)
        state1 = soft_aesenc(state1, key3)
        state2 = soft_aesdec(state2, key7)
        state3 = soft_aesenc(state3, key7)

        rx_store_vec_i128(buf, outptr, state0)
        rx_store_vec_i128(buf, outptr+16, state1)
        rx_store_vec_i128(buf, outptr+32, state2)
        rx_store_vec_i128(buf, outptr+48, state3)

        outptr += 64

    rx_store_vec_i128(state, 0, state0)
    rx_store_vec_i128(state, 16, state1)
    rx_store_vec_i128(state, 32, state2)
    rx_store_vec_i128(state, 48, state3)

