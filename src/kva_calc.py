import math

def convert_kva_to_amps(kva, line_to_line_voltage):
    """
    Convert kVA to Amps for a three-phase system using line-to-line voltage.
    
    Parameters:
    kva (float): The power in kilovolt-amperes.
    line_to_line_voltage (float): The line-to-line voltage in volts.
    
    Returns:
    float: The current in amperes.
    """
    amps = (kva * 1000) / (math.sqrt(3) * line_to_line_voltage * 1000)
    return amps

def main():
    try:
        # Prompt the user for kVA and line-to-line voltage
        kva = float(input("Enter the power in kVA: "))
        line_to_line_voltage = float(input("Enter the line-to-line voltage in kilo-volts: "))
        
        # Convert kVA to Amps
        amps = convert_kva_to_amps(kva, line_to_line_voltage)
        
        # Display the result
        print(f"The current is approximately {amps:.2f} amps.")
    except ValueError:
        print("Please enter valid numerical values for kVA and voltage.")

if __name__ == "__main__":
    main()