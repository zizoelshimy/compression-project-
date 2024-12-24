def compress(input):
    if not input:
        return ""

    compressed = []
    count = 1

    for i in range(1, len(input)):
        if input[i] == input[i - 1]:
            count += 1
        else:
            compressed.append(str(count) + input[i - 1])
            count = 1

    compressed.append(str(count) + input[-1])
    return "".join(compressed)

def compression_ratio(original, compressed):
    if not original:
        return 0  # To avoid division by zero
    return len(original) / len(compressed)

def decompress(input):
   if not input:
        return ""
   decoded_data = []
   i = 0
   while i < len(input):
      count_str = ""
      while i < len(input) and input[i].isdigit():
         count_str += input[i]
         i+= 1
      if i < len(input):
         char = input[i]
         count = int(count_str) if count_str else 1
         decoded_data.append(char * count)
         i += 1
   return "".join(decoded_data)