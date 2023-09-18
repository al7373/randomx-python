import unittest
from superscalar.SuperscalarInstruction import SuperscalarInstruction
from superscalar.SuperscalarInstructionInfo import SuperscalarInstructionInfo, slot_3, slot_3L, slot_4, slot_7, slot_8, slot_9, slot_10
from randomx.Instruction import Instruction
from blake2b.Blake2Generator import Blake2Generator
from superscalar.SuperscalarInstructionType import SuperscalarInstructionType
from superscalar.RegisterInfo import RegisterInfo 

class TestSuperscalarInstruction(unittest.TestCase):

    def test_toInstr(self):
        info = SuperscalarInstructionInfo.ISUB_R
        si = SuperscalarInstruction(info)
        si.src_ = 2
        si.dst_ = 3
        si.mod_ = 5
        si.imm32_ = 12345

        instr = Instruction()
        si.toInstr(instr)

        self.assertEqual(instr.opcode, info.getType().value)
        self.assertEqual(instr.dst, 3)
        self.assertEqual(instr.src, 2)
        self.assertEqual(instr.getImm32(), 12345)
        self.assertEqual(instr.getModMem(), 1)
        self.assertEqual(instr.getModShift(), 1)
        self.assertEqual(instr.getModCond(), 0)

    def test_create(self):
        seed = b"test_seed"
        gen = Blake2Generator(seed, len(seed))

        for slot in [slot_3, slot_3L, slot_4, slot_7, slot_8, slot_9]:
            for info in slot:
                instruction = SuperscalarInstruction()
                instruction.create(info, gen)

                # Vérifier si la méthode 'create' définit les attributs de l'objet SuperscalarInstruction correctement
                self.assertEqual(instruction.getInfo(), info)
                self.assertIsNotNone(instruction.getSource())
                self.assertIsNotNone(instruction.getDestination())
                self.assertIsNotNone(instruction.getGroup())

    def test_createForSlot(self):
        gen = Blake2Generator(b"seed", 4, 0)
        inst = SuperscalarInstruction()

        inst.createForSlot(gen, 3, 1, True, False)
        self.assertEqual(inst.getType(), SuperscalarInstructionType.IXOR_R)

        inst.createForSlot(gen, 3, 1, False, False)
        self.assertEqual(inst.getType(), SuperscalarInstructionType.IXOR_R)

        inst.createForSlot(gen, 4, 1, False, False)
        self.assertEqual(inst.getType(), SuperscalarInstructionType.IROR_C)

        inst.createForSlot(gen, 7, 1, False, False)
        self.assertEqual(inst.getType(), SuperscalarInstructionType.IXOR_C7)

        inst.createForSlot(gen, 8, 1, False, False)
        self.assertEqual(inst.getType(), SuperscalarInstructionType.IXOR_C8)

        inst.createForSlot(gen, 9, 1, False, False)
        self.assertEqual(inst.getType(), SuperscalarInstructionType.IADD_C9)

        inst.createForSlot(gen, 10, 1, False, True)
        self.assertEqual(inst.getType(), SuperscalarInstructionType.IMUL_RCP)

    def test_selectDestination(self):
        instr = SuperscalarInstruction()
        cycle = 1
        allow_chained_mul = False
        registers = [RegisterInfo() for _ in range(8)]
        gen = Blake2Generator(b"seed", 4)
        instr.create(SuperscalarInstructionInfo.ISUB_R, gen)
        self.assertTrue(instr.selectDestination(cycle, allow_chained_mul, registers, gen))
        self.assertEqual(instr.getDestination(), 1)

        allow_chained_mul = True
        cycle = 2
        instr.create(SuperscalarInstructionInfo.IADD_C9, gen)
        self.assertTrue(instr.selectDestination(cycle, allow_chained_mul, registers, gen))
        self.assertEqual(instr.getDestination(), 3)

        allow_chained_mul = False
        # Modifier l'opGroup_
        instr.create(SuperscalarInstructionInfo.IADD_C8, gen)
        # Définir la latence de tous les registres supérieure à cycle
        cycle = 1
        for register in registers:
            register.latency = cycle + 1
        # Vérifier que la fonction renvoie False
        self.assertFalse(instr.selectDestination(cycle, allow_chained_mul, registers, gen))
        self.assertEqual(instr.getDestination(), -1)

    def test_selectSource(self):
        # Initialisation des données pour le test
        seed = b'Test seed for Blake2Generator'
        gen = Blake2Generator(seed, len(seed))
        registers = [RegisterInfo() for _ in range(8)]

        # Exemple de SuperscalarInstructionInfo à utiliser pour le test
        instr1 = slot_3[0]  # ISUB_R
        instr2 = slot_4[0]  # IROR_C

        # Initialisation de deux instructions Superscalar
        instruction1 = SuperscalarInstruction.Null
        instruction1.create(instr1, gen)

        instruction2 = SuperscalarInstruction.Null
        instruction2.create(instr2, gen)

        # Appel de la méthode selectSource et vérification des résultats
        instruction1.selectSource(1, registers, gen)
        selected_src1 = instruction1.getSource()
        self.assertEqual(selected_src1, 6)
        self.assertIn(selected_src1, range(8), "Le registre source sélectionné doit être compris entre 0 et 7")

        instruction2.selectSource(1, registers, gen)
        selected_src2 = instruction2.getSource()
        self.assertEqual(selected_src2, 5)
        self.assertIn(selected_src2, range(8), "Le registre source sélectionné doit être compris entre 0 et 7")

        # Assurez-vous que les sources sélectionnées sont différentes, car les instructions sont différentes
        self.assertNotEqual(selected_src1, selected_src2, "Les registres sources sélectionnés doivent être différents pour des instructions différentes")




