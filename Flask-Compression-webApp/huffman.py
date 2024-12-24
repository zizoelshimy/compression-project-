import heapq
from collections import Counter
import json

def huffman_encode(text):
    """Encodes text using Huffman coding and returns the tree structure and compression ratio."""
    # Step 1: Count the frequency of each character in the text
    frequency = Counter(text)

    # Step 2: Create a priority queue (min-heap) to build the Huffman tree
    heap = [[weight, [char, ""]] for char, weight in frequency.items()]
    heapq.heapify(heap)

    # Step 3: Build the Huffman Tree
    huffman_tree = []
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        new_node = [lo[0] + hi[0]] + lo[1:] + hi[1:]
        huffman_tree.append([lo,hi])
        heapq.heappush(heap, new_node)
    huffman_codes = sorted(heap[0][1:], key=lambda p: (len(p[1]), p))
    huffman_dict = {char: code for char, code in huffman_codes}
    
    # Step 5: Encode the text using the Huffman codes
    try:
      encoded_text = "".join(huffman_dict[char] for char in text)
      
    except KeyError as e:
      print(f"Character '{e.args[0]}' is not in the Huffman dictionary.")
      return None, None, None, None
    
    
    #Calculate compression ratio
    original_size = len(text) * 8  #Assuming 8 bits per character
    compressed_size = len(encoded_text)
    compression_ratio = original_size / compressed_size if compressed_size else 0
    
    return encoded_text, huffman_dict, huffman_tree, compression_ratio
    

def huffman_decode(encoded_text, huffman_dict):
    """Decodes text using Huffman coding."""
    # Step 7: Decompress the encoded text
    # Reverse the Huffman dictionary for decoding
    reverse_huffman_dict = {code: char for char, code in huffman_dict.items()}

    # Decode the encoded text
    decoded_text = ""
    current_code = ""

    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_huffman_dict:
            decoded_text += reverse_huffman_dict[current_code]
            current_code = ""

    return decoded_text