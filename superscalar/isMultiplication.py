from .SuperscalarInstructionType import SuperscalarInstructionType

def isMultiplication(instruction_type: SuperscalarInstructionType) -> bool:
    return instruction_type in (
        SuperscalarInstructionType.IMUL_R,
        SuperscalarInstructionType.IMULH_R,
        SuperscalarInstructionType.ISMULH_R,
        SuperscalarInstructionType.IMUL_RCP,
    )

