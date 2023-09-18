import unittest
from randomx.Program import Program
import os
import json

class TestProgram(unittest.TestCase):

    def test_deserialize_entropyBuffer(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'program_dump.bin'), 'rb') as f:
            data = f.read()
        program = Program()
        program.deserialize(data)

        self.assertEqual(program.entropyBuffer, [
            18221569025469959029, 
            6540525175208166347, 
            11284897593959090804, 
            1859849227501142954, 
            5759946197137768062, 
            8426952128535686356,
            15435530889885022921, 
            17706436732194723147, 
            42957510343193920, 
            2142773600011913680, 
            11562294675589571736, 
            2078438899640705108,
            9938799071294326890, 
            13382051314497303325, 
            9713811302651988593, 
            17049312405384313502
        ])

    def test_getEntropy(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'program_dump.bin'), 'rb') as f:
            data = f.read()
        program = Program()
        program.deserialize(data)

        self.assertEqual(program.getEntropy(0), 18221569025469959029) 
        self.assertEqual(program.getEntropy(1), 6540525175208166347) 
        self.assertEqual(program.getEntropy(2), 11284897593959090804)
        self.assertEqual(program.getEntropy(3), 1859849227501142954) 
        self.assertEqual(program.getEntropy(4), 5759946197137768062) 
        self.assertEqual(program.getEntropy(5), 8426952128535686356)
        self.assertEqual(program.getEntropy(6), 15435530889885022921)
        self.assertEqual(program.getEntropy(7), 17706436732194723147) 
        self.assertEqual(program.getEntropy(8), 42957510343193920) 
        self.assertEqual(program.getEntropy(9), 2142773600011913680) 
        self.assertEqual(program.getEntropy(10), 11562294675589571736) 
        self.assertEqual(program.getEntropy(11), 2078438899640705108)
        self.assertEqual(program.getEntropy(12), 9938799071294326890) 
        self.assertEqual(program.getEntropy(13), 13382051314497303325) 
        self.assertEqual(program.getEntropy(14), 9713811302651988593) 
        self.assertEqual(program.getEntropy(15), 17049312405384313502)

    def test_deserialize_programBuffer(self):
        
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'program_dump.bin'), 'rb') as f:
            data = f.read()
        
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'program_dump.json'), 'r') as f:
            expected = json.load(f)

        program = Program()
        program.deserialize(data)

        for i, expected_instr in enumerate(expected['instructions']):
            instr = program.programBuffer[i]
            self.assertEqual(
                instr.opcode, expected_instr['opcode'], 
                f"opcode of instruction n°{i}"
            )
            self.assertEqual(
                instr.dst, expected_instr['dst'],
                f"dst of instruction n°{i}"
            )
            self.assertEqual(
                instr.src, expected_instr['src'],
                f"src of instruction n°{i}"
            )
            self.assertEqual(
                instr.mod, expected_instr['mod'],
                f"mod of instruction n°{i}"
            )
            self.assertEqual(
                instr.getImm32(), expected_instr['imm32'],
                f"imm32 of instruction n°{i}"
            )
            
