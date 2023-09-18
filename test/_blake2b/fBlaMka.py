import unittest
from blake2b.fBlaMka import fBlaMka

class TestfBlaMka(unittest.TestCase):

    def test_fBlaMka(self):
        x = 4652451441051634588
        y = 4417718805361862693
        e = 10904175292755824345 
        z = fBlaMka(x, y)
        self.assertEqual(z, e)

