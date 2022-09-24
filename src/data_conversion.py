# This file contains data conversion functions to convert between bases

def bytes_to_binary(data):
    # Converts bytes object to binary string
    if data == None or data == b'':
        return ''

    hex_to_bin = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'a': '1010',
        'b': '1011',
        'c': '1100',
        'd': '1101',
        'e': '1110',
        'f': '1111',
    }

    
    hex_string = data.hex()
    bin_string = ""
        
    # Loop over first and second nibbles of each byte, and append each byte in a binary string format
    for c in hex_string:
        bin_string += hex_to_bin[c]
    
    return bin_string

def binary_to_decimal(n, big_endian=False, signed=True):
    # Converts binary string to decimal
    if n == '':
        return 0
    value = 0

    # Convert to 'big endian' format if originally little endian
    if big_endian == True:
        n = n[::-1]

    # Sum over all but last bit
    for i in range(len(n) - 1):
        value += int(n[i]) * 2**(i)
    
    # Get value of MSB if signed
    msb = int(n[-1]) * 2**(len(n) - 1)
    if msb and signed:
        msb *= -1
    value += msb

    return value

def decimal_to_binary(data):
    pass

def binary_to_bytes(data):
    pass
