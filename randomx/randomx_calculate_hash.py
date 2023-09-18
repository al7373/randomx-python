from .configuration import RANDOMX_PROGRAM_COUNT 
from .const import RANDOMX_HASH_SIZE
from virtual_machine.randomx_vm import randomx_vm
from blake2b.blake2b import blake2b

def randomx_calculate_hash(machine: randomx_vm, _input: bytearray, inputSize: int, output: bytearray) -> None:
        tempHash = bytearray(64)
        blakeResult = blake2b(tempHash, len(tempHash), _input, inputSize, None, 0)
        machine.initScratchpad(tempHash)
		# machine->resetRoundingMode();
        for chain in range(RANDOMX_PROGRAM_COUNT - 1):
            machine.run(tempHash)
            reg = machine.getRegisterFile().to_bytes()
            blakeResult = blake2b(tempHash, len(tempHash), reg, len(reg), None, 0)
        machine.run(tempHash)
        machine.getFinalResult(output, RANDOMX_HASH_SIZE)

