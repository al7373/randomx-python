from .const import ARGON2_INCORRECT_PARAMETER
from .fill_memory_blocks_st import fill_memory_blocks_st 
from .Argon2Instance import Argon2Instance

def randomx_argon2_fill_memory_blocks(instance: Argon2Instance):
    if instance is None or instance.lanes == 0:
        return ARGON2_INCORRECT_PARAMETER
    return fill_memory_blocks_st(instance)

