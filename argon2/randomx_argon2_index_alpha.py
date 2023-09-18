from typing import Tuple
from .Argon2Instance import Argon2Instance
from .Argon2Position import Argon2Position
from .const import ARGON2_SYNC_POINTS

def randomx_argon2_index_alpha(instance: Argon2Instance, position: Argon2Position, pseudo_rand: int, same_lane: int) -> int:
    if position.pass_ == 0:
        # First pass
        if position.slice_ == 0:
            # First slice
            reference_area_size = position.index - 1  # all but the previous
        else:
            if same_lane:
                # The same lane => add current segment
                reference_area_size = position.slice_ * instance.segment_length + position.index - 1
            else:
                reference_area_size = position.slice_ * instance.segment_length + (-1 if position.index == 0 else 0)
    else:
        # Second pass
        if same_lane:
            reference_area_size = instance.lane_length - instance.segment_length + position.index - 1
        else:
            reference_area_size = instance.lane_length - instance.segment_length + (-1 if position.index == 0 else 0)

    # Mapping pseudo_rand to 0..<reference_area_size-1> and produce relative position
    relative_position = pseudo_rand
    relative_position = (relative_position * relative_position) >> 32
    relative_position = reference_area_size - 1 - (reference_area_size * relative_position >> 32)

    # Computing starting position
    start_position = 0

    if position.pass_ != 0:
        start_position = 0 if (position.slice_ == ARGON2_SYNC_POINTS - 1) else (position.slice_ + 1) * instance.segment_length

    # Computing absolute position
    absolute_position = (start_position + relative_position) % instance.lane_length

    return absolute_position

