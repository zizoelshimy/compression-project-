import heapq
from collections import Counter

# Step 1: Count the frequency of each character in the text
with open('text.txt', 'r') as file:
    text = file.read()
frequency = Counter(text)
print(f"Character frequencies: {frequency}")

print('*********************************************')

# Step 2: Create a priority queue (min-heap) to build the Huffman tree
heap = [[weight, [char, ""]] for char, weight in frequency.items()]
heapq.heapify(heap)
print(f"Initial heap: {heap}")

# Step 3: Build the Huffman Tree
while len(heap) > 1:
    lo = heapq.heappop(heap)
    hi = heapq.heappop(heap)
    for pair in lo[1:]:
        pair[1] = '0' + pair[1]
    for pair in hi[1:]:
        pair[1] = '1' + pair[1]
    heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

print(f"Huffman tree: {heap[0][1:]}")
print('**************************************************')

# Step 4: Create a dictionary with the Huffman codes for each character
huffman_codes = sorted(heap[0][1:], key=lambda p: (len(p[1]), p))
print(f"Sorted Huffman codes: {huffman_codes}")
huffman_dict = {char: code for char, code in huffman_codes}
print(f"Huffman dictionary: {huffman_dict}")

# Step 5: Encode the text using the Huffman codes
try:
    encoded_text = "".join(huffman_dict[char] for char in text)
    print(f"Encoded text: {encoded_text}")
except KeyError as e:
    print(f"Character '{e.args[0]}' is not in the Huffman dictionary.")

# Step 6: Calculate the compression ratio
original_size = len(text) * 8  # Size in bits (1 character = 8 bits)
encoded_size = len(encoded_text)  # Size in bits (encoded text)
compression_ratio = original_size / encoded_size if encoded_size > 0 else 0
print(f"Original size (in bits): {original_size}")
print(f"Encoded size (in bits): {encoded_size}")
print(f"Compression Ratio: {compression_ratio:.2f}")

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

print(f"Decoded text: {decoded_text}")
