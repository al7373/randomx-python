from typing import List
from randomx.configuration import RANDOMX_SUPERSCALAR_LATENCY 
from randomx.const import CYCLE_MAP_SIZE, SuperscalarMaxSize, LOOK_FORWARD_CYCLES, MAX_THROWAWAY_COUNT
from .ExecutionPort import ExecutionPort
from .RegisterInfo import RegisterInfo
from .DecoderBuffer import DecoderBuffer
from .SuperscalarInstruction import SuperscalarInstruction
from .MacroOp import MacroOp
from .isMultiplication import isMultiplication
from .SuperscalarProgram import SuperscalarProgram
from blake2b.Blake2Generator import Blake2Generator
from .scheduleMop import scheduleMop 

def generateSuperscalar(prog: SuperscalarProgram, gen: Blake2Generator):
    portBusy = [[0] * 3 for _ in range(CYCLE_MAP_SIZE)]
    registers = [RegisterInfo() for _ in range(8)]

    decodeBuffer = DecoderBuffer.default
    currentInstruction = SuperscalarInstruction.Null
    macroOpIndex = 0
    codeSize = 0
    macroOpCount = 0
    cycle = 0
    depCycle = 0
    retireCycle = 0
    portsSaturated = False
    programSize = 0
    mulCount = 0
    decodeCycle = 0
    throwAwayCount = 0

    while decodeCycle < RANDOMX_SUPERSCALAR_LATENCY and not portsSaturated and programSize < SuperscalarMaxSize:
        decodeBuffer = decodeBuffer.fetch_next(currentInstruction.getType(), decodeCycle, mulCount, gen)
        bufferIndex = 0
        while bufferIndex < decodeBuffer.get_size():
            topCycle = cycle
            if macroOpIndex >= currentInstruction.getInfo().getSize():
                if portsSaturated or programSize >= SuperscalarMaxSize:
                    break
                currentInstruction.createForSlot(gen, decodeBuffer.get_counts()[bufferIndex], decodeBuffer.get_index(), decodeBuffer.get_size() == bufferIndex + 1, bufferIndex == 0)
                macroOpIndex = 0

            mop = currentInstruction.getInfo().getOp(macroOpIndex)

            scheduleCycle = scheduleMop(False, mop, portBusy, cycle, depCycle)
            if scheduleCycle < 0:
                portsSaturated = True
                break
            if macroOpIndex == currentInstruction.getInfo().getSrcOp():
                forward = 0
                while forward < LOOK_FORWARD_CYCLES and not currentInstruction.selectSource(scheduleCycle, registers, gen):
                    forward += 1
                    scheduleCycle += 1
                    cycle += 1

                if forward == LOOK_FORWARD_CYCLES:
                    if throwAwayCount < MAX_THROWAWAY_COUNT:
                        throwAwayCount += 1
                        macroOpIndex = currentInstruction.getInfo().getSize()
                        continue
                    currentInstruction = SuperscalarInstruction.Null
                    break
            if macroOpIndex == currentInstruction.getInfo().getDstOp():
                forward = 0
                while forward < LOOK_FORWARD_CYCLES and not currentInstruction.selectDestination(scheduleCycle, throwAwayCount > 0, registers, gen):
                    forward += 1
                    scheduleCycle += 1
                    cycle += 1

                if forward == LOOK_FORWARD_CYCLES:
                    if throwAwayCount < MAX_THROWAWAY_COUNT:
                        throwAwayCount += 1
                        macroOpIndex = currentInstruction.getInfo().getSize()
                        continue
                    currentInstruction = SuperscalarInstruction.Null
                    break
            throwAwayCount = 0
            scheduleCycle = scheduleMop(True, mop, portBusy, scheduleCycle, depCycle)

            if scheduleCycle < 0:
                portsSaturated = True
                break

            depCycle = scheduleCycle + mop.getLatency()

            if macroOpIndex == currentInstruction.getInfo().getResultOp():
                dst = currentInstruction.getDestination()
                ri = registers[dst]
                retireCycle = depCycle
                ri.latency = retireCycle
                ri.lastOpGroup = currentInstruction.getGroup()
                ri.lastOpPar = currentInstruction.getGroupPar()
            codeSize += mop.getSize()
            bufferIndex += 1
            macroOpIndex += 1
            macroOpCount += 1

            if scheduleCycle >= RANDOMX_SUPERSCALAR_LATENCY:
                portsSaturated = True
            cycle = topCycle

            if macroOpIndex >= currentInstruction.getInfo().getSize():
                currentInstruction.toInstr(prog(programSize))
                programSize += 1
                mulCount += isMultiplication(currentInstruction.getType())
        cycle += 1
        decodeCycle += 1

    ipc = macroOpCount / retireCycle

    prog.asicLatencies = [0] * 8

    for i in range(programSize):
        instr = prog(i)
        latDst = prog.asicLatencies[instr.dst] + 1
        latSrc = prog.asicLatencies[instr.src] + 1 if instr.dst != instr.src else 0
        prog.asicLatencies[instr.dst] = max(latDst, latSrc)

    asicLatencyMax = 0
    addressReg = 0
    for i in range(8):
        if prog.asicLatencies[i] > asicLatencyMax:
            asicLatencyMax = prog.asicLatencies[i]
            addressReg = i
        prog.cpuLatencies[i] = registers[i].latency

    prog.setSize(programSize)
    prog.setAddressRegister(addressReg)

    prog.cpuLatency = retireCycle
    prog.asicLatency = asicLatencyMax
    prog.codeSize = codeSize
    prog.macroOps = macroOpCount
    prog.decodeCycles = decodeCycle
    prog.ipc = ipc
    prog.mulCount = mulCount


