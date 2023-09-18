cimport cpp_vm

from randomx.randomx_dataset import randomx_dataset as _randomx_dataset

from cpython.buffer cimport Py_buffer, PyBUF_SIMPLE, PyObject_GetBuffer, PyBuffer_Release

from randomx.RegisterFile import RegisterFile as PyRegisterFile 

from randomx.const import ScratchpadSize

cdef class cpp_vm:

    cdef InterpretedVmDefault* _thisptr
    cdef randomx_dataset _dataset

    def __cinit__(self):
        self._thisptr = new InterpretedVmDefault()

    def __dealloc__(self):
        del self._thisptr

    def setDataset(self, dataset: _randomx_dataset) -> None:
        cdef Py_buffer view
        if PyObject_GetBuffer(dataset.memory, &view, PyBUF_SIMPLE) != 0:
            raise ValueError("Could not get buffer")
        self._dataset.memory = <uint8_t*> view.buf
        self._thisptr.setDataset(&self._dataset)
        PyBuffer_Release(&view)

    def initScratchpad(self, seed: bytearray) -> None:
        cdef Py_buffer view
        if PyObject_GetBuffer(seed, &view, PyBUF_SIMPLE) != 0:
            raise ValueError("Could not get buffer")
        cdef void* _seed = view.buf
        self._thisptr.initScratchpad(_seed)
        PyBuffer_Release(&view)

    def allocate(self) -> None:
        self._thisptr.allocate()

    def run(self, seed: bytearray):
        cdef Py_buffer view
        if PyObject_GetBuffer(seed, &view, PyBUF_SIMPLE) != 0:
            raise ValueError("Could not get buffer")
        cdef void* _seed = view.buf
        self._thisptr.run(_seed)
        PyBuffer_Release(&view)

    def getRegisterFile(self) -> PyRegisterFile:
        reg = PyRegisterFile()

        cdef RegisterFile* _reg = self._thisptr.getRegisterFile()
        cdef uint8_t* byte_ptr = <uint8_t*> _reg
        cdef bytes b = bytes(byte_ptr[i] for i in range(sizeof_RegisterFile))

        reg.from_bytes(b)

        return reg

    def getScratchpad(self) -> bytes:
        cdef const uint8_t* byte_ptr = <const uint8_t*>self._thisptr.getScratchpad()
        cdef bytes b = bytes(byte_ptr[i] for i in range(ScratchpadSize))

        return b

    @property
    def scratchpad(self) -> bytes:
        return self.getScratchpad()

    def getFinalResult(self, out: bytearray, outSize: int):
        cdef char* ptr
        cdef Py_buffer view

        PyObject_GetBuffer(out, &view, PyBUF_SIMPLE)

        ptr = <char*> view.buf

        self._thisptr.getFinalResult(ptr, outSize)

        PyBuffer_Release(&view)

