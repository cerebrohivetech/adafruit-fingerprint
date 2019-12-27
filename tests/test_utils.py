# Standard library imports
import unittest


# Adafruit imports
from adafruit_fingerprint.utils import hexbyte_2integer_normalizer


class UtilsTest(unittest.TestCase):
    def test_hexbyte_2integer_normalizer(self):
        normalized_int_bytes = hexbyte_2integer_normalizer(1, 1)
        self.assertEqual(normalized_int_bytes, 257)
