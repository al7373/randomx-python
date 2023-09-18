import unittest
from blake2b.BLAKE2_ROUND_NOMSG import BLAKE2_ROUND_NOMSG

class TestBlake2RoundNoMsg(unittest.TestCase):

    def test_BLAKE2_ROUND_NOMSG(self):
        result = BLAKE2_ROUND_NOMSG(
            0x1111111111111111, 0x2222222222222222, 0x3333333333333333, 0x4444444444444444,
            0x5555555555555555, 0x6666666666666666, 0x7777777777777777, 0x8888888888888888,
            0x9999999999999999, 0xaaaaaaaaaaaaaaaa, 0xbbbbbbbbbbbbbbbb, 0xcccccccccccccccc,
            0xdddddddddddddddd, 0xeeeeeeeeeeeeeeee, 0xffffffffffffffff, 0x0000000000000000
        )
        expected = (
            0x7063721628c98c77, 0x6ceb79a889331970, 0x0a4e76ee1c9f5c6a, 0x1639ee90875ba25c,
            0xd567c8b41f9af32e, 0x069517d73086b2c3, 0x29b617b017462324, 0xe684f253eb2fbfa0,
            0x588bd9334f4e5b4b, 0x6e992a5b9040e5c9, 0x70fe6c1a7ce404ed, 0x2708078365af703e,
            0x6dcb3fe65a59ef24, 0xc97f9d15b189cbbe, 0x679ad7ece86f5494, 0x279d4cf03e16e920
        )
        self.assertEqual(result, expected)

