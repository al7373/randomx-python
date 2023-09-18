import unittest
from argon2.randomx_argon2_validate_inputs import randomx_argon2_validate_inputs
from argon2.Argon2Context import Argon2Context 
from argon2.const import *

class TestRandomXArgon2ValidateInputs(unittest.TestCase):

    def test_correct_parameters(self):
        context = Argon2Context(
            out=bytearray(32),
            outlen=32,
            pwd=bytearray(b"password"),
            pwdlen=8,
            salt=bytearray(b"somesalt"),
            saltlen=8,
            secret=None,
            secretlen=0,
            ad=None,
            adlen=0,
            t_cost=3,
            m_cost=ARGON2_MIN_MEMORY,
            lanes=ARGON2_MIN_LANES,
            version=1,
            threads=1,
        )
        result = randomx_argon2_validate_inputs(context)
        self.assertEqual(result, ARGON2_OK)

    def test_null_context(self):
        context = None
        result = randomx_argon2_validate_inputs(context)
        self.assertEqual(result, ARGON2_INCORRECT_PARAMETER)

    def test_invalid_pwd_length(self):
        context = Argon2Context(
            out=bytearray(32),
            outlen=32,
            pwd=None,
            pwdlen=1,
            salt=bytearray(b"somesalt"),
            saltlen=8,
            secret=None,
            secretlen=0,
            ad=None,
            adlen=0,
            t_cost=3,
            m_cost=ARGON2_MIN_MEMORY,
            lanes=ARGON2_MIN_LANES,
            version=1,
            threads=1
        )
        result = randomx_argon2_validate_inputs(context)
        self.assertEqual(result, ARGON2_PWD_PTR_MISMATCH)

    # Ajoutez d'autres tests pour couvrir différents cas d'erreur et de succès.

