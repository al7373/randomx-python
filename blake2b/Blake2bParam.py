from .const import BLAKE2B_SALTBYTES, BLAKE2B_PERSONALBYTES

class Blake2bParam:
    def __init__(self,
                 digest_length: int,
                 key_length: int,
                 fanout: int,
                 depth: int,
                 leaf_length: int,
                 node_offset: int,
                 node_depth: int,
                 inner_length: int,
                 reserved: bytearray = bytearray(14),
                 salt: bytearray = bytearray(BLAKE2B_SALTBYTES),
                 personal: bytearray = bytearray(BLAKE2B_PERSONALBYTES)):
        self.digest_length = digest_length
        self.key_length = key_length
        self.fanout = fanout
        self.depth = depth
        self.leaf_length = leaf_length
        self.node_offset = node_offset
        self.node_depth = node_depth
        self.inner_length = inner_length
        self.reserved = reserved
        self.salt = salt
        self.personal = personal

