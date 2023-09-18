from typing import List
from .MacroOp import MacroOp
from .ExecutionPort import ExecutionPort
from .scheduleUop import scheduleUop
from randomx.const import CYCLE_MAP_SIZE

def scheduleMop(commit: bool, mop: MacroOp, portBusy: List[List[ExecutionPort]], cycle: int, depCycle: int) -> int:
    if mop.isDependent():
        cycle = max(cycle, depCycle)
        
    if mop.isEliminated():
        if commit:
            pass
        return cycle
    elif mop.isSimple():
        return scheduleUop(commit, mop.getUop1(), portBusy, cycle)
    else:
        for cycle in range(cycle, CYCLE_MAP_SIZE):
            cycle1 = scheduleUop(False, mop.getUop1(), portBusy, cycle)
            cycle2 = scheduleUop(False, mop.getUop2(), portBusy, cycle)

            if cycle1 >= 0 and cycle1 == cycle2:
                if commit:
                    scheduleUop(True, mop.getUop1(), portBusy, cycle1)
                    scheduleUop(True, mop.getUop2(), portBusy, cycle2)
                return cycle1

    return -1

