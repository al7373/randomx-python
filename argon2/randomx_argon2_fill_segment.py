from typing import List
from .Block import Block
from .Argon2Instance import Argon2Instance
from .Argon2Position import Argon2Position
from .const import ARGON2_VERSION_10 
from .randomx_argon2_index_alpha import randomx_argon2_index_alpha 
from .fill_block import fill_block 

def randomx_argon2_fill_segment(instance: Argon2Instance, position: Argon2Position) -> None:
    ref_block: Block = None
    curr_block: Block = None
    address_block = Block([0] * 128)
    input_block = Block([0] * 128)
    zero_block = Block([0] * 128)
    pseudo_rand: int
    ref_index: int
    ref_lane: int
    prev_offset: int
    curr_offset: int
    starting_index: int
    i: int

    if instance is None:
        return

    starting_index = 0

    if position.pass_ == 0 and position.slice_ == 0:
        starting_index = 2  # we have already generated the first two blocks

    # Offset of the current block
    curr_offset = position.lane * instance.lane_length + position.slice_ * instance.segment_length + starting_index

    if curr_offset % instance.lane_length == 0:
        # Last block in this lane
        prev_offset = curr_offset + instance.lane_length - 1
    else:
        # Previous block
        prev_offset = curr_offset - 1

    for i in range(starting_index, instance.segment_length):
        # 1.1 Rotating prev_offset if needed
        if curr_offset % instance.lane_length == 1:
            prev_offset = curr_offset - 1

        # 1.2 Computing the index of the reference block
        # 1.2.1 Taking pseudo-random value from the previous block
        pseudo_rand = instance.memory[prev_offset].v[0]

        # 1.2.2 Computing the lane of the reference block
        ref_lane = (pseudo_rand >> 32) % instance.lanes

        if position.pass_ == 0 and position.slice_ == 0:
            # Can not reference other lanes yet
            ref_lane = position.lane

        # 1.2.3 Computing the number of possible reference block within the lane
        position = position._replace(index=i)
        ref_index = randomx_argon2_index_alpha(instance, position, pseudo_rand & 0xFFFFFFFF, ref_lane == position.lane)

        # 2 Creating a new block
        ref_block = instance.memory[instance.lane_length * ref_lane + ref_index]
        curr_block = instance.memory[curr_offset]

        if ARGON2_VERSION_10 == instance.version:
            # version 1.2.1 and earlier: overwrite, not XOR
            fill_block(instance.memory[prev_offset], ref_block, curr_block, 0)
        else:
            if position.pass_ == 0:
                fill_block(instance.memory[prev_offset], ref_block, curr_block, 0)
            else:
                fill_block(instance.memory[prev_offset], ref_block, curr_block, 1)

        curr_offset += 1
        prev_offset += 1

