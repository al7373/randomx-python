import numpy as np
from typing import List
from .Block import Block
from .Argon2Instance import Argon2Instance
from .const import ARGON2_QWORDS_IN_BLOCK 

def save_memory_to_file(argon2_instance: Argon2Instance, file_path: str) -> None:
    memory = argon2_instance.memory

    # Créez un tableau numpy vide avec la taille appropriée pour stocker tous les éléments de la mémoire.
    memory_array = np.empty(len(memory) * ARGON2_QWORDS_IN_BLOCK, dtype=np.uint64)

    # Copiez les éléments de la mémoire dans le tableau numpy.
    for i, block in enumerate(memory):
        for j, value in enumerate(block.v):
            memory_array[i * ARGON2_QWORDS_IN_BLOCK + j] = value

    # Enregistrez le contenu du tableau numpy dans un fichier binaire.
    memory_array.tofile(file_path)

