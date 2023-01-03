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

    
    hex_string = data[::-1].hex()
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

def decimal_to_binary(n, sampwidth, big_endian=False, signed=True):
    
    # Get binary_string in sampwidth-byte format
    binary_string = str(bin(abs(n)))[2:]
    binary_string = binary_string.rjust(sampwidth * 8, '0')
    binary_string = binary_string[::1]

    # if signed, get twos complement
    if (signed and n < 0):
        binary_string = ['0' if b == '1' else '1' for b in binary_string]

        complete = False
        binary_string = binary_string[::-1]
        big_endian = not big_endian

        i = 0
        while complete == False:
            b = binary_string[i]
            if (b == '1'):
                binary_string[i] = '0'
            else:
                binary_string[i] = '1'
                complete = True

    if (not big_endian):
        binary_string = binary_string[::-1]
    
    binary_string = "".join(binary_string)
    return binary_string

def binary_to_bytes(n):
    # n     -- little-endian binary number

    bin_to_hex = {
        '0000': '0',
        '0001': '1',
        '0010': '2',
        '0011': '3',
        '0100': '4',
        '0101': '5',
        '0110': '6',
        '0111': '7',
        '1000': '8',
        '1001': '9',
        '1010': 'a',
        '1011': 'b',
        '1100': 'c',
        '1101': 'd',
        '1110': 'e',
        '1111': 'f',
    }
    segments = []
    for i in range(len(n)//4):
        segments.append(n[i * 4: (i+1) * 4])
    
    byte_array = [bin_to_hex[segment] for segment in segments]

    byte_array = [byte_array[i*2] + byte_array[i*2 + 1] for i in range(len(byte_array)//2)]
    barray = [bytes.fromhex(segment) for segment in byte_array]
    bstring = b"".join(barray)
    return bstring