import heapq
from collections import Counter, namedtuple

# HuffmanNode class
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Define comparison operators for priority queue
    def __lt__(self, other):
        return self.freq < other.freq

# Build Huffman Tree
def build_huffman_tree(freq_map):
    priority_queue = [HuffmanNode(char, freq) for char, freq in freq_map.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)

    return priority_queue[0]

# Generate Huffman Codes
def generate_huffman_codes(root, current_code, codes):
    if root is None:
        return

    if root.char is not None:
        codes[root.char] = current_code

    generate_huffman_codes(root.left, current_code + "0", codes)
    generate_huffman_codes(root.right, current_code + "1", codes)

# Decode Huffman Encoded String
def huffman_decoding(encoded_string, root):
    decoded_string = []
    current_node = root
    for bit in encoded_string:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:  # Reached a leaf node
            decoded_string.append(current_node.char)
            current_node = root  # Reset to the root for the next character

    return ''.join(decoded_string)

# Main Function
def huffman_encoding(input_string):
    # Count frequency of each character
    freq_map = Counter(input_string)

    # Build Huffman Tree
    root = build_huffman_tree(freq_map)

    # Generate Huffman Codes
    codes = {}
    generate_huffman_codes(root, "", codes)

    # Encode the string
    encoded_string = "".join(codes[char] for char in input_string)
    return codes, encoded_string, root

# Input from user
if __name__ == "__main__":
    String_to_encode = input("Enter a string to encode: ")
    codes, encoded_string, root = huffman_encoding(String_to_encode)
    print("Huffman Codes:", codes)
    print("Encoded String:", encoded_string)

    binary_to_decode = input("Enter a binary to decode: ")
    decoded_string = huffman_decoding(binary_to_decode, root)
    print("Decoded String:", decoded_string)
