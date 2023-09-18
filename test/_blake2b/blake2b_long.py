import unittest
from typing import Tuple
from blake2b.blake2b_long import blake2b_long

class TestBlake2bLong(unittest.TestCase):
    def test_basic_functionality(self):
        test_cases = [
            (bytes.fromhex('010203040506070809'), 64, 'fc6a35640843cae6297ac4e8622579cab11a1d9b64f35b38fda5d7a1e5322dab0f03db420dafbf92b67a0fc5d8edad392d554b23046cad9a5ebe53e2b0a579cb'),
            (b"OpenAI", 32, '327a4c8c27a66b41e11586d8a83f887b81913eeb93bbb5a3218b64f67a53a043'),
            (b"OpenAI", 1024, '2974b37e22ba339d1152414a566cc10347d448d4ca701c447265ef6ba5942cb28adadbd863f18757647f8275959d8f4d0af637fd0158988d7a49aad42c7f6773c219c1429a8b6c46eba5703a7b2b6b22d64d9ebf74b8547eb3996bbea9b516df40744901a6015fb5f2bb75541886648a714d733d2f883d72b920e4038d76a05534aebfb4ce911d8f67089dabc4c5a15440a72b59413853268c053764990954b8a4baeae569da0e9893f39187982de25f50821e7b6eb2b4136f5af966222b28271fc9399b9303b07ef559ddf23711011ebee6985f3c5715d82dc1f322183b66d407b84223acc6e23ea50ad49cb09be0e466995cf481652518307791691191e56886e0f16a891d6dd411e7b453d59ea4e141f85a375a535f77a2b0fc5d21729f3378ef033bf8d5661be4ffb397f65df150b2de2c65d7079d92f6f434d33c390046b3e1c87d9e751744a74bc07f27dfe3dd25ca80e76957c8e47e4962b74a24e9586406e063a086f154f4e391651cd086bacb718eb0fb0c5b6846847aa975650cb4af0b2361aed81eb7dbcf1fb32c09d5d9bf3028eb967a2efc4721ab59ab7b1e01aa9a42ab7efcc8788a106dc9e2ca564a8ce33e37fda0b075b120ae9badc06f0809e4e6c4fd3ae9fb8c98c05ad19970443067b0be1eda976f32b5a0fceea697ec17f185364b97cd95baca0e679d7b7ab7d65c10835f9609dbb3f6766b5ac684beabe797d094a9a5b19b0a3ac55656d14ea1ed3d292c59fe69a88da617e3d3f37802138101682a216d46014e74971f9cf4de3516c44f065ac9da31136fa5c29d1d44d99a03e9c202095323a62ce582a4354769f09764d0a9d834e62ddcdd985afb8db868f3eb8b0f5952ff921a3670f186b6e2c9884721febfa4e2c859f1ec64f8b8d531aaa8f1e9cd25d2e46c2b5a9f2ed569ecf224d6df1a10edb8fdf27157ccef75c1860319705f6005fd9bfde859a4f6076d446313a92d2801a2fc1e3c29208f4c1cfad8295284d7aa97e8efc7969210f0c2654096b97b2ecee3684b3796ddd7376190fb56e58abb7ac16083ab48e707a6b01f17a3f211cfd8b5dee171cfeeb28b48e230e38e7613713f9bd932727397682c083b8ce77118a39f02759aaf89ae890d753745106b9bd69549ed037ebf28957f3d0c1545c6588b98956b07ee8a65bd66d4e2056f7ac603250b4bb62025540ab6b47a02623469a71585cf42a9798c41c441523cb48a1db6862ae2b8a3c23cbdc52ab304fd55f46439428d72166a6fe94770c62f068f60c303b27c13e3ee1fed1527642fa4a3795d68a872a4a9254bfa21d398cd0d38e6f7e64480502df6e9883fb3b69e4df1fd11693e1aa8c87389af249c4fcb59712742e3551ed34f933bf05abe19830e463bd5b88fe4211e83d779186e0d28f6342f8823a7cc8164eac5a6269e491dea607affe15919cab7e4'),
        ]

        for in_data, outlen, expected_hex in test_cases:
            out = bytearray(outlen)
            ret = blake2b_long(out, outlen, in_data, len(in_data))
            self.assertEqual(ret, 0)
            self.assertEqual(out.hex(), expected_hex)

    def test_negative_outlen(self):
        outlen = -1
        out = bytearray(1)  # Utilisez une taille de sortie valide
        in_data = b"Negative outlen test"
        ret = blake2b_long(out, outlen, in_data, len(in_data))
        self.assertEqual(ret, -1)

    def test_zero_outlen(self):
        outlen = 0
        out = bytearray(1)  # Utilisez une taille de sortie valide
        in_data = b"Zero outlen test"
        ret = blake2b_long(out, outlen, in_data, len(in_data))
        self.assertEqual(ret, -1)


