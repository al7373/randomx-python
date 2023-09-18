
cdef extern from "common.hpp" namespace "randomx":  # replace with the correct header file
    ctypedef unsigned long long int_reg_t

    cdef struct fpu_reg_t:
        double lo
        double hi

    cdef int RegistersCount = 8 
    cdef int RegisterCountFlt = 4

    cdef struct RegisterFile:
        int_reg_t r[8]
        fpu_reg_t f[4]
        fpu_reg_t e[4]
        fpu_reg_t a[4]

    int sizeof_RegisterFile "sizeof(randomx::RegisterFile)"

cdef extern from "dataset.hpp":
    ctypedef unsigned char uint8_t
    cdef struct randomx_dataset:
        uint8_t* memory
        void (*dealloc)()

cdef extern from "vm_interpreted.hpp" namespace "randomx":
    cdef cppclass InterpretedVmDefault:
        InterpretedVmDefault() 
        void run(void* seed)
        void setDataset(randomx_dataset* dataset)
        void initScratchpad(void* seed)
        void allocate()
        RegisterFile* getRegisterFile()
        const void* getScratchpad()
        void getFinalResult(void* out, size_t outSize)

