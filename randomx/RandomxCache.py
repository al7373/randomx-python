from typing import List, Callable, Union
from .configuration import RANDOMX_CACHE_ACCESSES 
from superscalar.SuperscalarProgram import SuperscalarProgram

class RandomxCache:
    def __init__(self):
        self.memory = None
        self.dealloc: Callable = None
        self.jit = None
        self.initialize: Callable = None
        self.datasetInit: Callable = None
        self.programs = [SuperscalarProgram()] * RANDOMX_CACHE_ACCESSES  # Remplacez RANDOMX_CACHE_ACCESSES par sa valeur définie
        self.reciprocalCache: List[int] = []
        self.cacheKey: str = ''
        self.argonImpl: Callable = None

    def isInitialized(self) -> bool:
        return self.programs[0].getSize() != 0

