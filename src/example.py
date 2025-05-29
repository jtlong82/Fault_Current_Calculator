import os
import sys
from sel_logic_decoder import SELLogicDecoder

# Save your SEL-651R settings files to a directory
# This example assumes you've saved them to a folder called "sel_settings"

# Create the decoder
decoder = SELLogicDecoder()

# Parse the logic files (usually Set_L1.txt, Set_L2.txt, etc.)
settings_dir = r"C:\Users\jlong\OneDrive\Documents\GitHub\Fault_Current_Calculator\src\sel_settings"  # Change this to your actual directory

# If you want to parse specific files:
important_files = [
    "Set_1.txt",
    "Set_L1.txt",
    "Set_D1.txt",
    "Set_F.txt",

]

for filename in important_files:
    file_path = os.path.join(settings_dir, filename)
    if os.path.exists(file_path):
        decoder.parse_settings_file(file_path)
    else:
        print(f"Warning: File {file_path} not found")

# Example 1: Decode a specific equation
equation = "OUT102"  # Change this to any equation you're interested in
result = decoder.decode_equation(equation, max_depth=5)

print(f"\nDecoding equation: {equation}")
if 'error' in result:
    print(f"Error: {result['error']}")
else:
    print(f"Original: {result['original']}")
    print(f"Expanded: {result['expanded']}")

# Example 2: Find and decode all equations containing "PB03"
search_term = "PB03"
print(f"\nFinding all equations containing '{search_term}':")
for eq_name, logic in decoder.logic_bits.items():
    if search_term in logic:
        result = decoder.decode_equation(eq_name)
        print(f"\n{eq_name}: {result['original']}")
        print(f"Expanded: {result['expanded']}")

# Example 3: Decode a complex equation
complex_eq = "TRA"  # "Trip A" logic
result = decoder.decode_equation(complex_eq, max_depth=8)

print(f"\nDecoding complex equation: {complex_eq}")
if 'error' in result:
    print(f"Error: {result['error']}")
else:
    print(f"Original: {result['original']}")
    print(f"Expanded: {result['expanded']}")

# Example 4: Export all decoded equations to a file
output_file = "decoded_logic.txt"
with open(output_file, 'w') as f:
    for eq_name in sorted(decoder.logic_bits.keys()):
        result = decoder.decode_equation(eq_name, max_depth=5)
        if 'error' not in result and result['original'] != result['expanded']:
            f.write(f"Equation: {eq_name}\n")
            f.write(f"Original: {result['original']}\n")
            f.write(f"Expanded: {result['expanded']}\n\n")

print(f"\nAll decoded equations saved to {output_file}")