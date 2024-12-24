import heapq
from collections import Counter
import json

class ArithmeticCompressor:
    def __init__(self):
        self.low = 0.0
        self.high = 1.0
        self.range = 1.0
        self.symbol_counts = {}
        self.symbol_probs = {}
        self.steps = []
        self.input_text = ""  # Initialize input_text attribute in the constructor


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
        self.calculate_probabilities(self.input_text) #Using self.input_text from compress function to decompress
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
        
        return  original_bits / compressed_bits