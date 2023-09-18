from .const import ARGON2_INCORRECT_PARAMETER, \
ARGON2_PWD_PTR_MISMATCH, \
ARGON2_MIN_PWD_LENGTH, \
ARGON2_MAX_PWD_LENGTH, \
ARGON2_PWD_TOO_SHORT, \
ARGON2_PWD_TOO_LONG, \
ARGON2_SALT_PTR_MISMATCH, \
ARGON2_MIN_SALT_LENGTH, \
ARGON2_MAX_SALT_LENGTH, \
ARGON2_SALT_TOO_SHORT, \
ARGON2_SALT_TOO_LONG, \
ARGON2_SECRET_PTR_MISMATCH, \
ARGON2_MIN_SECRET, \
ARGON2_MAX_SECRET, \
ARGON2_SECRET_TOO_SHORT, \
ARGON2_SECRET_TOO_LONG, \
ARGON2_AD_PTR_MISMATCH, \
ARGON2_MIN_AD_LENGTH, \
ARGON2_MAX_AD_LENGTH, \
ARGON2_AD_TOO_SHORT, \
ARGON2_AD_TOO_LONG, \
ARGON2_MEMORY_TOO_LITTLE, \
ARGON2_MAX_MEMORY, \
ARGON2_MEMORY_TOO_MUCH, \
ARGON2_TIME_TOO_SMALL, \
ARGON2_MIN_TIME, \
ARGON2_MAX_TIME, \
ARGON2_TIME_TOO_LARGE, \
ARGON2_LANES_TOO_FEW, \
ARGON2_MIN_LANES, \
ARGON2_MAX_LANES, \
ARGON2_LANES_TOO_MANY, \
ARGON2_THREADS_TOO_FEW, \
ARGON2_MIN_THREADS, \
ARGON2_MAX_THREADS, \
ARGON2_THREADS_TOO_MANY, \
ARGON2_FREE_MEMORY_CBK_NULL, \
ARGON2_ALLOCATE_MEMORY_CBK_NULL, \
ARGON2_OK, \
ARGON2_MIN_MEMORY

from .Argon2Context import Argon2Context 

def randomx_argon2_validate_inputs(context: Argon2Context) -> int:
    if context is None:
        return ARGON2_INCORRECT_PARAMETER

    if context.pwd is None:
        if context.pwdlen != 0:
            return ARGON2_PWD_PTR_MISMATCH
    else:
        if ARGON2_MIN_PWD_LENGTH > context.pwdlen:
            return ARGON2_PWD_TOO_SHORT
        if ARGON2_MAX_PWD_LENGTH < context.pwdlen:
            return ARGON2_PWD_TOO_LONG

    if context.salt is None:
        if context.saltlen != 0:
            return ARGON2_SALT_PTR_MISMATCH
    else:
        if ARGON2_MIN_SALT_LENGTH > context.saltlen:
            return ARGON2_SALT_TOO_SHORT
        if ARGON2_MAX_SALT_LENGTH < context.saltlen:
            return ARGON2_SALT_TOO_LONG

    if context.secret is None:
        if context.secretlen != 0:
            return ARGON2_SECRET_PTR_MISMATCH
    else:
        if ARGON2_MIN_SECRET > context.secretlen:
            return ARGON2_SECRET_TOO_SHORT
        if ARGON2_MAX_SECRET < context.secretlen:
            return ARGON2_SECRET_TOO_LONG

    if context.ad is None:
        if context.adlen != 0:
            return ARGON2_AD_PTR_MISMATCH
    else:
        if ARGON2_MIN_AD_LENGTH > context.adlen:
            return ARGON2_AD_TOO_SHORT
        if ARGON2_MAX_AD_LENGTH < context.adlen:
            return ARGON2_AD_TOO_LONG

    if ARGON2_MIN_MEMORY > context.m_cost:
        return ARGON2_MEMORY_TOO_LITTLE
    if ARGON2_MAX_MEMORY < context.m_cost:
        return ARGON2_MEMORY_TOO_MUCH
    if context.m_cost < 8 * context.lanes:
        return ARGON2_MEMORY_TOO_LITTLE

    if ARGON2_MIN_TIME > context.t_cost:
        return ARGON2_TIME_TOO_SMALL
    if ARGON2_MAX_TIME < context.t_cost:
        return ARGON2_TIME_TOO_LARGE

    if ARGON2_MIN_LANES > context.lanes:
        return ARGON2_LANES_TOO_FEW
    if ARGON2_MAX_LANES < context.lanes:
        return ARGON2_LANES_TOO_MANY

    if ARGON2_MIN_THREADS > context.threads:
        return ARGON2_THREADS_TOO_FEW
    if ARGON2_MAX_THREADS < context.threads:
        return ARGON2_THREADS_TOO_MANY

    if context.allocate_cbk is not None and context.free_cbk is None:
        return ARGON2_FREE_MEMORY_CBK_NULL

    if context.allocate_cbk is None and context.free_cbk is not None:
        return ARGON2_ALLOCATE_MEMORY_CBK_NULL

    return ARGON2_OK

