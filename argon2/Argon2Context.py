from typing import Optional

class Argon2Context:
    def __init__(self, out: bytearray, outlen: int, pwd: bytearray, pwdlen: int,
                 salt: bytearray, saltlen: int, secret: Optional[bytearray],
                 secretlen: int, ad: Optional[bytearray], adlen: int,
                 t_cost: int, m_cost: int, lanes: int, version: int, threads: int):
        self.out = out
        self.outlen = outlen
        self.pwd = pwd
        self.pwdlen = pwdlen
        self.salt = salt
        self.saltlen = saltlen
        self.secret = secret
        self.secretlen = secretlen
        self.ad = ad
        self.adlen = adlen
        self.t_cost = t_cost
        self.m_cost = m_cost
        self.lanes = lanes
        self.version = version
        self.threads = threads
        self.allocate_cbk = None
        self.free_cbk = None
