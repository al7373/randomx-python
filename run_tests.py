import os
import sys
import unittest

if __name__ == "__main__":
    test_dir = os.path.join(os.path.dirname(__file__), "test")
    suite = unittest.TestLoader().discover(start_dir=test_dir, pattern="*.py")
    unittest.TextTestRunner().run(suite)
