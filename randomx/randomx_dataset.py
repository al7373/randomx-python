from typing import List
import struct
from .const import CacheLineSize

class randomx_dataset:
    def __init__(self):
        self.memory: Union[bytearray, None] = None

def datasetRead(dataset_memory: bytearray, blockNumber: int, out: List[int]):
    # Calculer le nombre d'entiers de 64 bits
    n = CacheLineSize // 8
    # Convertir le bytearray en entiers non signés de 64 bits
    out[:] = list(struct.unpack('<' + 'Q'*n, dataset_memory[blockNumber:blockNumber+CacheLineSize]))
    """
    for i in range(len(out)):
        addr = blockNumber + (i * 8)
        out[i] = int.from_bytes(
            # le 8 (8 octets), c'est parce que out[i] attend un entier de 64 bit (entier non signé)
            # 8(bit/octet) * 8(octet) = 64bits
            dataset_memory[addr:addr+8], 
            byteorder='little'
        )
    """

