import unittest
from superscalar.SuperscalarProgram import SuperscalarProgram
from blake2b.Blake2Generator import Blake2Generator
from superscalar.generateSuperscalar import generateSuperscalar
import struct
from randomx.configuration import RANDOMX_CACHE_ACCESSES 
import os
import json

class TestGenerateSuperscalar(unittest.TestCase):

    def test_generateSuperscalar(self):
        seed = b"testseed"
        seed_size = len(seed)

        # Création d'un générateur Blake2
        gen = Blake2Generator(seed, seed_size)

        # Création d'un programme superscalaire vide
        prog = SuperscalarProgram()

        # Appel de la fonction generateSuperscalar
        generateSuperscalar(prog, gen)

        # Vérification des propriétés du programme généré
        self.assertEqual(prog.getSize(), 468)
        self.assertEqual(prog.codeSize, 2305)
        self.assertEqual(prog.macroOps, 528)
        self.assertEqual(prog.decodeCycles, 149)
        self.assertEqual(prog.cpuLatency, 173)
        self.assertEqual(prog.asicLatency, 93)

        #self.assertAlmostEqualprog.ipc, 3.05202, 5)
        self.assertEqual(
            bytes.fromhex(struct.pack('<d', prog.ipc).hex()), 
            bytes.fromhex('29f427198b6a0840')
        )

        expected_used_registers = [6, 1, 5, 4, 0, 4, 2, 3, 0, 3, 7, 0, 4, 3, 0, 2, 5, 6, 7, 1, 3, 6, 7, 4, 4, 5, 2, 5, 1, 6, 2, 0, 3, 0, 7, 1, 0, 0, 2, 5, 3, 2, 3, 1, 4, 6, 4, 4, 0, 4, 7, 7, 2, 3, 7, 6, 3, 0, 1, 7, 2, 5, 1, 6, 4, 3, 2, 5, 7, 3, 2, 0, 6, 1, 4, 0, 2, 0, 4, 6, 2, 1, 2, 7, 5, 7, 1, 3, 4, 0, 1, 6, 6, 1, 7, 2, 6, 7, 0, 5, 1, 0, 3, 1, 0, 0, 5, 3, 0, 1, 1, 2, 4, 1, 5, 3, 5, 1, 4, 0, 2, 2, 6, 7, 5, 2, 3, 7, 6, 1, 0, 2, 1, 3, 1, 2, 1, 3, 0, 7, 2, 7, 4, 1, 6, 5, 5, 3, 7, 2, 5, 6, 1, 0, 7, 2, 4, 3, 3, 4, 0, 2, 3, 7, 4, 5, 6, 5, 1, 6, 5, 4, 0, 6, 2, 1, 5, 5, 3, 1, 5, 3, 4, 6, 7, 0, 3, 7, 1, 0, 6, 2, 4, 3, 2, 0, 6, 2, 5, 2, 0, 4, 1, 6, 7, 7, 6, 7, 2, 3, 5, 1, 7, 2, 4, 2, 0, 6, 2, 1, 4, 0, 4, 0, 3, 1, 2, 0, 7, 4, 5, 0, 4, 3, 4, 0, 7, 6, 3, 2, 3, 5, 4, 5, 1, 4, 2, 0, 4, 5, 6, 3, 1, 6, 6, 7, 6, 1, 2, 3, 6, 4, 0, 0, 1, 1, 0, 5, 0, 1, 7, 0, 3, 3, 4, 5, 4, 2, 1, 5, 6, 7, 2, 1, 4, 3, 3, 4, 5, 0, 3, 6, 7, 6, 4, 3, 4, 7, 6, 1, 2, 6, 0, 3, 2, 5, 2, 3, 0, 6, 6, 7, 4, 1, 4, 6, 7, 7, 6, 3, 5, 6, 7, 2, 3, 5, 0, 0, 3, 0, 4, 1, 0, 1, 3, 0, 4, 2, 4, 7, 6, 5, 4, 4, 2, 2, 4, 5, 7, 1, 3, 0, 3, 1, 6, 1, 3, 3, 2, 1, 6, 5, 7, 5, 0, 7, 4, 3, 0, 5, 0, 7, 5, 2, 4, 6, 6, 3, 1, 0, 6, 0, 6, 0, 4, 1, 3, 1, 1, 5, 5, 3, 2, 3, 2, 5, 6, 1, 6, 4, 4, 1, 1, 7, 6, 7, 4, 2, 0, 1, 3, 5, 6, 2, 6, 3, 5, 0, 1, 7, 6, 6, 7, 6, 7, 2, 0, 7, 2, 0, 6, 3, 6, 3, 4, 6, 1, 4, 6, 3, 1, 7, 4, 4, 0, 7, 4, 6, 7, 4, 0, 5, 2, 3, 2, 3, 7, 5, 1, 6, 7, 3, 5, 5, 1, 2, 4, 0]

        # Vérification des registres utilisés
        used_registers = [prog(i).dst for i in range(prog.getSize())]

        self.assertEqual(used_registers, expected_used_registers)

    def test_generateSuperscalar_1(self):

        key = "test key 000"
        key_size = len(key)
        keyInBytes = key.encode('utf-8')

        programs = [SuperscalarProgram()] * RANDOMX_CACHE_ACCESSES

        gen = Blake2Generator(keyInBytes, key_size)

        progsDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'progs')

        for i in range(RANDOMX_CACHE_ACCESSES):
            generateSuperscalar(programs[i], gen)

            with open(os.path.join(progsDir, 'initCache_prog_' + str(i) + '.json'), 'r') as f:
                expectedProg = json.load(f)

            prog = programs[i]

            instructions = []
            for j in range(prog.getSize()):
                instruction = {}
                instr = prog(j)
                instruction["dst"] = instr.dst
                instruction["imm32"] = instr.getImm32()
                instruction["mod"] = instr.mod
                instruction["opcode"] = instr.opcode
                instruction["src"] = instr.src
                instructions.append(instruction)

            self.assertEqual(instructions, expectedProg["instructions"], f"\nLe programme n°{i} a échoué.\n")

            self.assertEqual(prog.size, expectedProg["size"])
            self.assertEqual(prog.addrReg, expectedProg["address_register"])
            self.assertEqual(prog.ipc, expectedProg["ipc"])
            self.assertEqual(prog.codeSize, expectedProg["codeSize"])
            self.assertEqual(prog.macroOps, expectedProg["macroOps"])
            self.assertEqual(prog.decodeCycles, expectedProg["decodeCycles"])
            self.assertEqual(prog.cpuLatency, expectedProg["cpuLatency"])
            self.assertEqual(prog.asicLatency, expectedProg["asicLatency"])
            self.assertEqual(prog.mulCount, expectedProg["mulCount"])
            self.assertEqual(prog.cpuLatencies, expectedProg["cpuLatencies"])
            self.assertEqual(prog.asicLatencies, expectedProg["asicLatencies"])


