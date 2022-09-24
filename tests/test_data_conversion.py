import unittest
import set_test_env
from data_conversion import *

class TestDataConversion(unittest.TestCase):
    
    def test_bytes_to_binary(self):
        self.assertEqual(bytes_to_binary(b'\x00\x01\x02\x03\x04', '0000000000000001000000100000001100000100'))
        self.assertEqual(bytes_to_binary(b'\xff\x04', '1111111100000100'))
        self.assertEqual(bytes_to_binary(b'\xf0', '11110000'))
        self.assertEqual(bytes_to_binary(b'', ''))
        self.assertEqual(bytes_to_binary(None, ''))
    
    def test_binary_to_decimal(self):
        # Test little-endian signed numbers
        bin_string = '1'
        for i in range(16):
            self.assertEqual(binary_to_decimal(bin_string), -(2**i))
            bin_string = '0' + bin_string
        
        bin_string = '0101' # -6
        self.assertEqual(binary_to_decimal(bin_string), -6)

        bin_string = '1100'
        self.assertEqual(binary_to_decimal(bin_string), 3)

        bin_string = ''
        self.assertEqual(binary_to_decimal(bin_string), 0)

        # Test little-endian unsigned numbers
        bin_string = '1'
        for i in range(16):
            self.assertEqual(binary_to_decimal(bin_string, signed=False), 2**i)
            bin_string = '0' + bin_string

        bin_string = '0101' # 10
        self.assertEqual(binary_to_decimal(bin_string, signed=False), 10)

        bin_string = '1100'
        self.assertEqual(binary_to_decimal(bin_string, signed=False), 3)

        bin_string = ''
        self.assertEqual(binary_to_decimal(bin_string, signed=False), 0)

        # Test big-endian signed numbers
        bin_string = '1'
        for i in range(16):
            self.assertEqual(binary_to_decimal(bin_string, big_endian=True), -2**i)
            bin_string = bin_string + '0'

        bin_string = '0101' # 5
        self.assertEqual(binary_to_decimal(bin_string, big_endian=True), 5)

        bin_string = '1100' # -4
        self.assertEqual(binary_to_decimal(bin_string, big_endian=True), -4)

        bin_string = ''
        self.assertEqual(binary_to_decimal(bin_string, big_endian=True), 0)

        # Test big-endian unsigned numbers
        bin_string = '1'
        for i in range(16):
            self.assertEqual(binary_to_decimal(bin_string, big_endian=True, signed=False), -2**i)
            bin_string = bin_string + '0'

        bin_string = '0101' # 5
        self.assertEqual(binary_to_decimal(bin_string, big_endian=True, signed=False), 5)

        bin_string = '1100' # 10
        self.assertEqual(binary_to_decimal(bin_string, big_endian=True, signed=False), 10)

        bin_string = ''
        self.assertEqual(binary_to_decimal(bin_string, big_endian=True, signed=False), 0)

if __name__ == '__main__':
    unittest.main()