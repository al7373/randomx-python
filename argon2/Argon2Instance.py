from typing import List, Callable
from .Argon2Context import Argon2Context
from .Block import Block
from .Argon2Type import Argon2Type

class Argon2Instance:
    def __init__(self, memory: List[Block], version: int, passes: int, memory_blocks: int,
                 segment_length: int, lane_length: int, lanes: int, threads: int,
                 argon2_type: Argon2Type, print_internals: int, context_ptr: Argon2Context,
                 randomx_argon2_impl: Callable):
        self.memory = memory
        self.version = version
        self.passes = passes
        self.memory_blocks = memory_blocks
        self.segment_length = segment_length
        self.lane_length = lane_length
        self.lanes = lanes
        self.threads = threads
        self.type = argon2_type
        self.print_internals = print_internals
        self.context_ptr = context_ptr
        self.impl = randomx_argon2_impl
 
