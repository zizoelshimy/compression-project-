import os
import re
import math
from flask import Flask, render_template, request, jsonify
from scipy.stats import skew
from werkzeug.utils import secure_filename
import json
from bitstring import BitArray
import rle  # Import the rle module
import golomb # Import the golomb module
import huffman # Import the huffman module
import arithmetic # Import the arithmetic module
from file_analysis import (
    read_file,
    clean_to_alphanumeric,
    check_file_type,
    calculate_frequency,
    calculate_text_entropy,
    check_skewness,
    check_geometric_distribution,
    analyze_alphabet_size,
    check_dominant_character,
    check_for_pattern,
    check_long_runs
)

app = Flask(__name__, static_folder='static')

# Configure the upload folder and allowed file extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'bin', 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dictionary to store the encoded data and huffman dictionary name
encoded_data_store = {}

# Check if the file type is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to clean data to alphanumeric
def clean_to_alphanumeric(data):
    return re.sub(r'[^a-zA-Z0-9]', '', data)

# Function to calculate frequency of characters
def calculate_frequency(data):
    frequency = {}
    for char in data:
        frequency[char] = frequency.get(char, 0) + 1
    return frequency

# Function to calculate entropy of the text
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

# Function to check skewness of the data
def check_skewness(data):
    if len(data) < 3:
        return None
    from scipy.stats import skew
    data_skew = skew(data)
    return data_skew

# Function to check if the data follows a geometric distribution
def check_geometric_distribution(data, p_threshold=0.05):
    def mle_estimate_geometric_p(data):
        if not data:
            return None
        import numpy as np
        sample_mean = np.mean(data)
        if sample_mean <= 0:  # This is the fix
            return None
        p_hat = 1 / sample_mean
        return p_hat


    p_hat = mle_estimate_geometric_p(data)
    return p_hat


# Function to parse numbers from a file, handling comma-separated values
def parse_numbers_from_data(data):
    try:
        # Try splitting by commas and convert to integers, filtering out empty strings
        numbers = [int(x.strip()) for x in data.split(',') if x.strip().isdigit()]
        return numbers
    except ValueError:
        # If comma-separated parsing fails, try parsing as sequence of individual digits
         return [int(char) for char in data if char.isdigit()]


# --- End Compression Algorithms---


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Read the file content
        data = read_file(file_path)
        
        print(f"Data read from file: {data}")  # Check the data here
        # Clean the data to alphanumeric
        alphanumeric_data = clean_to_alphanumeric(data)

        # Check if the data contains only numbers
        is_numbers_only = check_file_type(alphanumeric_data)
        
        print(f"Cleaned data {alphanumeric_data} , is_numbers_only {is_numbers_only}")

        # Calculate entropy
        entropy_result = calculate_text_entropy(data)
        print(f"Entropy result {entropy_result}")
        
        # Convert data to numbers for geometric distribution and skewness
        if is_numbers_only:
          numeric_data = [int(char) for char in data if char.isdigit()]
        else:
          numeric_data = parse_numbers_from_data(data)

        print(f"Numeric Data {numeric_data}") # Check the numeric data

        # Calculate skewness and geometric distribution p value
        skewness = check_skewness(numeric_data)
        geometric_p = check_geometric_distribution(numeric_data)

        print(f"Skewness {skewness} Geometric P {geometric_p}") # Check the results

        # Determine skewness message
        skew_message = "Data is skewed"
        if skewness is not None and -0.5 <= skewness <= 0.5:
           skew_message = "Data is symmetrical"
           
         # Determine suitability of the file for golomb encoding
        golomb_suitability = "Golomb technique might not be suitable"
        if skewness is not None and -0.5 <= skewness <= 0.5:
          golomb_suitability = "Golomb technique is suitable"

        best_technique_message = ""  # Initialize the message to an empty string.
        best_technique = None
        if is_numbers_only:
            if numeric_data and geometric_p is not None:
                if skewness is not None and -0.5 <= skewness <= 0.5:
                    best_technique = "golomb"
                    best_technique_message = "Golomb is suitable for this file."
                else:
                    best_technique = "huffman"
                    best_technique_message = "Huffman is the most suitable for this file"
            else:
                best_technique = "huffman"
                best_technique_message = "Huffman is the most suitable for this file"
        else:
          alphabet_info = analyze_alphabet_size(alphanumeric_data)
          if entropy_result['entropy'] >= 5:
            best_technique = "arithmetic"
            best_technique_message = "Arithmetic coding is the most suitable for this file"
          elif (entropy_result['entropy'] >= 3) and (entropy_result['entropy'] < 5):
               dominant_check = check_dominant_character(alphanumeric_data, dominance_threshold=30)
               if dominant_check["is_dominant"]:
                  if alphabet_info['classification'] == "Small" or alphabet_info['classification'] == "Moderate":
                       best_technique = "huffman"
                       best_technique_message = "Huffman coding is the most suitable for this file"
                  else:
                      best_technique = "arithmetic"
                      best_technique_message = "Arithmetic coding is the most suitable for this file"
               else:
                    pattern, ratio = check_for_pattern(alphanumeric_data)
                    if pattern:
                      if alphabet_info['classification'] == "Small" or alphabet_info['classification'] == "Moderate":
                            best_technique = "huffman"
                            best_technique_message = "Huffman coding is the most suitable for this file"
                      else:
                         best_technique = "arithmetic"
                         best_technique_message = "Arithmetic coding is the most suitable for this file"
                    else:
                        if alphabet_info['classification'] == "Small" or alphabet_info['classification'] == "Moderate":
                            best_technique = "huffman"
                            best_technique_message = "Huffman coding is the most suitable for this file"
                        else:
                           best_technique = "arithmetic"
                           best_technique_message ="Arithmetic coding is the most suitable for this file"
          else:
              long_run_char, long_run_length = check_long_runs(alphanumeric_data)
              if long_run_char and skewness is None :
                 best_technique = "rle"
                 best_technique_message = "RLE technique is the most suitable for this file"
              else:
                best_technique = "huffman"
                best_technique_message = "Huffman coding is the most suitable for this file"
  
        # Prepare the result for the response
        result = {
            "cleaned_content": alphanumeric_data,
            "is_numbers_only": is_numbers_only,
            "entropy": round(entropy_result['entropy'], 2),
            "complexity": entropy_result['complexity'],
            "skewness": round(skewness, 2) if skewness is not None else None,
            "geometric_p": round(geometric_p, 4) if geometric_p is not None else None,
            "skew_message": skew_message,
            "golomb_suitability": golomb_suitability,
            "best_technique_message": best_technique_message,
            "best_technique": best_technique,
        }
        print(f"Final Result {result}") # Check final result
        # Return the analysis result as JSON
        return jsonify(result)

def load_encoded_data(filename):
  """Load encoded data and m from file for golomb decompression"""
  try:
     with open(filename, 'r') as f:
          encoded = f.readline().strip()
          m = int(f.readline().strip())
          return encoded, m
  except Exception as e:
         print(f"Error loading encoded data: {e}")
         return None, None
   
@app.route('/compress', methods=['POST'])
def compress_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']
    technique = request.form.get('technique')


    if file.filename == '':
        return jsonify({"error": "No selected file"})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        with open(file_path, 'r') as f:
            data = f.read()
         
        print(f"Data to process: {data} Technique {technique}")
        processed_content = ""
        comp_ratio = 0
        m = 0 # initialize m
        huffman_tree = None
        try:
            if technique == 'golomb':
                numeric_data = parse_numbers_from_data(data)

                if not numeric_data:
                   return jsonify({"error": "Invalid data for golomb encoding, please provide numbers"})
                
                m = golomb.compute_golomb_m(numeric_data)
                
                encoded = golomb.golomb_encode(numeric_data, m)
                processed_content =  encoded
                comp_ratio = len(data) / len(processed_content) if processed_content else 0
                
            elif technique == 'huffman':
                  encoded, huffman_dict, huffman_tree, comp_ratio  = huffman.huffman_encode(data)
                  if encoded is None:
                      return jsonify({"error": "Huffman encoding failed."})
                  processed_content = encoded
                  
                  # Save the huffman_dict to a file with .huff extension
                  huffman_filename = filename + ".huff"
                  huffman_file_path = os.path.join(app.config['UPLOAD_FOLDER'], huffman_filename)
                  with open(huffman_file_path, 'w') as huffman_file:
                      json.dump(huffman_dict, huffman_file)
                  # Store the encoded text and the huffman filename
                  encoded_data_store[filename] = {
                     "encoded_content": encoded,
                      "huffman_filename": huffman_filename
                  }
                  print(f"Saved data of {filename} encoded data is {encoded_data_store[filename]['encoded_content']} and the dict name is {encoded_data_store[filename]['huffman_filename']}")

            elif technique == 'rle':
                 processed_content = rle.compress(data)
                 comp_ratio = rle.compression_ratio(data, processed_content)
            elif technique == 'arithmetic':
                 compressor = arithmetic.ArithmeticCompressor()
                 compressed_value = compressor.compress(data)
                 comp_ratio = compressor.calculate_compression_ratio(data, compressed_value)
                 processed_content = str(compressed_value)
                 compressor.input_text = data
                 
                 # Save the compressed data to a file with .arithmetic extension
                 arithmetic_filename = filename + ".arithmetic"
                 arithmetic_file_path = os.path.join(app.config['UPLOAD_FOLDER'], arithmetic_filename)
                 with open(arithmetic_file_path, 'w') as arithmetic_file:
                    arithmetic_file.write(f"{processed_content}\n")
                    arithmetic_file.write(f"{len(data)}\n")
                 # Store the compressed text and the huffman filename
                 encoded_data_store[filename] = {
                     "compressed_value": processed_content,
                     "arithmetic_filename": arithmetic_filename
                 }
            else:
                return jsonify({"error": "Invalid compression technique"})
        except Exception as e:
            print(f"An error occurred during processing {e}")
            return jsonify({"error": f"An error occurred during file compression: {e}"})
        
        print(f"Processed Data {processed_content}")
        
        return jsonify({"original_content": data, "processed_content": processed_content, "compression_ratio": round(comp_ratio, 2) if comp_ratio != 0 else None, "m": m, "huffman_tree": huffman_tree})
    
    return jsonify({"error": "Invalid file type"})
    
@app.route('/decompress', methods=['POST'])
def decompress_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']
    technique = request.form.get('technique')

    if file.filename == '':
        return jsonify({"error": "No selected file"})

    if file and allowed_file(file.filename):
         filename = secure_filename(file.filename)
         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
         file.save(file_path)
        
         print(f"Data to decompress filename: {filename} Technique {technique}")
         processed_content = ""
         original_content = "" # Initialize original_content to empty string
         try:
            with open(file_path, 'r') as f:
                data = f.read()
            if technique == 'golomb':
                 # Load encoded data and m from the file.
                 loaded_encoded, loaded_m = load_encoded_data(file_path)
                 if loaded_encoded:
                     decoded = golomb.golomb_decode(loaded_encoded.split(','), loaded_m)
                     processed_content = ",".join(map(str, decoded))
                     original_content = data # Store the original data
                 else:
                    return jsonify({"error": f"Failed to load encoded data for file: {filename}"})
            elif technique == 'huffman':
                 # Check if the data exists in the store
                 if filename in encoded_data_store:
                    # Load the encoded content
                    encoded_content = encoded_data_store[filename]["encoded_content"]
                    huffman_filename = encoded_data_store[filename]["huffman_filename"]

                    # Load the huffman_dict from the .huff file
                    huffman_file_path = os.path.join(app.config['UPLOAD_FOLDER'], huffman_filename)
                    
                    try:
                       with open(huffman_file_path, 'r') as huffman_file:
                          huffman_dict = json.load(huffman_file)
                    except FileNotFoundError:
                        return jsonify({"error": "Huffman dictionary file not found."})
                    decoded = huffman.huffman_decode(encoded_content, huffman_dict)
                    processed_content = decoded
                    # Delete the huffman_filename from encoded_data_store to do not fill our data store with unnecesary data
                    del encoded_data_store[filename]
                    # Clean the file from the uploads directory
                    os.remove(huffman_file_path)
                    print(f"cleaned data of {filename}")
                    
                    # Fix: Now show the encoded content in original column, and the decoded in processed
                    original_content = encoded_content
                 else:
                    return jsonify({"error": "No encoded data found for this file. Be sure to compress the file before decompress"})
            elif technique == 'rle':
                 original_content = data
                 processed_content = rle.decompress(data)
            elif technique == 'arithmetic':
                  if filename in encoded_data_store:
                     # Load the compressed value and the original text length from file
                     arithmetic_filename = encoded_data_store[filename]["arithmetic_filename"]
                     arithmetic_file_path = os.path.join(app.config['UPLOAD_FOLDER'], arithmetic_filename)
                     try:
                        with open(arithmetic_file_path, 'r') as arithmetic_file:
                              compressed_value = float(arithmetic_file.readline().strip())
                              original_length = int(arithmetic_file.readline().strip())

                        compressor = arithmetic.ArithmeticCompressor()
                        compressor.input_text = data # load the data to create probabilities for decompression
                        processed_content = compressor.decompress(compressed_value, original_length)
                        original_content = str(compressed_value)
                        del encoded_data_store[filename]
                        os.remove(arithmetic_file_path)
                     except FileNotFoundError:
                        return jsonify({"error": "Arithmetic data file not found."})
                  else:
                       return jsonify({"error": "No arithmetic data found for this file. Be sure to compress the file before decompress"})
            else:
                return jsonify({"error": "Invalid decompression technique"})
         except Exception as e:
            print(f"An error occurred during decompression {e}")
            return jsonify({"error": f"An error occurred during file decompression: {e}"})
         
         print(f"Decompressed Data {processed_content}")
         return jsonify({"original_content": original_content, "processed_content": processed_content, "compression_ratio": None, "m": None})
    
    return jsonify({"error": "Invalid file type"})

if __name__ == "__main__":
    app.run(debug=True)