def store32(dst, index, w):
    """
    Cette fonction prend un tableau 'dst', un index 'index' et un entier non signé de 32 bits 'w'.
    Elle stocke les 4 octets (32 bits) de 'w' dans le tableau 'dst' à partir de l'index spécifié
    dans l'ordre little-endian (c'est-à-dire l'octet de poids faible en premier).

    :param dst: bytearray où les octets doivent être stockés
    :param index: position à partir de laquelle les octets doivent être stockés dans 'dst'
    :param w: entier non signé de 32 bits dont les octets doivent être stockés
    """
    for i in range(4):
        dst[index + i] = w & 0xFF
        w >>= 8

