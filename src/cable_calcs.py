import math

def calculate_mutual_inductance_flat(S, r_m):
    """
    Calculate mutual inductance for flat configuration.
    
    Parameters:
    S (float): Spacing between the centers of adjacent cables (in inches)
    r_m (float): Mean radius of the sheath (in inches)
    
    Returns:
    float: Mutual inductance (micro-ohms per foot)
    """
    X_m = 52.92 * math.log10(S / r_m)
    return X_m

def calculate_mutual_inductance_trefoil(D, r_m):
    """
    Calculate mutual inductance for trefoil configuration.
    
    Parameters:
    D (float): Distance between the centers of adjacent cables (in inches)
    r_m (float): Mean radius of the sheath (in inches)
    
    Returns:
    float: Mutual inductance (micro-ohms per foot)
    """
    X_m = 46.21 * math.log10(D / r_m)
    return X_m

def calculate_sheath_voltage_rise(I, X_m, cable_length):
    """
    Calculate sheath voltage rise.
    
    Parameters:
    I (float): Current (amperes)
    X_m (float): Mutual inductance (micro-ohms per foot)
    cable_length (float): Cable length (feet)
    
    Returns:
    float: Sheath voltage rise (volts)
    """
    V_sh = I * X_m * cable_length * 10**-6
    return V_sh

def main():
    # Get user input for configuration type
    config_type = input("Enter the configuration type (flat/trefoil): ").strip().lower()
    
    if config_type == 'flat':
        # Get user input for flat configuration variables
        S = float(input("Enter the spacing between the centers of adjacent cables (in inches): "))
        r_m = float(input("Enter the mean radius of the sheath (in inches): "))
        X_m = calculate_mutual_inductance_flat(S, r_m)
    elif config_type == 'trefoil':
        # Get user input for trefoil configuration variables
        D = float(input("Enter the distance between the centers of adjacent cables (in inches): "))
        r_m = float(input("Enter the mean radius of the sheath (in inches): "))
        X_m = calculate_mutual_inductance_trefoil(D, r_m)
    else:
        print("Invalid configuration type. Please enter 'flat' or 'trefoil'.")
        return
    
    print(f"Calculated mutual inductance (X_m): {X_m:.2f} micro-ohms per foot")
    
    # Get user input for sheath voltage rise calculation
    I_normal = float(input("Enter the normal operating current (amperes): "))
    I_fault = float(input("Enter the fault current (amperes): "))
    cable_length = float(input("Enter the cable length (feet): "))
    
    V_sh_normal = calculate_sheath_voltage_rise(I_normal, X_m, cable_length)
    V_sh_fault = calculate_sheath_voltage_rise(I_fault, X_m, cable_length)
    
    print(f"Sheath voltage rise under normal load: {V_sh_normal:.2f} volts")
    print(f"Sheath voltage rise under fault conditions: {V_sh_fault:.2f} volts")

if __name__ == "__main__":
    main()
