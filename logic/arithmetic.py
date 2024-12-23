import matplotlib.pyplot as plt
import matplotlib.patches as patches

class ArithmeticCompressor:
    def __init__(self):
        self.low = 0.0
        self.high = 1.0
        self.range = 1.0
        self.symbol_counts = {}
        self.symbol_probs = {}
        self.steps = [] 

    def calculate_probabilities(self, text):
        
        self.symbol_counts = {}
        for symbol in text:
          self.symbol_counts[symbol] = self.symbol_counts.get(symbol, 0) + 1
        
        total_count = len(text)
        for symbol, count in self.symbol_counts.items():
            self.symbol_probs[symbol] = count / total_count

    def compress(self, text):
     
        self.calculate_probabilities(text)
        self.low = 0.0
        self.high = 1.0
        self.range = 1.0
        self.steps = [] 

        for symbol in text:
        
            self.steps.append({"symbol": symbol, "low": self.low, "high": self.high})

            symbol_low = 0.0
            for sym, prob in self.symbol_probs.items():
                if sym < symbol:
                    symbol_low += prob
            
            symbol_high = symbol_low + self.symbol_probs[symbol]
            
            new_low = self.low + self.range * symbol_low
            new_high = self.low + self.range * symbol_high
            
            self.low = new_low
            self.high = new_high
            self.range = self.high - self.low


        compressed_value = (self.low + self.high)/2 
        return compressed_value


    def decompress(self, compressed_value, text_length):
        decompressed_text = ""
        self.calculate_probabilities(self.input_text) 
        self.low = 0.0
        self.high = 1.0
        self.range = 1.0
        
        for _ in range(text_length):
            found_symbol = None
            for sym, prob in self.symbol_probs.items():
              symbol_low = 0.0
              for sym2, prob2 in self.symbol_probs.items():
                if sym2 < sym:
                  symbol_low += prob2
                
              symbol_high = symbol_low + self.symbol_probs[sym]

              if self.low + self.range * symbol_low <= compressed_value < self.low + self.range * symbol_high:
                  found_symbol = sym
                  break
                  
            if found_symbol is None:
              raise Exception("Can't find symbol")

            decompressed_text += found_symbol
            
            symbol_low = 0.0
            for sym, prob in self.symbol_probs.items():
              if sym < found_symbol:
                symbol_low += prob
            
            symbol_high = symbol_low + self.symbol_probs[found_symbol]

            new_low = self.low + self.range * symbol_low
            new_high = self.low + self.range * symbol_high
            
            self.low = new_low
            self.high = new_high
            self.range = self.high - self.low

        return decompressed_text


    def calculate_compression_ratio(self, original_text, compressed_value):
        original_bits = len(original_text) * 8 
       
        compressed_bits = 64 if isinstance(compressed_value, float) else len(bin(compressed_value)[2:]) 
        
        return  compressed_bits / original_bits 
    
    def visualise_steps(self):
        fig, ax = plt.subplots(figsize=(10, len(self.steps) * 1))
        ax.set_xlim([0, 1])
        ax.set_ylim([0, len(self.steps) + 1])
        ax.set_yticks(range(1, len(self.steps) + 1))
        ax.set_yticklabels([f"{step['symbol']}" for step in self.steps])
        ax.set_xlabel("Range")
        ax.set_title("Arithmetic Compression Steps")

        for i, step in enumerate(self.steps):
          height_adjustment = 0.4 
          rect = patches.Rectangle((step["low"], i + 1 - height_adjustment), step["high"] - step["low"], 2*height_adjustment, edgecolor='black', facecolor='lightblue', linewidth=1, fill=True)
          ax.add_patch(rect)
          ax.text( (step["low"] + step["high"])/2, i+1, f'[{step["low"]:.3f}, {step["high"]:.3f})', ha='center', va='center')


        plt.tight_layout()
        plt.show()


compressor = ArithmeticCompressor()
with open("huffman_favored_file.txt", "r") as file:
    input_text = file.read()
compressed_value = compressor.compress(input_text)
compressor.input_text = input_text 
decompressed_text = compressor.decompress(compressed_value, len(input_text))
compression_ratio = compressor.calculate_compression_ratio(input_text, compressed_value)

print(f"Original Text: {input_text}")
print(f"Compressed Value: {compressed_value}")
print(f"Decompressed Text: {decompressed_text}")
print(f"Compression Ratio: {compression_ratio:.3f}") 


compressor.visualise_steps() 