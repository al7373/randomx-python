from .configuration import RANDOMX_SUPERSCALAR_LATENCY, RANDOMX_ARGON_SALT, RANDOMX_ARGON_MEMORY, RANDOMX_SCRATCHPAD_L3, RANDOMX_DATASET_BASE_SIZE, RANDOMX_DATASET_EXTRA_SIZE, RANDOMX_SCRATCHPAD_L3, RANDOMX_SCRATCHPAD_L2, RANDOMX_SCRATCHPAD_L1, RANDOMX_JUMP_BITS, RANDOMX_JUMP_OFFSET

sizeof_int_reg_t = 8
ScratchpadL1 = RANDOMX_SCRATCHPAD_L1 // sizeof_int_reg_t
ScratchpadL2 = RANDOMX_SCRATCHPAD_L2 // sizeof_int_reg_t
ScratchpadL3 = RANDOMX_SCRATCHPAD_L3 // sizeof_int_reg_t
ScratchpadL1Mask = (ScratchpadL1 - 1) * 8
ScratchpadL2Mask = (ScratchpadL2 - 1) * 8
ScratchpadL1Mask16 = (ScratchpadL1 // 2 - 1) * 16
ScratchpadL2Mask16 = (ScratchpadL2 // 2 - 1) * 16
ScratchpadL3Mask = (ScratchpadL3 - 1) * 8
ScratchpadL3Mask64 = (ScratchpadL3 // 8 - 1) * 64

RegistersCount = 8
RegisterNeedsDisplacement = 5

CYCLE_MAP_SIZE = RANDOMX_SUPERSCALAR_LATENCY + 4

SuperscalarMaxSize = 3 * RANDOMX_SUPERSCALAR_LATENCY + 2;

LOOK_FORWARD_CYCLES = 4

MAX_THROWAWAY_COUNT = 256

# en C c'est correct, main Python non
# ArgonSaltSize = len(RANDOMX_ARGON_SALT) - 1
# voici ce qui est correct en Python
ArgonSaltSize = len(RANDOMX_ARGON_SALT)

ArgonBlockSize = 1024
RANDOMX_DATASET_ITEM_SIZE = 64
CacheSize = RANDOMX_ARGON_MEMORY * ArgonBlockSize
CacheLineSize = RANDOMX_DATASET_ITEM_SIZE
CacheLineAlignMask = (RANDOMX_DATASET_BASE_SIZE - 1) & ~(CacheLineSize - 1)

DatasetExtraItems = RANDOMX_DATASET_EXTRA_SIZE // RANDOMX_DATASET_ITEM_SIZE
ConditionMask = ((1 << RANDOMX_JUMP_BITS) - 1);
ConditionOffset = RANDOMX_JUMP_OFFSET;
StoreL3Condition = 14

superscalarMul0 = 6364136223846793005
superscalarAdd1 = 9298411001130361340
superscalarAdd2 = 12065312585734608966
superscalarAdd3 = 9306329213124626780
superscalarAdd4 = 5281919268842080866
superscalarAdd5 = 10536153434571861004
superscalarAdd6 = 3398623926847679864
superscalarAdd7 = 9549104520008361294

AES_GEN_1R_KEY0 = (0xb4f44917, 0xdbb5552b, 0x62716609, 0x6daca553)
AES_GEN_1R_KEY1 = (0x0da1dc4e, 0x1725d378, 0x846a710d, 0x6d7caf07)
AES_GEN_1R_KEY2 = (0x3e20e345, 0xf4c0794f, 0x9f947ec6, 0x3f1262f1)
AES_GEN_1R_KEY3 = (0x49169154, 0x16314c88, 0xb1ba317c, 0x6aef8135)

ScratchpadSize = RANDOMX_SCRATCHPAD_L3

AES_GEN_4R_KEY0 = (0x99e5d23f, 0x2f546d2b, 0xd1833ddb, 0x6421aadd)
AES_GEN_4R_KEY1 = (0xa5dfcde5, 0x06f79d53, 0xb6913f55, 0xb20e3450)
AES_GEN_4R_KEY2 = (0x171c02bf, 0x0aa4679f, 0x515e7baf, 0x5c3ed904)
AES_GEN_4R_KEY3 = (0xd8ded291, 0xcd673785, 0xe78f5d08, 0x85623763)
AES_GEN_4R_KEY4 = (0x229effb4, 0x3d518b6d, 0xe3d6a7a6, 0xb5826f73)
AES_GEN_4R_KEY5 = (0xb272b7d2, 0xe9024d4e, 0x9c10b3d9, 0xc7566bf3)
AES_GEN_4R_KEY6 = (0xf63befa7, 0x2ba9660a, 0xf765a38b, 0xf273c9e7)
AES_GEN_4R_KEY7 = (0xc0b0762d, 0x0c06d1fd, 0x915839de, 0x7a7cd609)

exponentSize = 11
mantissaSize = 52
mantissaMask = (1 << mantissaSize) - 1
exponentMask = (1 << exponentSize) - 1
exponentBias = 1023
constExponentBits = 0x300
dynamicExponentBits = 4
staticExponentBits = 4

RegistersCount = 8
RegisterCountFlt = RegistersCount // 2

mantissaSize = 52
dynamicExponentBits = 4
dynamicMantissaMask = (1 << (mantissaSize + dynamicExponentBits)) - 1

RANDOMX_HASH_SIZE = 32

