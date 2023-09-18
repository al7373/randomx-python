
def extend_to_128bits(n: int) -> int:
    # Masque pour obtenir le bit de signe (position 63) de l'entier 64 bits
    sign_bit_mask = 1 << 63

    # Récupère le bit de signe de l'entier 64 bits
    sign_bit = n & sign_bit_mask

    if sign_bit:
        # Si le bit de signe est 1, c'est-à-dire que l'entier est négatif,
        # on étend en ajoutant des 1 sur les 64 bits les plus significatifs.
        signed_128bit = (0xFFFFFFFFFFFFFFFF << 64) | n
    else:
        # Si le bit de signe est 0, c'est-à-dire que l'entier est positif ou nul,
        # on étend en ajoutant des 0 sur les 64 bits les plus significatifs.
        signed_128bit = n

    return signed_128bit

def smulh(a: int, b: int) -> int:
    _a = a & 0xFFFFFFFFFFFFFFFF
    _b = b & 0xFFFFFFFFFFFFFFFF
    _a = extend_to_128bits(_a)
    _b = extend_to_128bits(_b)
    return ((_a * _b) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF) >> 64

