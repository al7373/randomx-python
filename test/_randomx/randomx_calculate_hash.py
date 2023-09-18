import unittest
from randomx.randomx_calculate_hash import randomx_calculate_hash
from randomx.randomx_dataset import randomx_dataset
from vm_interpreted.InterpretedVm import InterpretedVm 
from cpp_vm.cpp_vm import cpp_vm 
import os
import timeit

class TestRandomxCalculateHash(unittest.TestCase):

    def test_randomx_calculate_hash(self):

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset_dump.bin'), 'rb') as f:
            data = f.read()

        dataset = randomx_dataset()
        dataset.memory = data

        machine = InterpretedVm()

        machine.setDataset(dataset)

        start_time = timeit.default_timer()

        _hash = bytearray(32)

        myInput = bytes([
            0x52,	0x61,	0x6e,	0x64,	0x6f,	0x6d,	0x58,	0x20,
            0x65,	0x78,	0x61,	0x6d,	0x70,	0x6c,	0x65,	0x20,
            0x69,	0x6e,	0x70,	0x75,	0x74,	0x00
        ])

        randomx_calculate_hash(machine, myInput, len(myInput), _hash)

        end_time = timeit.default_timer()

        execution_time = end_time - start_time

        print(f"randomx_calculate_hash execution_time: {execution_time} seconds")

    def test_randomx_calculate_hash_cpp_vm(self):

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset_dump.bin'), 'rb') as f:
            data = f.read()

        dataset = randomx_dataset()
        dataset.memory = data

        machine = cpp_vm()

        machine.setDataset(dataset)

        machine.allocate()

        start_time = timeit.default_timer()

        _hash = bytearray(32)

        myInput = bytes([
            0x52,	0x61,	0x6e,	0x64,	0x6f,	0x6d,	0x58,	0x20,
            0x65,	0x78,	0x61,	0x6d,	0x70,	0x6c,	0x65,	0x20,
            0x69,	0x6e,	0x70,	0x75,	0x74,	0x00
        ])

        randomx_calculate_hash(machine, myInput, len(myInput), _hash)

        end_time = timeit.default_timer()

        execution_time = end_time - start_time

        print(f"randomx_calculate_hash_cpp_vm execution_time: {execution_time} seconds")

        self.assertEqual(_hash.hex(), "8a48e5f9db45ab79d9080574c4d81954fe6ac63842214aff73c244b26330b7c9")

