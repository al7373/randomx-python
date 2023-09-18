from .SuperscalarInstructionType import SuperscalarInstructionType 

class DecoderBuffer:
    decode_buffers = []
    default = None

    def __init__(self, name=None, index=None, counts=None):
        self.name_ = name
        self.index_ = index
        self.counts_ = counts
        self.opsCount_ = len(counts) if counts is not None else 0

    def get_counts(self):
        return self.counts_

    def get_size(self):
        return self.opsCount_

    def get_index(self):
        return self.index_

    def get_name(self):
        return self.name_

    def fetch_next(self, instr_type, cycle, mul_count, gen):
        if instr_type == SuperscalarInstructionType.IMULH_R or instr_type == SuperscalarInstructionType.ISMULH_R:
            return DecoderBuffer.decode_buffer3310

        if mul_count < cycle + 1:
            return DecoderBuffer.decode_buffer4444

        if instr_type == SuperscalarInstructionType.IMUL_RCP:
            return DecoderBuffer.decode_buffer484 if gen.get_byte() & 1 else DecoderBuffer.decode_buffer493

        return self.fetch_next_default(gen)

    def fetch_next_default(self, gen):
        return DecoderBuffer.decode_buffers[gen.get_byte() & 3]

buffer0 = [4, 8, 4]
buffer1 = [7, 3, 3, 3]
buffer2 = [3, 7, 3, 3]
buffer3 = [4, 9, 3]
buffer4 = [4, 4, 4, 4]
buffer5 = [3, 3, 10]

DecoderBuffer.decode_buffer484 = DecoderBuffer("4,8,4", 0, buffer0)
DecoderBuffer.decode_buffer7333 = DecoderBuffer("7,3,3,3", 1, buffer1)
DecoderBuffer.decode_buffer3733 = DecoderBuffer("3,7,3,3", 2, buffer2)
DecoderBuffer.decode_buffer493 = DecoderBuffer("4,9,3", 3, buffer3)
DecoderBuffer.decode_buffer4444 = DecoderBuffer("4,4,4,4", 4, buffer4)
DecoderBuffer.decode_buffer3310 = DecoderBuffer("3,3,10", 5, buffer5)

DecoderBuffer.decode_buffers = [
    DecoderBuffer.decode_buffer484,
    DecoderBuffer.decode_buffer7333,
    DecoderBuffer.decode_buffer3733,
    DecoderBuffer.decode_buffer493,
]

DecoderBuffer.default = DecoderBuffer()

