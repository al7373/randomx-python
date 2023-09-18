import unittest
from vm_interpreted.InterpretedVm import InterpretedVm
import os
from randomx.randomx_dataset import randomx_dataset
from blake2b.blake2b import blake2b

class TestInterpretedVm(unittest.TestCase):

    def test_run(self):

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../_randomx/dataset_dump.bin'), 'rb') as f:
            data = f.read()

        dataset = randomx_dataset()
        dataset.memory = data

        machine = InterpretedVm()

        machine.setDataset(dataset)

        tempHash = bytearray(64)

        in_data = bytes([
            0x52,	0x61,	0x6e,	0x64,	0x6f,	0x6d,	0x58,	0x20,
            0x65,	0x78,	0x61,	0x6d,	0x70,	0x6c,	0x65,	0x20,
            0x69,	0x6e,	0x70,	0x75,	0x74,	0x00
        ])

        blakeResult = blake2b(tempHash, len(tempHash), in_data, len(in_data), None, 0)

        machine.initScratchpad(tempHash)

        expectedTempHash = bytearray([
            0x84,	0x90,	0x6b,	0x48,	0xbd,	0x9f,	0x8c,	0xbf,
            0x62,	0xf5,	0xa0,	0x8a,	0xbc,	0xc4,	0x65,	0x82,
            0x76,	0x8c,	0x31,	0xde,	0x46,	0x1c,	0x9f,	0x08,
            0x93,	0x76,	0x0e,	0x8f,	0x71,	0xda,	0xf4,	0x5f,
            0xaa,	0x91,	0x45,	0x82,	0x96,	0x59,	0x6b,	0xfe,
            0x48,	0xef,	0x62,	0x6d,	0x20,	0xb0,	0x18,	0xac,
            0x95,	0xe7,	0x5e,	0xde,	0xdd,	0xba,	0xec,	0x29,
            0xcf,	0xdf,	0x56,	0x4b,	0x6e,	0x3d,	0xba,	0x58
        ])

        self.assertEqual(tempHash.hex(), expectedTempHash.hex())

        # chain: 0
        machine.run(tempHash)

        # pour tester que tempHash ne change pas après machine.run
        # self.assertEqual(tempHash.hex(), expectedTempHash.hex())

        reg = machine.getRegisterFile()

        self.assertEqual(reg.r, [
            11905290616973309872, 
            11084093945605122378, 
            9658358183713692388, 
            3039984054309546556, 
            10148183520807958893, 
            16992555893191319727,
            2042482198024245230, 
            18221387339043260174
        ])

        self.assertEqual(reg.f[0].lo, -6.5509218151641486e-296)
        self.assertEqual(reg.f[0].hi, 9.9611750495227247e-288)
        self.assertEqual(reg.f[1].lo, 5.4358142914976027e-289)
        self.assertEqual(reg.f[1].hi, -7.2508163485180635e-283)
        self.assertEqual(reg.f[2].lo, -9.9842037598206744e-306)
        self.assertEqual(reg.f[2].hi, -6.7543726567798994e-300)
        self.assertEqual(reg.f[3].lo, 1.8406430402904109e-270)
        self.assertEqual(reg.f[3].hi, 2.1326346315915913e-288)

        self.assertEqual(reg.e[0].lo, 1.6404835333946248e+18)
        self.assertEqual(reg.e[0].hi, 7.5560091747870476e+25)
        self.assertEqual(reg.e[1].lo, 5.8015460116901498e+27) 
        self.assertEqual(reg.e[1].hi, 5.8416837053532367e+22)
        self.assertEqual(reg.e[2].lo, 637003.17243195313)
        self.assertEqual(reg.e[2].hi, 20.83993850352854)
        self.assertEqual(reg.e[3].lo, 1.1387086150584801e+30) 
        self.assertEqual(reg.e[3].hi, 5.178339327590577e+28)

        self.assertEqual(reg.a[0].lo, 2149835947.1810861)
        self.assertEqual(reg.a[0].hi, 2638.4968321402316)
        self.assertEqual(reg.a[1].lo, 917833.1847499148) 
        self.assertEqual(reg.a[1].hi, 15.755895524927684)
        self.assertEqual(reg.a[2].lo, 1006.0685992408105) 
        self.assertEqual(reg.a[2].hi, 18993.25198922756)
        self.assertEqual(reg.a[3].lo, 92365838.791484013) 
        self.assertEqual(reg.a[3].hi, 1738118321.5794246)

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratchpad_dump_0.bin'), 'rb') as f:
            expected_scratchpad_0 = f.read()

        self.assertEqual(machine.scratchpad.hex(), expected_scratchpad_0.hex())

        _reg = machine.getRegisterFile().to_bytes()
        blakeResult = blake2b(tempHash, len(tempHash), _reg, len(_reg), None, 0)

        expectedTempHash = bytearray([
            0xa2,	0x5e,	0x1b,	0x4b,	0xd9,	0xef,	0x84,	0x51,
            0x1e,	0xcb,	0xe0,	0x84,	0x32,	0x70,	0x69,	0xbb,
            0xf0,	0x19,	0x70,	0x4d,	0xf4,	0xe6,	0x6e,	0x6a,
            0x2a,	0xc5,	0xef,	0xfe,	0x42,	0x15,	0x95,	0xba,
            0xc7,	0xc9,	0xb3,	0x09,	0x1d,	0x7b,	0x21,	0x19,
            0xea,	0x7d,	0xd8,	0x91,	0xec,	0x8a,	0xfb,	0x87,
            0xf1,	0x22,	0xd2,	0xba,	0x57,	0x48,	0x10,	0x21,
            0x90,	0x21,	0xdc,	0x61,	0x53,	0x21,	0xfa,	0xc1
        ])

        self.assertEqual(tempHash.hex(), expectedTempHash.hex())

        # chain: 1
        machine.run(tempHash)

        expected_reg_bytes = bytes([
            0x26,	0xee,	0x01,	0x0f,	0xf3,	0x7d,	0xdf,	0x14,
            0x43,	0x72,	0x24,	0xe0,	0x36,	0xa9,	0x2b,	0x1f,
            0x3e,	0xe7,	0x42,	0xbe,	0xb1,	0x69,	0x61,	0x2b,
            0xf3,	0x17,	0x68,	0x56,	0xf0,	0x5d,	0x83,	0x82,
            0xd2,	0x85,	0x15,	0x72,	0x89,	0x33,	0x5b,	0x71,
            0x1b,	0xcc,	0xf0,	0x05,	0x7d,	0x19,	0xb8,	0x64,
            0x5e,	0x4b,	0x99,	0x1b,	0x1f,	0x6a,	0x06,	0x28,
            0x8a,	0x04,	0x7d,	0x81,	0xa2,	0xb0,	0x8c,	0x7f,
            0x2d,	0xe4,	0xe9,	0x2c,	0xe1,	0x92,	0xd5,	0x11,
            0xfb,	0x55,	0x04,	0x8d,	0x5a,	0xca,	0xb3,	0x91,
            0x59,	0xda,	0xf5,	0x17,	0xbc,	0x69,	0xb3,	0x8b,
            0x4f,	0x54,	0x3a,	0xa2,	0xfc,	0x73,	0xe9,	0x86,
            0x82,	0x6b,	0xcc,	0x30,	0x0d,	0x30,	0x24,	0x02,
            0xaa,	0x68,	0xc3,	0x1f,	0xa1,	0xb9,	0xda,	0x05,
            0x76,	0x86,	0xf0,	0x8b,	0x40,	0x3b,	0x45,	0x07,
            0xa0,	0xe4,	0x80,	0x2a,	0x0a,	0x0a,	0x9a,	0x86,
            0x8e,	0x7c,	0x57,	0xf8,	0xfc,	0x51,	0x2c,	0x50,
            0x99,	0x71,	0x01,	0xe8,	0x50,	0x99,	0x51,	0x50,
            0x53,	0xd5,	0x6a,	0xa6,	0xf9,	0x05,	0x61,	0x4a,
            0x71,	0x67,	0x8b,	0x6f,	0xb7,	0x0d,	0x20,	0x47,
            0x0a,	0xdf,	0xab,	0xfc,	0x50,	0xe9,	0x97,	0x43,
            0x3b,	0x78,	0x80,	0x41,	0x18,	0x9e,	0x04,	0x44,
            0x0e,	0xf4,	0xb7,	0x49,	0xa7,	0x1a,	0x94,	0x46,
            0x42,	0x79,	0x98,	0x0f,	0xe8,	0xf7,	0x0c,	0x47,
            0x95,	0xf4,	0xb7,	0x26,	0x2d,	0x4e,	0x16,	0x41,
            0x8a,	0x12,	0x4c,	0x05,	0x2a,	0xd2,	0x99,	0x41,
            0x0d,	0xf8,	0x65,	0xee,	0x8c,	0x37,	0x0a,	0x41,
            0xf4,	0xb5,	0xd2,	0x64,	0x3d,	0xb8,	0xaa,	0x40,
            0xcc,	0xbb,	0xe8,	0x25,	0x69,	0x1d,	0xc1,	0x41,
            0xe8,	0x1e,	0x2c,	0xe3,	0x74,	0x03,	0x3f,	0x41,
            0xb8,	0x6e,	0xd3,	0x52,	0xf5,	0xd3,	0xd7,	0x40,
            0xd4,	0xe4,	0xa2,	0x24,	0x0c,	0x92,	0x35,	0x41
        ])

        _reg = machine.getRegisterFile().to_bytes()

        self.assertEqual(_reg.hex(), expected_reg_bytes.hex())

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratchpad_dump_1.bin'), 'rb') as f:
            expected_scratchpad_1 = f.read()

        self.assertEqual(machine.scratchpad.hex(), expected_scratchpad_1.hex())

        _reg = machine.getRegisterFile().to_bytes()
        blakeResult = blake2b(tempHash, len(tempHash), _reg, len(_reg), None, 0)

        expectedTempHash = bytearray([
            0xfe,	0xf4,	0x6b,	0x30,	0x30,	0x1b,	0xfe,	0x69,
            0xc6,	0xbb,	0x3c,	0xe0,	0x4d,	0x9c,	0x85,	0xdc,
            0x42,	0x04,	0xd2,	0xa9,	0x2a,	0x92,	0x8d,	0x36,
            0x3d,	0xb5,	0x4f,	0x36,	0x97,	0x36,	0x3e,	0x39,
            0xb5,	0x9a,	0x42,	0x4c,	0x7d,	0xd1,	0x8a,	0x50,
            0x82,	0xac,	0x2c,	0x5b,	0x04,	0x20,	0x0c,	0x0c,
            0x3f,	0x0d,	0x67,	0x84,	0x56,	0x0d,	0x89,	0xd0,
            0xf4,	0x3f,	0x6e,	0xcc,	0xed,	0xfb,	0x0e,	0xbd
        ])

        self.assertEqual(tempHash.hex(), expectedTempHash.hex())

        # chain: 2..(RANDOMX_PROGRAM_COUNT - 2)
