from .Blake2bState import Blake2bState
from .blake2b_set_lastblock import blake2b_set_lastblock 

def blake2b_invalidate_state(S: Blake2bState):
    blake2b_set_lastblock(S)  # invalidate for further use

