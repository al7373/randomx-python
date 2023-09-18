from typing import List, Optional
from .SuperscalarProgram import SuperscalarProgram
from .SuperscalarInstructionType import SuperscalarInstructionType 
from .smulh import smulh
from .mulh import mulh
from .signExtend2sCompl import signExtend2sCompl 
from .rotr import rotr 
from randomx.randomx_reciprocal import randomx_reciprocal
from ctypes import c_uint64
import json

def executeSuperscalar(
        r: List[c_uint64], 
        prog: SuperscalarProgram, 
        reciprocals: Optional[List[c_uint64]] = None,
        produce_instr_effects=False,
        instr_effects_filename=None
    ):

    if produce_instr_effects:
        instr_effects = []

    for j in range(prog.getSize()):

        if produce_instr_effects:
            previous_registers = r.copy()

        instr = prog(j)
        opcode = SuperscalarInstructionType(instr.opcode)

        if opcode == SuperscalarInstructionType.ISUB_R:
            r[instr.dst] = (r[instr.dst] - r[instr.src]) & 0xFFFFFFFFFFFFFFFF
        elif opcode == SuperscalarInstructionType.IXOR_R:
            r[instr.dst] ^= r[instr.src]
        elif opcode == SuperscalarInstructionType.IADD_RS:
            r[instr.dst] = (r[instr.dst] + (r[instr.src] << instr.getModShift())) & 0xFFFFFFFFFFFFFFFF
        elif opcode == SuperscalarInstructionType.IMUL_R:
            r[instr.dst] = (r[instr.dst] * r[instr.src]) & 0xFFFFFFFFFFFFFFFF
        elif opcode == SuperscalarInstructionType.IROR_C:
            r[instr.dst] = rotr(r[instr.dst], instr.getImm32())
        elif opcode in (SuperscalarInstructionType.IADD_C7, SuperscalarInstructionType.IADD_C8, SuperscalarInstructionType.IADD_C9):
            r[instr.dst] = (r[instr.dst] + signExtend2sCompl(instr.getImm32())) &  0xFFFFFFFFFFFFFFFF
        elif opcode in (SuperscalarInstructionType.IXOR_C7, SuperscalarInstructionType.IXOR_C8, SuperscalarInstructionType.IXOR_C9):
            r[instr.dst] ^= signExtend2sCompl(instr.getImm32())
        elif opcode == SuperscalarInstructionType.IMULH_R:
            r[instr.dst] = mulh(r[instr.dst], r[instr.src])
        elif opcode == SuperscalarInstructionType.ISMULH_R:
            r[instr.dst] = smulh(r[instr.dst], r[instr.src])
        elif opcode == SuperscalarInstructionType.IMUL_RCP:
            if reciprocals is not None:
                r[instr.dst] = (r[instr.dst] * reciprocals[instr.getImm32()]) & 0xFFFFFFFFFFFFFFFF
            else:
                r[instr.dst] *= randomx_reciprocal(instr.getImm32())
        else:
            raise ValueError("Unreachable code")

        if produce_instr_effects:
            instr_effect = {
                "instruction": {
                    "dst": instr.dst,
                    "imm32": instr.getImm32(),
                    "mod": instr.mod,
                    "opcode": instr.opcode,
                    "src": instr.src
                }
            }
            instr_effect["registers"] = r.copy()
            instr_effect["previous_registers"] = previous_registers

            instr_effects.append(instr_effect)

    if produce_instr_effects:
        # Ouvrez un fichier en mode écriture
        filename = './test/_superscalar/instr_effects_python.json'
        if instr_effects_filename is not None:
            filename = './test/_superscalar/instr_effects/' + instr_effects_filename + '.json'
        with open(filename, 'w') as file:
            # Convertissez l'objet Python en JSON et écrivez-le dans le fichier
            json.dump(instr_effects, file)

