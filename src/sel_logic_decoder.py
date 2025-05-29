import re
import os
import sys
import argparse
from collections import defaultdict

class SELLogicDecoder:
    def __init__(self):
        self.logic_bits = {}  # Dictionary to store logic bit definitions
        self.logic_equations = {}  # Dictionary to store logic equations
        self.visited = set()  # Set to track visited nodes during recursion
        
    def parse_settings_file(self, file_path):
        """Parse an SEL settings file and extract logic bits and equations."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Find the section identifier (e.g., [L1], [L2], etc.)
            section_match = re.search(r'\[(L\d+)\]', content)
            if section_match:
                section = section_match.group(1)
                print(f"Processing section {section} from {file_path}")
                
                # Extract SET and RST bits (logic latches)
                set_patterns = re.finditer(r'SET(\d+),"([^"]*)"', content)
                rst_patterns = re.finditer(r'RST(\d+),"([^"]*)"', content)
                
                # Store SET logic
                for match in set_patterns:
                    bit_num = match.group(1)
                    logic = match.group(2).strip()
                    if logic != "NA":
                        bit_name = f"LT{bit_num}"
                        self.logic_bits[bit_name] = logic
                        print(f"Found SET logic for {bit_name}: {logic}")
                
                # Store RST logic
                for match in rst_patterns:
                    bit_num = match.group(1)
                    logic = match.group(2).strip()
                    if logic != "NA":
                        bit_name = f"RST_LT{bit_num}"
                        self.logic_bits[bit_name] = logic
                
                # Extract SV (SEL variables) definitions
                sv_patterns = re.finditer(r'SV(\d+),"([^"]*)"', content)
                for match in sv_patterns:
                    bit_num = match.group(1)
                    logic = match.group(2).strip()
                    if logic != "NA":
                        bit_name = f"SV{bit_num}"
                        self.logic_bits[bit_name] = logic
                        print(f"Found SV logic for {bit_name}: {logic}")
                
                # Extract OUT (output) definitions
                out_patterns = re.finditer(r'OUT(\d+),"([^"]*)"', content)
                for match in out_patterns:
                    bit_num = match.group(1)
                    logic = match.group(2).strip()
                    if logic != "NA" and logic != "0":
                        bit_name = f"OUT{bit_num}"
                        self.logic_bits[bit_name] = logic
                        print(f"Found OUT logic for {bit_name}: {logic}")
                
                # Extract other logic equations (TR, CL, etc.)
                other_patterns = re.finditer(r'([A-Z0-9_]+),"([^"]*)"', content)
                for match in other_patterns:
                    eq_name = match.group(1)
                    logic = match.group(2).strip()
                    # Only add if it seems like a logic equation (contains logical operators)
                    if logic != "NA" and logic != "0" and any(op in logic for op in [" AND ", " OR ", " NOT ", "("]):
                        self.logic_bits[eq_name] = logic
                        print(f"Found other logic for {eq_name}: {logic}")
                
                return True
            else:
                print(f"No logic section found in {file_path}")
                return False
                
        except Exception as e:
            print(f"Error parsing file {file_path}: {e}")
            return False
    
    def parse_directory(self, directory):
        """Parse all .txt files in a directory that might contain SEL settings."""
        for filename in os.listdir(directory):
            if filename.lower().endswith('.txt') and 'set_l' in filename.lower():
                file_path = os.path.join(directory, filename)
                self.parse_settings_file(file_path)
    
    def expand_logic(self, expression, depth=0, max_depth=10):
        """Recursively expand a logic expression by substituting bit references."""
        if depth > max_depth:
            return f"[MAX_DEPTH_REACHED: {expression}]"
        
        # Base case: empty expression
        if not expression or expression == "0" or expression == "NA":
            return expression
        
        # Find all word bits (like LT01, SV02, etc.) in the expression
        word_bits = re.findall(r'\b([A-Z0-9_]+)(?!\s*=)', expression)
        
        # If no word bits found, return the expression as is
        if not word_bits:
            return expression
        
        expanded_expression = expression
        
        # Replace each word bit with its definition
        for bit in word_bits:
            # Skip if it's a common operator or number
            if bit in ["AND", "OR", "NOT", "XOR", "R_TRIG", "F_TRIG"]:
                continue
            
            # Skip numeric literals
            if bit.isdigit():
                continue
                
            # Check if the bit has a definition and hasn't been visited yet to avoid circular references
            if bit in self.logic_bits and bit not in self.visited:
                self.visited.add(bit)
                bit_definition = self.logic_bits[bit]
                
                # Recursively expand the bit definition
                expanded_definition = self.expand_logic(bit_definition, depth + 1, max_depth)
                
                # Replace all instances of the bit with its expanded definition, wrapping in parentheses
                # for clarity and to preserve operator precedence
                pattern = r'\b' + re.escape(bit) + r'\b'
                expanded_expression = re.sub(pattern, f"({expanded_definition})", expanded_expression)
                
                self.visited.remove(bit)
            
        return expanded_expression
    
    def decode_equation(self, equation_name, max_depth=5):
        """Decode a specific logic equation by name."""
        if equation_name in self.logic_bits:
            self.visited.clear()  # Reset visited set
            original = self.logic_bits[equation_name]
            expanded = self.expand_logic(original, max_depth=max_depth)
            return {
                "equation": equation_name,
                "original": original,
                "expanded": expanded
            }
        else:
            return {
                "equation": equation_name,
                "error": "Equation not found"
            }
    
    def decode_all_equations(self, max_depth=5):
        """Decode all stored logic equations."""
        results = {}
        for eq_name in self.logic_bits:
            results[eq_name] = self.decode_equation(eq_name, max_depth)
        return results

    def format_expanded_logic(self, expanded_logic):
        """Format expanded logic for better readability."""
        # Add line breaks after main operators
        formatted = re.sub(r'(\))\s+(AND|OR)\s+', r'\1\n    \2 ', expanded_logic)
        # Indent nested expressions
        level = 0
        result = []
        for char in formatted:
            if char == '(':
                level += 1
                result.append(char)
            elif char == ')':
                level -= 1
                result.append(char)
            else:
                result.append(char)
        
        return ''.join(result)

def main():
    parser = argparse.ArgumentParser(description='Decode SEL relay logic equations.')
    parser.add_argument('--file', type=str, help='Path to a specific SEL settings file.')
    parser.add_argument('--dir', type=str, help='Directory containing SEL settings files.')
    parser.add_argument('--equation', type=str, help='Specific equation to decode.')
    parser.add_argument('--max-depth', type=int, default=5, help='Maximum recursion depth for expansion.')
    parser.add_argument('--output', type=str, help='Output file for results.')
    
    args = parser.parse_args()
    
    decoder = SELLogicDecoder()
    
    # Parse input settings
    if args.file:
        decoder.parse_settings_file(args.file)
    elif args.dir:
        decoder.parse_directory(args.dir)
    else:
        print("Please specify either a file or directory to parse.")
        return
    
    # Decode equations
    if args.equation:
        result = decoder.decode_equation(args.equation, args.max_depth)
        print(f"\nDecoding equation: {args.equation}")
        print(f"Original: {result['original']}")
        print(f"Expanded: {result['expanded']}")
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(f"Equation: {args.equation}\n")
                f.write(f"Original: {result['original']}\n")
                f.write(f"Expanded: {result['expanded']}\n")
    else:
        results = decoder.decode_all_equations(args.max_depth)
        
        if args.output:
            with open(args.output, 'w') as f:
                for eq_name, result in results.items():
                    if 'error' not in result:
                        f.write(f"Equation: {eq_name}\n")
                        f.write(f"Original: {result['original']}\n")
                        f.write(f"Expanded: {result['expanded']}\n\n")
        else:
            for eq_name, result in results.items():
                if 'error' not in result and result['original'] != result['expanded']:
                    print(f"\nDecoding equation: {eq_name}")
                    print(f"Original: {result['original']}")
                    print(f"Expanded: {result['expanded']}")

if __name__ == "__main__":
    main()