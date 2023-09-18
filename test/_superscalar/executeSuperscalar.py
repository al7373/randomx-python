import unittest
from typing import List
from superscalar.executeSuperscalar import executeSuperscalar
from superscalar.SuperscalarProgram import SuperscalarProgram
from superscalar.SuperscalarInstructionType import SuperscalarInstructionType
from randomx.Instruction import Instruction
import json
import os
import sys

# sys.set_int_max_str_digits(10000)

class TestExecuteSuperscalar(unittest.TestCase):

    def test_ISUB_R(self):
        r = [1, 2, 3, 4, 5, 6, 7, 8]
        prog = SuperscalarProgram()
        prog.setSize(1)
        instr = Instruction()
        instr.opcode = SuperscalarInstructionType.ISUB_R.value
        instr.dst = 1
        instr.src = 2
        prog.programBuffer[0] = instr

        executeSuperscalar(r, prog)
        self.assertEqual(r, [1, 18446744073709551615, 3, 4, 5, 6, 7, 8])

    def test_ISUB_R_1046483985571386024(self):
        r = [1, 1046483985571386024, 10306024060725146345, 4, 5, 6, 7, 8]
        prog = SuperscalarProgram()
        prog.setSize(1)
        instr = Instruction()
        instr.opcode = SuperscalarInstructionType.ISUB_R.value
        instr.dst = 1
        instr.src = 2
        prog.programBuffer[0] = instr

        executeSuperscalar(r, prog)
        self.assertEqual(r, [1, 9187203998555791295, 10306024060725146345, 4, 5, 6, 7, 8])

    def test_IXOR_R(self):
        r = [1, 2, 3, 4, 5, 6, 7, 8]
        prog = SuperscalarProgram()
        prog.setSize(1)
        instr = Instruction()
        instr.opcode = SuperscalarInstructionType.IXOR_R.value
        instr.dst = 1
        instr.src = 2
        prog.programBuffer[0] = instr

        executeSuperscalar(r, prog)
        self.assertEqual(r, [1, 1, 3, 4, 5, 6, 7, 8])

    def test_IXOR_R_12691012460731140224(self):
        r = [1, 12691012460731140224, 380322263769223000, 4, 5, 6, 7, 8]
        prog = SuperscalarProgram()
        prog.setSize(1)
        instr = Instruction()
        instr.opcode = SuperscalarInstructionType.IXOR_R.value
        instr.dst = 1
        instr.src = 2
        prog.programBuffer[0] = instr

        executeSuperscalar(r, prog)
        self.assertEqual(r, [1, 13067376299294361560, 380322263769223000, 4, 5, 6, 7, 8])

    def test_IADD_RS(self):
        r = [1, 2, 3, 4, 5, 6, 7, 8]
        prog = SuperscalarProgram()
        prog.setSize(1)
        instr = Instruction()
        instr.opcode = SuperscalarInstructionType.IADD_RS.value
        instr.dst = 1
        instr.src = 2
        instr.mod = 2  # modShift = 2
        prog.programBuffer[0] = instr

        executeSuperscalar(r, prog)
        self.assertEqual(r, [1, 5, 3, 4, 5, 6, 7, 8])

    def test_IADD_RS_12916111777369101259(self):
        r = [1, 12916111777369101259, 1818988163740667062, 4, 5, 6, 7, 8]
        prog = SuperscalarProgram()
        prog.setSize(1)
        instr = Instruction()
        instr.opcode = SuperscalarInstructionType.IADD_RS.value
        instr.dst = 1
        instr.src = 2
        instr.mod = 0xdd 
        prog.programBuffer[0] = instr

        executeSuperscalar(r, prog)
        self.assertEqual(r, [1, 9021273013584886139, 1818988163740667062, 4, 5, 6, 7, 8])

    def test_IMUL_R(self):
        r = [1, 2, 3, 4, 5, 6, 7, 8]
        prog = SuperscalarProgram()
        prog.setSize(1)
        instr = Instruction()
        instr.opcode = SuperscalarInstructionType.IMUL_R.value
        instr.dst = 1
        instr.src = 2
        prog.programBuffer[0] = instr

        executeSuperscalar(r, prog)
        self.assertEqual(r, [1, 6, 3, 4, 5, 6, 7, 8])

    def test_IMUL_R_6364136223846793005(self):
        r = [6364136223846793005, 15662221698380390097, 18384096042004490091, 15670078305396536945, 1233090996314240335, 14584374767940244257, 8609653616329052757, 15912571922823092835]
        prog = SuperscalarProgram()
        prog.setSize(1)
        instr = Instruction()
        instr.opcode = SuperscalarInstructionType.IMUL_R.value
        instr.dst = 3
        instr.src = 0
        prog.programBuffer[0] = instr

        executeSuperscalar(r, prog)
        self.assertEqual(r, [6364136223846793005, 15662221698380390097, 18384096042004490091, 13009453847783645405, 1233090996314240335, 14584374767940244257, 8609653616329052757, 15912571922823092835])

    def test_IMUL_R_10221665616007626095(self):
        r = [1, 10221665616007626095, 1818988163740667062, 4, 5, 6, 7, 8]
        prog = SuperscalarProgram()
        prog.setSize(1)
        instr = Instruction()
        instr.opcode = SuperscalarInstructionType.IMUL_R.value
        instr.dst = 1
        instr.src = 2
        prog.programBuffer[0] = instr

        executeSuperscalar(r, prog)
        self.assertEqual(r, [1, 5808442873918611690, 1818988163740667062, 4, 5, 6, 7, 8])

    def test_IROR_C(self):
        r = [1, 2, 3, 4, 5, 6, 7, 8]
        prog = SuperscalarProgram()
        prog.setSize(1)
        instr = Instruction()
        instr.opcode = SuperscalarInstructionType.IROR_C.value
        instr.dst = 1
        instr.setImm32(1)  # Shift 1 bit
        prog.programBuffer[0] = instr

        executeSuperscalar(r, prog)
        self.assertEqual(r, [1, 1, 3, 4, 5, 6, 7, 8])

    def test_IROR_C_6939675455496331487(self):
        r = [1, 6939675455496331487, 3, 4, 5, 6, 7, 8]
        prog = SuperscalarProgram()
        prog.setSize(1)
        instr = Instruction()
        instr.opcode = SuperscalarInstructionType.IROR_C.value
        instr.dst = 1
        instr.setImm32(52)
        prog.programBuffer[0] = instr

        executeSuperscalar(r, prog)
        self.assertEqual(r, [1, 16924792200264283652, 3, 4, 5, 6, 7, 8])

    def test_IADD_C7(self):
        r = [1, 2, 3, 4, 5, 6, 7, 8]
        prog = SuperscalarProgram()
        prog.setSize(1)
        instr = Instruction()
        instr.opcode = SuperscalarInstructionType.IADD_C7.value
        instr.dst = 1
        instr.setImm32(3)
        prog.programBuffer[0] = instr

    def test_IADD_C7_1770085717091116626(self):
        r = [1, 1770085717091116626, 3, 4, 5, 6, 7, 8]
        prog = SuperscalarProgram()
        prog.setSize(1)
        instr = Instruction()
        instr.opcode = SuperscalarInstructionType.IADD_C7.value
        instr.dst = 1
        instr.setImm32(195985898)
        prog.programBuffer[0] = instr

        executeSuperscalar(r, prog)
        self.assertEqual(r, [1, 1770085717287102524, 3, 4, 5, 6, 7, 8])

    def test_IADD_C8_4035726067198559265(self):
        r = [12903528805402956936, 681616694861448470, 7187797453867926541, 10075901744801106141, 8242844125479750015, 4035726067198559265, 4327036483130138847, 3709534635486800689]

        prog = SuperscalarProgram()
        prog.setSize(1)
        instr = Instruction()
        instr.opcode = SuperscalarInstructionType.IADD_C8.value
        instr.dst = 5
        instr.src = 5
        instr.setImm32(4284054654)
        prog.programBuffer[0] = instr

        executeSuperscalar(r, prog)
        self.assertEqual(r, [
            12903528805402956936,
            681616694861448470,
            7187797453867926541,
            10075901744801106141,
            8242844125479750015,
            4035726067187646623,
            4327036483130138847,
            3709534635486800689
        ])

    def test_IXOR_C7(self):
        r = [1, 2, 3, 4, 5, 6, 7, 8]
        prog = SuperscalarProgram()
        prog.setSize(1)
        instr = Instruction()
        instr.opcode = SuperscalarInstructionType.IXOR_C7.value
        instr.dst = 1
        instr.setImm32(2)
        prog.programBuffer[0] = instr

        executeSuperscalar(r, prog)
        self.assertEqual(r, [1, 0, 3, 4, 5, 6, 7, 8])

    def test_IXOR_C8_1818988163740667062(self):
        r = [1, 1818988163740667062, 3, 4, 5, 6, 7, 8]
        prog = SuperscalarProgram()
        prog.setSize(1)
        instr = Instruction()
        instr.opcode = SuperscalarInstructionType.IXOR_C8.value
        instr.dst = 1
        instr.setImm32(3068346566)
        prog.programBuffer[0] = instr

        executeSuperscalar(r, prog)
        self.assertEqual(r, [1, 16627755910890278000, 3, 4, 5, 6, 7, 8])

    def test_IMULH_R(self):
        r = [1, 2, 3, 4, 5, 6, 7, 8]
        prog = SuperscalarProgram()
        prog.setSize(1)
        instr = Instruction()
        instr.opcode = SuperscalarInstructionType.IMULH_R.value
        instr.dst = 1
        instr.src = 2
        prog.programBuffer[0] = instr

        executeSuperscalar(r, prog)
        self.assertEqual(r, [1, 0, 3, 4, 5, 6, 7, 8])

    def test_IMULH_R_413773405112495121(self):
        r = [1, 413773405112495121, 16955433526176753096, 4, 5, 6, 7, 8]
        prog = SuperscalarProgram()
        prog.setSize(1)
        instr = Instruction()
        instr.opcode = SuperscalarInstructionType.IMULH_R.value
        instr.dst = 1
        instr.src = 2
        prog.programBuffer[0] = instr

        executeSuperscalar(r, prog)
        self.assertEqual(r, [1, 380322263769223000, 16955433526176753096, 4, 5, 6, 7, 8])

    def test_ISMULH_R_0xBC550E96BA88A72B(self):
        r = [1, 0xBC550E96BA88A72B, 0xF5391FA9F18D6273, 4, 5, 6, 7, 8]
        prog = SuperscalarProgram()
        prog.setSize(1)
        instr = Instruction()
        instr.opcode = SuperscalarInstructionType.ISMULH_R.value
        instr.dst = 1
        instr.src = 2
        prog.programBuffer[0] = instr

        executeSuperscalar(r, prog)
        self.assertEqual(r, [1, 0x02D93EF1269D3EE5, 0xF5391FA9F18D6273, 4, 5, 6, 7, 8])

    def test_ISMULH_R_0x00550E96BA88ACCC(self):
        r = [1, 0x00550E96BA88ACCC, 0xF5391FA9F18D6273, 4, 5, 6, 7, 8]
        prog = SuperscalarProgram()
        prog.setSize(1)
        instr = Instruction()
        instr.opcode = SuperscalarInstructionType.ISMULH_R.value
        instr.dst = 1
        instr.src = 2
        prog.programBuffer[0] = instr

        executeSuperscalar(r, prog)
        self.assertEqual(r, [1, 0xFFFC6B5A4AC6CCCF, 0xF5391FA9F18D6273, 4, 5, 6, 7, 8])

    def test_IMUL_RCP(self):
        r = [1, 2, 3, 4, 5, 6, 7, 8]
        prog = SuperscalarProgram()
        prog.setSize(1)
        instr = Instruction()
        instr.opcode = SuperscalarInstructionType.IMUL_RCP.value
        instr.dst = 1
        instr.setImm32(3)  # Assume a predefined reciprocal for 3
        reciprocals = [1, 1, 2, 6]  # List of predefined reciprocals, 6 is the reciprocal for 3 in this example
        prog.programBuffer[0] = instr

        executeSuperscalar(r, prog, reciprocals)
        self.assertEqual(r, [1, 12, 3, 4, 5, 6, 7, 8])

    def test_IMUL_RCP_6233335023111290087(self):
        r = [1, 6233335023111290087, 3, 4, 5, 6, 7, 8]
        prog = SuperscalarProgram()
        prog.setSize(1)
        instr = Instruction()
        instr.opcode = SuperscalarInstructionType.IMUL_RCP.value
        instr.dst = 1
        instr.setImm32(3)  # Assume a predefined reciprocal for 3
        reciprocals = [1, 1, 2, 14293867265140468308]  # List of predefined reciprocals, 6 is the reciprocal for 3 in this example
        prog.programBuffer[0] = instr

        executeSuperscalar(r, prog, reciprocals)
        self.assertEqual(r, [1, 13431623528971755980, 3, 4, 5, 6, 7, 8])

    def test_instr_effects(self):

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instr_effects.json'), 'r') as f:
            instr_effects = json.load(f)

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instr_effects_python.json'), 'r') as f:
            instr_effects_python = json.load(f)

        for index, (instr_effect_python, instr_effect) in enumerate(zip(instr_effects_python, instr_effects)):

            prev_instr = instr_effects[index - 1] if index > 0 else None

            error_message = (
                f"L'instruction ayant l'index {index} a echoué.\n"
                f"L'instruction précédente est {prev_instr}"
            )

            self.assertEqual(
                instr_effect_python, 
                instr_effect, 
                error_message
            )

    def test_prog(self):

        r = [
            12265035440700876845, 
            3115575367880460753, 
            956646718107005035, 
            3103140520150376817,
            16391709936311263823, 
            4035726067198559265, 
            9591680619904714069, 
            3365054476449844579
        ]

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reciprocals.json'), 'r') as f:
            reciprocals = json.load(f)

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prog.json'), 'r') as f:
            progData = json.load(f)

        prog = SuperscalarProgram()

        prog = SuperscalarProgram()
        prog.setSize(progData['size'])
        prog.setAddressRegister(progData['address_register'])

        for index, instruction_data in enumerate(progData['instructions']):
            instruction = Instruction()
            instruction.opcode = instruction_data['opcode']
            instruction.dst = instruction_data['dst']
            instruction.src = instruction_data['src']
            instruction.setMod(instruction_data['mod'])
            instruction.setImm32(instruction_data['imm32'])
            prog.programBuffer[index] = instruction

        executeSuperscalar(r, prog, reciprocals, produce_instr_effects=False)

        # les valeurs ci-dessous sont correctes, elles viennent de la version C++
        self.assertEqual(r, [
            4286615819793156168, 
            4079512904007104130, 
            4039086561088512024, 
            1130408280926274320, 
            333017908324936060, 
            836639654418310296,
            13866092813378598336, 
            14568679482152831205
        ])

    def test_instr_effects_in_dataset_item(self):

        currentDir = os.path.dirname(os.path.abspath(__file__))
        instrEffectsRefDir = os.path.join(currentDir, 'instr_effects_ref')
        instrEffectsDir = os.path.join(currentDir, 'instr_effects')

        for filename in os.listdir(instrEffectsRefDir):
            instrEffectsRefPath = os.path.join(instrEffectsRefDir, filename)
            instrEffectsPath = os.path.join(instrEffectsDir, filename)
            if os.path.isfile(instrEffectsPath) and os.path.isfile(instrEffectsRefPath):
                with open(instrEffectsPath, 'r') as f:
                    instr_effects = json.load(f)
                with open(instrEffectsRefPath, 'r') as f:
                    instr_effects_ref = json.load(f)

                for index, (instr_effect, instr_effect_ref) in enumerate(zip(instr_effects, instr_effects_ref)):

                    prev_instr = instr_effects_ref[index - 1] if index > 0 else None

                    error_message = (
                        f"\nNom du fichier \"{filename}\"\n"
                        f"L'instruction ayant l'index {index} a echoué.\n"
                        f"L'instruction précédente est {prev_instr}\n"
                        f"L'instruction de reférence actuelle est:\n"
                        f"{instr_effects_ref[index]}\n"
                        f"L'instruction python actuelle est:\n"
                        f"{instr_effects[index]}\n"
                    )

                    self.assertEqual(
                        instr_effect, 
                        instr_effect_ref, 
                        error_message
                    )

