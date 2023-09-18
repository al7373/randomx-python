from .Blake2bState import Blake2bState

def blake2b_increment_counter(S: Blake2bState, inc: int):
    S.t[0] += inc
    S.t[1] += (S.t[0] < inc)

