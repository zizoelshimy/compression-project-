import math
import numpy as np

def golomb_encode(data, m):
    b = math.ceil(math.log2(m))
    encoded_data = []
    for number in data:
        q = number // m  # Quotient
        r = number % m  # Remainder
        # Unary code for quotient
        unary_code = '1' * q + '0'
        # Binary code for remainder
        if (1 << b) - m > r:
            b -= 1
        binary_code = format(r, f'0{b}b')
        # Combine unary and binary codes
        encoded_data.append(unary_code + binary_code)
    return encoded_data

def golomb_decode(encoded_data, m):
    
    decoded_data = []
    for code in encoded_data:
        # Separate the unary and binary parts
        unary_part = code.split('0', 1)[0]
        remainder_part = code[len(unary_part) + 1:]

        # Compute the quotient from the unary part
        q = len(unary_part)

        # Compute the binary length for the remainder
        b = math.ceil(math.log2(m))
        if (1 << b) - m > int(remainder_part, 2):
            b -= 1

        # Compute the remainder from the binary part
        r = int(remainder_part, 2)

        # Decode the original number
        number = q * m + r
        decoded_data.append(number)

    return decoded_data

def compute_compression_ratio(original_data, encoded_data):
    
    original_size = len(original_data) * 32  # Assuming 32-bit integers
    compressed_size = sum(len(bitstream) for bitstream in encoded_data)
    return original_size / compressed_size

def compute_golomb_m(data):
    # Calculate the mean of the input data
    mean = sum(data) / len(data)

    # Find the closest power of 2 to the mean
    m = 2 ** round(math.log2(mean))
    return m