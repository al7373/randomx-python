from .configuration import RANDOMX_ARGON_SALT, RANDOMX_ARGON_LANES, RANDOMX_ARGON_MEMORY, RANDOMX_ARGON_ITERATIONS, RANDOMX_CACHE_ACCESSES 
from .const import ArgonSaltSize
from argon2.const import ARGON2_SYNC_POINTS, ARGON2_VERSION_NUMBER, ARGON2_OK 
from argon2.Argon2Context import Argon2Context
from argon2.Argon2Instance import Argon2Instance 
from argon2.randomx_argon2_validate_inputs import randomx_argon2_validate_inputs 
from argon2.randomx_argon2_initialize import randomx_argon2_initialize 
from argon2.randomx_argon2_fill_memory_blocks import randomx_argon2_fill_memory_blocks 
from argon2.Argon2Type import Argon2Type
from .randomx_reciprocal import randomx_reciprocal
from superscalar.SuperscalarInstructionType import SuperscalarInstructionType
from blake2b.Blake2Generator import Blake2Generator
from .RandomxCache import RandomxCache
from superscalar.generateSuperscalar import generateSuperscalar 
from superscalar.SuperscalarProgram import SuperscalarProgram

def initCache(cache: RandomxCache, key, key_size: int):
    memory_blocks: int
    segment_length: int
    context: Argon2Context

    keyInBytes = key.encode('utf-8')

    context = Argon2Context(
        out=None,
        outlen=0,
        pwd=keyInBytes,
        pwdlen=key_size,
        salt=RANDOMX_ARGON_SALT.encode('utf-8'),
        saltlen=ArgonSaltSize,
        secret=None,
        secretlen=0,
        ad=None,
        adlen=0,
        t_cost=RANDOMX_ARGON_ITERATIONS,
        m_cost=RANDOMX_ARGON_MEMORY,
        lanes=RANDOMX_ARGON_LANES,
        version=ARGON2_VERSION_NUMBER,
        threads=1
    )

    inputs_valid = randomx_argon2_validate_inputs(context)
    assert inputs_valid == ARGON2_OK

    memory_blocks = context.m_cost
    segment_length = memory_blocks // (context.lanes * ARGON2_SYNC_POINTS)

    instance = Argon2Instance(
        memory=cache.memory,
        version=context.version,
        passes=context.t_cost,
        memory_blocks=memory_blocks,
        segment_length=segment_length,
        lane_length=segment_length * ARGON2_SYNC_POINTS,
        lanes=context.lanes,
        threads=context.threads,
        argon2_type=Argon2Type.Argon2_d,
        print_internals=0,
        context_ptr=context,
        randomx_argon2_impl=cache.argonImpl
    )

    if instance.threads > instance.lanes:
        instance.threads = instance.lanes

    randomx_argon2_initialize(instance, context)
    randomx_argon2_fill_memory_blocks(instance)

    cache.reciprocalCache.clear()
    gen = Blake2Generator(keyInBytes, key_size)
    for i in range(RANDOMX_CACHE_ACCESSES):
        prog = SuperscalarProgram()
        generateSuperscalar(prog, gen)
        cache.programs[i] = prog
        for j in range(cache.programs[i].getSize()):
            instr = cache.programs[i](j)
            if SuperscalarInstructionType(instr.opcode) == SuperscalarInstructionType.IMUL_RCP:
                rcp = randomx_reciprocal(instr.getImm32())
                instr.setImm32(len(cache.reciprocalCache))
                cache.reciprocalCache.append(rcp)

