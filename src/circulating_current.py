import math

def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")

def get_positive_float_with_range(prompt, max_value):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0 or value > max_value:
                print(f"Please enter a positive number less than or equal to {max_value}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")

def calculate_circulating_current():
    print("\nTransformer Circulating Current Calculator")
    print("-----------------------------------------")
    
    # Get transformer 1 information
    print("\nTransformer 1:")
    mva1 = get_positive_float("Enter MVA rating: ")
    z1_percent = get_positive_float_with_range("Enter impedance (%): ", 20)
    
    # Get transformer 2 information
    print("\nTransformer 2:")
    mva2 = get_positive_float("Enter MVA rating: ")
    z2_percent = get_positive_float_with_range("Enter impedance (%): ", 20)
    
    # Get system information
    print("\nSystem Information:")
    voltage = get_positive_float("Enter low-side voltage (kV): ")
    vmismatch_percent = get_positive_float_with_range("Enter voltage mismatch (%): ", 10)
    
    # Convert to common MVA base (using larger MVA as base)
    base_mva = max(mva1, mva2)
    z1_converted = z1_percent * (base_mva/mva1)
    z2_converted = z2_percent * (base_mva/mva2)
    
    # Calculate base current
    base_current = (base_mva * 1000) / (voltage * math.sqrt(3))
    
    # Calculate circulating current in per unit
    z_total = z1_converted + z2_converted
    ic_pu = (vmismatch_percent/100) / (z_total/100)
    
    # Calculate actual circulating current
    ic_amps = ic_pu * base_current
    
    # Print results
    print("\nResults:")
    print("-----------------------------------------")
    print(f"Base MVA: {base_mva:.2f} MVA")
    print(f"Transformer 1 impedance on base MVA: {z1_converted:.2f}%")
    print(f"Transformer 2 impedance on base MVA: {z2_converted:.2f}%")
    print(f"Total impedance: {z_total:.2f}%")
    print(f"Base current: {base_current:.1f} A")
    print(f"Circulating current: {ic_amps:.1f} A")
    print(f"Circulating current (per unit): {ic_pu:.3f}")

if __name__ == "__main__":
    while True:
        calculate_circulating_current()
        
        # Ask if user wants to calculate again
        again = input("\nCalculate another circulating current? (y/n): ").lower()
        if again != 'y':
            print("\nThank you for using the calculator!")
            break