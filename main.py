from superscalar.SuperscalarProgram import SuperscalarProgram
from blake2b.Blake2Generator import Blake2Generator
from superscalar.generateSuperscalar import generateSuperscalar
import struct
from randomx.configuration import RANDOMX_CACHE_ACCESSES 

def main():

    key = "test key 000"
    key_size = len(key)
    keyInBytes = key.encode('utf-8')

    programs = [SuperscalarProgram()] * RANDOMX_CACHE_ACCESSES

    gen = Blake2Generator(keyInBytes, key_size)

    for i in range(RANDOMX_CACHE_ACCESSES):
        generateSuperscalar(programs[i], gen)
        prog = programs[i]

if __name__ == "__main__":
    main()

