from typing import List
from .ExecutionPort import ExecutionPort
from randomx.const import CYCLE_MAP_SIZE

def scheduleUop(commit: bool, uop: ExecutionPort, portBusy: List[List[ExecutionPort]], cycle: int) -> int:
    while cycle < CYCLE_MAP_SIZE:
        if (uop & ExecutionPort.P5) != 0 and not portBusy[cycle][2]:
            if commit:
                portBusy[cycle][2] = uop
            return cycle
        if (uop & ExecutionPort.P0) != 0 and not portBusy[cycle][0]:
            if commit:
                portBusy[cycle][0] = uop
            return cycle
        if (uop & ExecutionPort.P1) != 0 and not portBusy[cycle][1]:
            if commit:
                portBusy[cycle][1] = uop
            return cycle
        cycle += 1
    return -1

