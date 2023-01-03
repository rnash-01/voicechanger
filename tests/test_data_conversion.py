import unittest
import set_test_env
from data_conversion import *

class TestDataConversion(unittest.TestCase):
    
    def test_bytes_to_binary(self):
        self.assertEqual(bytes_to_binary(b'\x00\x01\x02\x03\x04'), '0000010000000011000000100000000100000000')
        self.assertEqual(bytes_to_binary(b'\xff\x04'), '0000010011111111')
        self.assertEqual(bytes_to_binary(b'\xf0'), '11110000')
        self.assertEqual(bytes_to_binary(b''), '')
        self.assertEqual(bytes_to_binary(None), '')
    
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
            self.assertEqual(binary_to_decimal(bin_string, big_endian=True, signed=False), 2**i)
            bin_string = bin_string + '0'

        bin_string = '0101' # 5
        self.assertEqual(binary_to_decimal(bin_string, big_endian=True, signed=False), 5)

        bin_string = '1100' # 12
        self.assertEqual(binary_to_decimal(bin_string, big_endian=True, signed=False), 12)

        bin_string = ''
        self.assertEqual(binary_to_decimal(bin_string, big_endian=True, signed=False), 0)

    def test_decimal_to_binary(self):
        # Signed

        # Little endian
        n = 128
        self.assertEqual(decimal_to_binary(n, 2, False, True), '0000000100000000')
        
        n = -128
        self.assertEqual(decimal_to_binary(n, 2, False, True), '1111111011111111')

        n = 0
        self.assertEqual(decimal_to_binary(n, 2, False, True), '0000000000000000')
        
        n = 1
        self.assertEqual(decimal_to_binary(n, 2, False, True), '1000000000000000')

        # Big Endian
        n = 128
        self.assertEqual(decimal_to_binary(n, 2, True, True), '0000000010000000')
        
        n = -128
        self.assertEqual(decimal_to_binary(n, 2, True, True), '1111111101111111')

        n = 0
        self.assertEqual(decimal_to_binary(n, 2, True, True), '0000000000000000')
        
        n = 1
        self.assertEqual(decimal_to_binary(n, 2, True, True), '0000000000000001')


        # Unsigned
        
        # Little endian
        n = 128
        self.assertEqual(decimal_to_binary(n, 2, False, True), '0000000100000000')
        
        n = 65407
        self.assertEqual(decimal_to_binary(n, 2, False, True), '1111111011111111')

        n = 0
        self.assertEqual(decimal_to_binary(n, 2, False, True), '0000000000000000')
        
        n = 1
        self.assertEqual(decimal_to_binary(n, 2, False, True), '1000000000000000')

        # Big Endian
        n = 128
        self.assertEqual(decimal_to_binary(n, 2, True, True), '0000000010000000')
        
        n = 65407
        self.assertEqual(decimal_to_binary(n, 2, True, True), '1111111101111111')

        n = 0
        self.assertEqual(decimal_to_binary(n, 2, True, True), '0000000000000000')
        
        n = 1
        self.assertEqual(decimal_to_binary(n, 2, True, True), '0000000000000001')

    def test_binary_to_bytes(self):
        # 0
        binary = '0000000000000000'
        self.assertEqual(binary_to_bytes(binary), b'\x00\x00')

        # 1
        binary = '1000000000000000'
        self.assertEqual(binary_to_bytes(binary), b'\x80\x00')

        # 128
        binary = '0000000100000000'
        self.assertEqual(binary_to_bytes(binary), b'\x01\x00')

        # -128
        binary = '1111111011111111'
        self.assertEqual(binary_to_bytes(binary), b'\xfe\xff')
        
if __name__ == '__main__':
    unittest.main()