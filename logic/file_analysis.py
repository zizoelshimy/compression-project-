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

    if 6.5 <= entropy <= 8:
        complexity = "The text is complex"
    elif 4 <= entropy < 6.5:
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

def main():
    file_path = '.venv/Scripts/geometric_data.txt'
    data = read_file(file_path)
    
    alphanumeric_data = clean_to_alphanumeric(data)
    print("Cleaned Content:", alphanumeric_data)

    is_numbers_only = check_file_type(alphanumeric_data)
    print("Contains numbers only:", is_numbers_only)
    
    if is_numbers_only:
        result = calculate_text_entropy(data)
        print(f"Entropy: {result['entropy']:.2f}")
        print(result['complexity'])
    

    data = [int(char) for char in data if char.isdigit()]
    
    if data:

        geometric_p = check_geometric_distribution(data)
        if geometric_p is not None:

            skewness = check_skewness(data)
            

            if skewness is not None and -0.5 <= skewness <= 0.5:  
                print("The data is moderately or low skewed.")
                print("Golomb technique is suitable for the data.")
                # implement golomb technique here
            else:
                print("golomb technique might not suitable for the data.")
        else:
            print("The data does not follow a geometric distribution.")
            print("golomb technique might not suitable for the data.")

    else:
        print("Unable to calculate skewness due to insufficient data.")


if __name__ == "__main__":
    main()

