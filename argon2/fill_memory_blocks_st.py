from .Argon2Instance import Argon2Instance
from .const import ARGON2_SYNC_POINTS, ARGON2_OK
from .Argon2Position import Argon2Position

def fill_memory_blocks_st(instance: Argon2Instance):
    for r in range(instance.passes):
        for s in range(ARGON2_SYNC_POINTS):
            for l in range(instance.lanes):
                position = Argon2Position(pass_=r, lane=l, slice_=s, index=0)
                # Fill the segment using the selected implementation
                instance.impl(instance, position)
    return ARGON2_OK

