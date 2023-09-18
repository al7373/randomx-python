from .Blake2bState import Blake2bState
from .blake2b_set_lastnode import blake2b_set_lastnode

def blake2b_set_lastblock(S: Blake2bState):
    if hasattr(S, 'last_node') and S.last_node:
        blake2b_set_lastnode(S)
    S.f[0] = (1 << 64) - 1

