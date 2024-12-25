import re
import math
import numpy as np
from scipy.stats import skew

def read_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data

def clean_to_alphanumeric(data):
    return re.sub(r'[^a-zA-Z0-9]', '', data)

def check_file_type(data):
    if data.isdigit():
        return True
    else:
        return False

def calculate_frequency(data):
    frequency = {}
    for char in data:
        frequency[char] = frequency.get(char, 0) + 1
    return frequency

def calculate_text_entropy(data):
    frequency = calculate_frequency(data)
    total_chars = len(data)
    entropy = 0
    for count in frequency.values():
        probability = count / total_chars
        entropy -= probability * math.log2(probability)

    if   5 <= entropy <= 8:
        complexity = "The text is complex"
    elif 3 <= entropy < 5:
        complexity = "The text is moderate"
    else:
        complexity = "The text is simple"

    return {
        "entropy": entropy,
        "complexity": complexity
    }

def check_skewness(data):
   
    if len(data) < 3:
        print("Not enough data to calculate the skewness.")
        return None

    data_skew = skew(data)
    print(f"Skewness: {data_skew:.4f}")
    if data_skew < -1:
        print("Data is highly skewed to the left (Negatively Skewed).")
    elif data_skew > 1:
        print("Data is highly skewed to the right (Positively Skewed).")
    elif -0.5 <= data_skew <= 0.5:
        print("Data is approximately symmetrical.")
    elif data_skew < 0:
        print("Data is moderately skewed to the left.")
    else:
        print("Data is moderately skewed to the right.")
    return data_skew

def check_geometric_distribution(data, p_threshold=0.05):
    def mle_estimate_geometric_p(data):
       
        if not data:
            return None 
        sample_mean = np.mean(data)
        if sample_mean == 0:
            return None  
        p_hat = 1 / sample_mean  
        return p_hat   
    
    p_hat = mle_estimate_geometric_p(data)
    if p_hat is not None:
        print(f"MLE Estimate for p: {p_hat:.4f}")
        if p_hat > p_threshold:
            print("The data is likely geometrically distributed.")
        else:
            print("The data might not be geometrically distributed.")
        return p_hat
    else:
        print("Cannot check if data is geometrically distributed due to insufficient data.")
        return None

def is_uniquely_decodable(codewords):
    codewords = sorted(codewords, key=len)
    
    for i in range(len(codewords)):
        for j in range(i + 1, len(codewords)):
            if codewords[j].startswith(codewords[i]):
                return False
    return True

def analyze_alphabet_size(data, small_threshold=26, moderate_threshold=128):

    unique_chars = set(data)
    alphabet_size = len(unique_chars)*8
    

    if alphabet_size <= small_threshold:
        classification = "Small"
    elif alphabet_size <= moderate_threshold:
        classification = "Moderate"
    else:
        classification = "Large"
    

    return {
        "alphabet_size": alphabet_size,
        "unique_characters": unique_chars,
        "classification": classification,
    }

def check_dominant_character(data, dominance_threshold=30):
    #check the character is dominant 
    frequency = calculate_frequency(data)
    dominant_character = max(frequency, key=frequency.get)
    dominant_frequency = frequency[dominant_character]

    total_chars = len(data)
    dominant_percentage = (dominant_frequency / total_chars) * 100

    is_dominant = dominant_percentage >= dominance_threshold

    return {
        "is_dominant": is_dominant,
        "dominant_character": dominant_character if is_dominant else None,
        "dominant_percentage": dominant_percentage,
    }

def check_for_pattern(text, min_pattern_length=2, max_pattern_length=10, threshold_ratio = 0.3):

    if not text or len(text) < min_pattern_length:
        return None, 0

    best_pattern = None
    best_ratio = 0


    for pattern_length in range(min_pattern_length, min(max_pattern_length + 1, len(text)//2+1)):
            
      for i in range(len(text) - pattern_length +1):
        pattern = text[i:i + pattern_length]
        pattern_count = 0
        
        for j in range(len(text) - pattern_length + 1):
          if text[j:j+pattern_length] == pattern:
            pattern_count+=1

        pattern_ratio = pattern_count / (len(text)-pattern_length +1)

        if pattern_ratio>best_ratio:
           best_ratio = pattern_ratio
           best_pattern = pattern

    if best_ratio >= threshold_ratio:
       return best_pattern, best_ratio
    else:
        return None, 0


def check_long_runs(text, min_run_length=3):

    if not text or len(text) < min_run_length:
        return None, 0

    current_char = None
    current_run_length = 0
    longest_run_char = None
    longest_run_length = 0

    for char in text:
        if char == current_char:
            current_run_length += 1
        else:
            if current_run_length >= min_run_length and current_run_length> longest_run_length:
              longest_run_length = current_run_length
              longest_run_char = current_char
            current_char = char
            current_run_length = 1
    

    if current_run_length >= min_run_length and current_run_length> longest_run_length:
        longest_run_length = current_run_length
        longest_run_char = current_char
    if longest_run_char is None:
        return None, 0
    else:
        return longest_run_char, longest_run_length

def main():
    
    data = read_file('D:/cmporession project/.venv/Scripts/skeewed_data.txt')
    print("Original Content:", len(data)*8)
    alphanumeric_data = clean_to_alphanumeric(data)
    print("Cleaned Content:", alphanumeric_data)

    is_numbers_only = check_file_type(alphanumeric_data)
    print("Contains numbers only:", is_numbers_only)

    dominant_check = check_dominant_character(alphanumeric_data, dominance_threshold=30)
    long_run_char, long_run_length = check_long_runs(alphanumeric_data)
    
    if is_numbers_only:
        result = calculate_text_entropy(alphanumeric_data)
        print(f"Entropy: {result['entropy']:.2f}")
        print(f"Complexity: {result['complexity']}")

        data = [int(char) for char in alphanumeric_data if char.isdigit()]

        if data:
            geometric_p = check_geometric_distribution(data)
            if geometric_p is not None:
                skewness = check_skewness(data)

                if skewness is not None and -0.5 <= skewness <= 0.5:
                    print("The data is moderately or low skewed.")
                    print("Golomb technique is suitable for the data.")
                    # implement golomb technique here
                else:
                    print("Golomb technique might not be suitable for the data.")
            else:
                print("The data does not follow a geometric distribution.")
                print("Golomb technique might not be suitable for the data.")
        else:
            print("Unable to calculate skewness due to insufficient data.")
    else:
        alphabet_info = analyze_alphabet_size(alphanumeric_data)
        print(f"Alphabet Size: {alphabet_info['alphabet_size']}")
        print(f"Classification: {alphabet_info['classification']}")
        result = calculate_text_entropy(alphanumeric_data)
        print(f"Entropy: {result['entropy']:.2f}")
        print(f"Complexity: {result['complexity']}")
        if alphanumeric_data:
            r = analyze_alphabet_size(alphanumeric_data)
            if result['entropy'] >= 5:
                print("The text is complex")
                print("arithmetic coding is suitable for the text")
            elif (result['entropy'] >= 3) and (result['entropy'] < 5):
                if dominant_check["is_dominant"]: 
                    if r['classification'] == "Small" or r['classification'] == "Moderate":
                        print(f"Dominant Character: {dominant_check['dominant_character']}")
                        print(f"Percentage: {dominant_check['dominant_percentage']:.2f}%")
                        print("A dominant character exists in the text.")
                        print("huffman technique is suitable for the data.")
                        # implement huffman technique here
                    else:
                        print("the file is complex.")
                        print("arithmetic technique is suitable for the data.")
                        # implement arithmetic technique here

                else:
                    print("THE FILE HAS NO DOMINANT CHARACTER")
                    pattern, ratio = check_for_pattern(alphanumeric_data)
                    if pattern:
                        
                        print(f"Pattern: {pattern}")
                        print(f"Ratio: {ratio:.2f}")
                        print("A pattern exists in the text.")
                        if r['classification'] == "Small" or r['classification'] == "Moderate":
                            print("huffman technique is suitable for the data.")
                            # implement huffman technique here
                        else:
                            print("arithmetic technique is suitable for the data.")
                            # implement arithmetic technique here
                    else:
                        print("No pattern exists in the text.")
                        if r['classification'] == "Small" or r['classification'] == "Moderate":
                            print("huffman technique is suitable for the data.")
                            # implement huffman technique here
                        else:
                            print("arithmetic technique is suitable for the data.")
                            # implement arithmetic technique here
                    
                
            else:

                print("The text is simple")
                
                if long_run_char and skewness is None :
                    print(f"Long Run Character: {long_run_char}")
                    print(f"Long Run Length: {long_run_length}")
                    print("A long run of characters exists in the text.")
                    print("RLE technique is suitable for the data.")
                    # implement RLE technique here
                else:
                    print("there's no repeated sequances")
                    print("Huffman technique is suitable for the data.") 
                    # implement HUFFMAN technique here                   

if __name__ == "__main__":
    main()
