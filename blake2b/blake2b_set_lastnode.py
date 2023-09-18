from .Blake2bState import Blake2bState 

def blake2b_set_lastnode(S: Blake2bState):
    S.f[1] = (1 << 64) - 1

