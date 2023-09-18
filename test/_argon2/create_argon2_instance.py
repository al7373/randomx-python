from argon2.rxa2_fill_first_blocks import rxa2_fill_first_blocks 
from argon2.rxa2_initial_hash import rxa2_initial_hash  
from argon2.Argon2Instance import Argon2Instance 
from argon2.Argon2Context import Argon2Context 
from argon2.Argon2Type import Argon2Type   
from argon2.Block import Block
from argon2.const import ARGON2_PREHASH_SEED_LENGTH, ARGON2_SYNC_POINTS, ARGON2_QWORDS_IN_BLOCK

def create_argon2_instance():
    # Paramètres de test
    outlen = 0
    pwd = bytes.fromhex("52616e646f6d58206578616d706c65206b657900")
    pwdlen = 20
    salt = bytes.fromhex("52616e646f6d5803")
    saltlen = 8
    secret = None
    secretlen = 0
    ad = None
    adlen = 0
    t_cost = 3
    m_cost = 262144
    lanes = 1
    version = 19
    threads = 1

    # Initialisation de Argon2Context
    context = Argon2Context(
        out=bytearray(outlen),
        outlen=outlen,
        pwd=pwd,
        pwdlen=pwdlen,
        salt=salt,
        saltlen=saltlen,
        secret=secret,
        secretlen=secretlen,
        ad=ad,
        adlen=adlen,
        t_cost=t_cost,
        m_cost=m_cost,
        lanes=lanes,
        version=version,
        threads=threads
    )

    # Créer une instance d'Argon2
    memory_blocks = context.m_cost
    segment_length = memory_blocks // (lanes * ARGON2_SYNC_POINTS)
    lane_length = segment_length * ARGON2_SYNC_POINTS

    memory = [Block([0] * ARGON2_QWORDS_IN_BLOCK) for _ in range(memory_blocks * lanes)]

    instance = Argon2Instance(
        memory=memory,
        version=context.version,
        passes=context.t_cost,
        memory_blocks=memory_blocks,
        segment_length=segment_length,
        lane_length=lane_length,
        lanes=lanes,
        threads=context.threads,
        argon2_type=Argon2Type.Argon2_d,
        print_internals=-8192,
        context_ptr=None,
        randomx_argon2_impl=None
    )

    return instance, context

