#!/usr/bin/env python3
# BDD Relay Settings Calculator for Transformer Differential Protection
# Based on GEH-1816 Manual for BDD15B and BDD16B Relays

import math
import numpy as np

def calculate_line_current(mva, kv):
    """Calculate maximum line current in Amps"""
    return mva * 1000 / (math.sqrt(3) * kv)

def calculate_ct_secondary(line_current, ct_ratio):
    """Calculate CT secondary current"""
    ratio_parts = ct_ratio.split('/')
    primary = float(ratio_parts[0])
    secondary = float(ratio_parts[1])
    return line_current * secondary / primary

def find_nearest_tap(current, available_taps):
    """Find the nearest available tap value"""
    available_taps = np.array(available_taps)
    idx = (np.abs(available_taps - current)).argmin()
    return available_taps[idx]

def calculate_mismatch_error(ratio1, tap1, ratio2, tap2):
    """Calculate mismatch error between two windings"""
    ratio1_tap1 = ratio1 / tap1
    ratio2_tap2 = ratio2 / tap2
    return abs(ratio1_tap1 - ratio2_tap2) / ratio1_tap1 * 100

def extract_ct_ratio(ct_info):
    """Extract CT ratio from input string like '500/5'"""
    ratio_parts = ct_info.split('/')
    return float(ratio_parts[0]) / float(ratio_parts[1])

def calculate_two_winding_settings():
    """Calculate settings for a two-winding transformer"""
    print("\n--- Two-Winding Transformer BDD Relay Settings Calculator ---\n")
    
    # Transformer data
    mva = float(input("Enter transformer MVA rating: "))
    hv_kv = float(input("Enter HV winding voltage (kV): "))
    lv_kv = float(input("Enter LV winding voltage (kV): "))
    
    # Connection data
    print("\nEnter transformer connection (options: Delta-Wye, Wye-Delta, Delta-Delta, Wye-Wye)")
    transformer_connection = input("Transformer connection: ")
    
    # CT data
    hv_ct_ratio = input("Enter HV CT ratio (e.g., 500/5): ")
    hv_ct_connection = input("Enter HV CT connection (Wye or Delta): ").lower()
    
    lv_ct_ratio = input("Enter LV CT ratio (e.g., 1000/5): ")
    lv_ct_connection = input("Enter LV CT connection (Wye or Delta): ").lower()
    
    # Calculate line currents
    hv_line_current = calculate_line_current(mva, hv_kv)
    lv_line_current = calculate_line_current(mva, lv_kv)
    
    print(f"\nHV line current: {hv_line_current:.2f} A")
    print(f"LV line current: {lv_line_current:.2f} A")
    
    # Calculate CT secondary currents
    hv_ct_secondary = calculate_ct_secondary(hv_line_current, hv_ct_ratio)
    lv_ct_secondary = calculate_ct_secondary(lv_line_current, lv_ct_ratio)
    
    print(f"HV CT secondary current: {hv_ct_secondary:.2f} A")
    print(f"LV CT secondary current: {lv_ct_secondary:.2f} A")
    
    # Connection compensation
    hv_factor = math.sqrt(3) if (hv_ct_connection == "wye" and "delta" in transformer_connection.lower().split('-')[0].lower()) else 1
    lv_factor = math.sqrt(3) if (lv_ct_connection == "wye" and "delta" in transformer_connection.lower().split('-')[1].lower()) else 1
    
    hv_adjusted_current = hv_ct_secondary * hv_factor
    lv_adjusted_current = lv_ct_secondary * lv_factor
    
    print(f"HV adjusted secondary current: {hv_adjusted_current:.2f} A")
    print(f"LV adjusted secondary current: {lv_adjusted_current:.2f} A")
    
    # Available tap values for BDD relay
    available_taps = [2.9, 3.2, 3.5, 3.8, 4.2, 4.6, 5.0, 8.7]
    
    # Find nearest tap values
    hv_tap = find_nearest_tap(hv_adjusted_current, available_taps)
    lv_tap = find_nearest_tap(lv_adjusted_current, available_taps)
    
    print(f"\nNearest available HV tap: {hv_tap} A")
    print(f"Nearest available LV tap: {lv_tap} A")
    
    # Calculate CT ratios
    hv_ct_ratio_numeric = extract_ct_ratio(hv_ct_ratio)
    lv_ct_ratio_numeric = extract_ct_ratio(lv_ct_ratio)
    
    # Calculate mismatch error
    mismatch_error = calculate_mismatch_error(hv_ct_ratio_numeric, hv_tap, lv_ct_ratio_numeric, lv_tap)
    
    print(f"\nMismatch error: {mismatch_error:.2f}%")
    
    # Determine appropriate slope setting
    if mismatch_error < 10:
        recommended_slope = 15
    elif mismatch_error < 20:
        recommended_slope = 25
    else:
        recommended_slope = 40
    
    print(f"\n--- BDD15B Relay Settings Recommendations ---")
    print(f"HV winding tap: {hv_tap} A")
    print(f"LV winding tap: {lv_tap} A")
    print(f"Recommended slope setting: {recommended_slope}%")
    
    if mismatch_error > 5:
        print("\nNote: Mismatch error exceeds 5%. Consider adjusting CT ratios or using ratio-matching adjustments during commissioning.")
    
    # Instantaneous pickup setting (typically 8 times tap)
    print(f"Instantaneous pickup setting: 8 times tap")
    
    return {
        "hv_tap": hv_tap,
        "lv_tap": lv_tap,
        "slope": recommended_slope,
        "mismatch_error": mismatch_error
    }

def calculate_three_winding_settings():
    """Calculate settings for a three-winding transformer"""
    print("\n--- Three-Winding Transformer BDD Relay Settings Calculator ---\n")
    
    # Transformer data
    mva = float(input("Enter transformer MVA rating: "))
    hv_kv = float(input("Enter HV winding voltage (kV): "))
    mv_kv = float(input("Enter MV winding voltage (kV): "))
    lv_kv = float(input("Enter LV winding voltage (kV): "))
    
    # CT data
    hv_ct_ratio = input("Enter HV CT ratio (e.g., 500/5): ")
    hv_ct_connection = input("Enter HV CT connection (Wye or Delta): ").lower()
    
    mv_ct_ratio = input("Enter MV CT ratio (e.g., 1000/5): ")
    mv_ct_connection = input("Enter MV CT connection (Wye or Delta): ").lower()
    
    lv_ct_ratio = input("Enter LV CT ratio (e.g., 2000/5): ")
    lv_ct_connection = input("Enter LV CT connection (Wye or Delta): ").lower()
    
    # Calculate line currents
    hv_line_current = calculate_line_current(mva, hv_kv)
    mv_line_current = calculate_line_current(mva, mv_kv)
    lv_line_current = calculate_line_current(mva, lv_kv)
    
    print(f"\nHV line current: {hv_line_current:.2f} A")
    print(f"MV line current: {mv_line_current:.2f} A")
    print(f"LV line current: {lv_line_current:.2f} A")
    
    # Calculate CT secondary currents
    hv_ct_secondary = calculate_ct_secondary(hv_line_current, hv_ct_ratio)
    mv_ct_secondary = calculate_ct_secondary(mv_line_current, mv_ct_ratio)
    lv_ct_secondary = calculate_ct_secondary(lv_line_current, lv_ct_ratio)
    
    print(f"HV CT secondary current: {hv_ct_secondary:.2f} A")
    print(f"MV CT secondary current: {mv_ct_secondary:.2f} A")
    print(f"LV CT secondary current: {lv_ct_secondary:.2f} A")
    
    # Connection compensation
    # For a three-winding transformer, we need to know the connections between windings
    print("\nTransformer winding connections:")
    hv_connection = input("Enter HV winding connection (Delta or Wye): ").lower()
    mv_connection = input("Enter MV winding connection (Delta or Wye): ").lower()
    lv_connection = input("Enter LV winding connection (Delta or Wye): ").lower()
    
    # Apply connection compensation
    hv_factor = math.sqrt(3) if (hv_ct_connection == "wye" and hv_connection == "delta") else 1
    mv_factor = math.sqrt(3) if (mv_ct_connection == "wye" and mv_connection == "delta") else 1
    lv_factor = math.sqrt(3) if (lv_ct_connection == "wye" and lv_connection == "delta") else 1
    
    hv_adjusted_current = hv_ct_secondary * hv_factor
    mv_adjusted_current = mv_ct_secondary * mv_factor
    lv_adjusted_current = lv_ct_secondary * lv_factor
    
    print(f"HV adjusted secondary current: {hv_adjusted_current:.2f} A")
    print(f"MV adjusted secondary current: {mv_adjusted_current:.2f} A")
    print(f"LV adjusted secondary current: {lv_adjusted_current:.2f} A")
    
    # Available tap values for BDD relay
    available_taps = [2.9, 3.2, 3.5, 3.8, 4.2, 4.6, 5.0, 8.7]
    
    # Find nearest tap values
    hv_tap = find_nearest_tap(hv_adjusted_current, available_taps)
    mv_tap = find_nearest_tap(mv_adjusted_current, available_taps)
    lv_tap = find_nearest_tap(lv_adjusted_current, available_taps)
    
    print(f"\nNearest available HV tap: {hv_tap} A")
    print(f"Nearest available MV tap: {mv_tap} A")
    print(f"Nearest available LV tap: {lv_tap} A")
    
    # Calculate CT ratios
    hv_ct_ratio_numeric = extract_ct_ratio(hv_ct_ratio)
    mv_ct_ratio_numeric = extract_ct_ratio(mv_ct_ratio)
    lv_ct_ratio_numeric = extract_ct_ratio(lv_ct_ratio)
    
    # Calculate mismatch errors
    hv_mv_mismatch = calculate_mismatch_error(hv_ct_ratio_numeric, hv_tap, mv_ct_ratio_numeric, mv_tap)
    mv_lv_mismatch = calculate_mismatch_error(mv_ct_ratio_numeric, mv_tap, lv_ct_ratio_numeric, lv_tap)
    lv_hv_mismatch = calculate_mismatch_error(lv_ct_ratio_numeric, lv_tap, hv_ct_ratio_numeric, hv_tap)
    
    print(f"\nHV-MV mismatch error: {hv_mv_mismatch:.2f}%")
    print(f"MV-LV mismatch error: {mv_lv_mismatch:.2f}%")
    print(f"LV-HV mismatch error: {lv_hv_mismatch:.2f}%")
    
    # Determine appropriate slope setting
    max_mismatch = max(hv_mv_mismatch, mv_lv_mismatch, lv_hv_mismatch)
    if max_mismatch < 10:
        recommended_slope = 15
    elif max_mismatch < 20:
        recommended_slope = 25
    else:
        recommended_slope = 40
    
    print(f"\n--- BDD16B Relay Settings Recommendations ---")
    print(f"HV winding tap: {hv_tap} A")
    print(f"MV winding tap: {mv_tap} A")
    print(f"LV winding tap: {lv_tap} A")
    print(f"Recommended slope setting: {recommended_slope}%")
    
    if max_mismatch > 5:
        print("\nNote: Mismatch error exceeds 5%. Consider adjusting CT ratios or using ratio-matching adjustments during commissioning.")
    
    # Instantaneous pickup setting (typically 8 times tap)
    print(f"Instantaneous pickup setting: 8 times tap")
    
    # Create standardized BDD16B relay settings
    print("\n--- BDD16B Relay Parameter Settings ---")
    print("DEVICE_TYPE | PARAMETER_NUMBER | PARAMETER_GROUP | PARAMETER_NAME | PARAMETER_VALUE | REMARKS")
    print("-----------|-----------------|----------------|----------------|-----------------|--------")
    
    # Standardize CT ratios for relay
    hv_relay_ct = hv_ct_ratio_numeric / 5  # Convert to X/1 format
    mv_relay_ct = mv_ct_ratio_numeric / 5  # Convert to X/1 format
    lv_relay_ct = lv_ct_ratio_numeric / 5  # Convert to X/1 format
    
    print(f"BDD-16B | 1 | 0 | CT 1 | {lv_relay_ct:.0f}/1 | {'DELTA' if lv_ct_connection == 'delta' else ''}")
    print(f"BDD-16B | 2 | 0 | AUX CT 1 | N/A |")
    print(f"BDD-16B | 3 | 0 | CT 2 | {mv_relay_ct:.0f}/1 | {'DELTA' if mv_ct_connection == 'delta' else ''}")
    print(f"BDD-16B | 4 | 0 | AUX CT 2 | N/A |")
    print(f"BDD-16B | 5 | 0 | CT 3 | {hv_relay_ct:.0f}/1 | {'DELTA' if hv_ct_connection == 'delta' else ''}")
    print(f"BDD-16B | 6 | 0 | AUX CT 3 | N/A |")
    print(f"BDD-16B | 7 | 0 | WDG. TAP 1 | {lv_tap} | 30% MINIMUM PICKUP")
    print(f"BDD-16B | 8 | 0 | WDG. TAP 2 | {mv_tap} |")
    print(f"BDD-16B | 9 | 0 | WDG. TAP 3 | {hv_tap} |")
    print(f"BDD-16B | 10 | 0 | SLOPE | {recommended_slope} |")
    print(f"BDD-16B | 11 | 0 | HARMONIC RESTRAINT | FIELD ENTRY |")
    print(f"BDD-16B | 12 | 0 | INST MULTIPLE OF TAP | 8 |")
    print(f"BDD-16B | 13 | 0 | INST P.U. | FIELD ENTRY |")
    print(f"BDD-16B | 14 | 0 | TIME | FIELD ENTRY |")
    print(f"BDD-16B | 15 | 0 | I.C.S. | FIELD ENTRY |")
    print(f"BDD-16B | 16 | 0 | CONTROL VOLTAGE | 125 |")
    print(f"BDD-16B | 17 | 0 | MINIMUM P.U. MULTIPLE | |")
    print(f"BDD-16B | 18 | 0 | MINIMUM P.U. | |")
    
    return {
        "hv_tap": hv_tap,
        "mv_tap": mv_tap,
        "lv_tap": lv_tap,
        "slope": recommended_slope,
        "max_mismatch": max_mismatch
    }

def analyze_existing_two_winding_settings():
    """Analyze existing settings for a two-winding transformer"""
    print("\n--- Analyze Existing Two-Winding BDD Relay Settings ---\n")
    
    # Get CT ratios
    hv_ct_ratio = input("Enter HV CT ratio (e.g., 500/5): ")
    lv_ct_ratio = input("Enter LV CT ratio (e.g., 1000/5): ")
    
    # Get tap settings
    hv_tap = float(input("Enter HV winding tap setting: "))
    lv_tap = float(input("Enter LV winding tap setting: "))
    
    # Get slope setting
    slope = float(input("Enter slope setting (%): "))
    
    # Calculate CT ratios
    hv_ct_ratio_numeric = extract_ct_ratio(hv_ct_ratio)
    lv_ct_ratio_numeric = extract_ct_ratio(lv_ct_ratio)
    
    # Calculate mismatch error
    mismatch_error = calculate_mismatch_error(hv_ct_ratio_numeric, hv_tap, lv_ct_ratio_numeric, lv_tap)
    
    print(f"\n--- Analysis Results ---")
    print(f"HV CT ratio: {hv_ct_ratio}")
    print(f"LV CT ratio: {lv_ct_ratio}")
    print(f"HV tap setting: {hv_tap} A")
    print(f"LV tap setting: {lv_tap} A")
    print(f"Current slope setting: {slope}%")
    print(f"Calculated mismatch error: {mismatch_error:.2f}%")
    
    # Provide recommendations
    recommended_slope = 15
    if mismatch_error > 10:
        recommended_slope = 25
    if mismatch_error > 20:
        recommended_slope = 40
    
    if mismatch_error <= 5:
        print("\nThe mismatch error is within acceptable limits (<= 5%).")
    else:
        print("\nThe mismatch error exceeds 5%, which may lead to some differential current during load conditions.")
    
    if slope < recommended_slope:
        print(f"Warning: Current slope setting ({slope}%) may be too low for the calculated mismatch ({mismatch_error:.2f}%).")
        print(f"Recommendation: Consider increasing slope to at least {recommended_slope}%.")
    
    return {
        "hv_tap": hv_tap,
        "lv_tap": lv_tap,
        "slope": slope,
        "mismatch_error": mismatch_error,
        "recommended_slope": recommended_slope
    }

def analyze_existing_three_winding_settings():
    """Analyze existing settings for a three-winding transformer"""
    print("\n--- Analyze Existing Three-Winding BDD Relay Settings ---\n")
    
    # Get CT ratios
    hv_ct_ratio = input("Enter HV CT ratio (e.g., 500/5): ")
    mv_ct_ratio = input("Enter MV CT ratio (e.g., 1000/5): ")
    lv_ct_ratio = input("Enter LV CT ratio (e.g., 2000/5): ")
    
    # Get tap settings
    hv_tap = float(input("Enter HV winding tap setting: "))
    mv_tap = float(input("Enter MV winding tap setting: "))
    lv_tap = float(input("Enter LV winding tap setting: "))
    
    # Get slope setting
    slope = float(input("Enter slope setting (%): "))
    
    # Calculate CT ratios
    hv_ct_ratio_numeric = extract_ct_ratio(hv_ct_ratio)
    mv_ct_ratio_numeric = extract_ct_ratio(mv_ct_ratio)
    lv_ct_ratio_numeric = extract_ct_ratio(lv_ct_ratio)
    
    # Calculate mismatch errors
    hv_mv_mismatch = calculate_mismatch_error(hv_ct_ratio_numeric, hv_tap, mv_ct_ratio_numeric, mv_tap)
    mv_lv_mismatch = calculate_mismatch_error(mv_ct_ratio_numeric, mv_tap, lv_ct_ratio_numeric, lv_tap)
    lv_hv_mismatch = calculate_mismatch_error(lv_ct_ratio_numeric, lv_tap, hv_ct_ratio_numeric, hv_tap)
    
    max_mismatch = max(hv_mv_mismatch, mv_lv_mismatch, lv_hv_mismatch)
    
    print(f"\n--- Analysis Results ---")
    print(f"HV CT ratio: {hv_ct_ratio}")
    print(f"MV CT ratio: {mv_ct_ratio}")
    print(f"LV CT ratio: {lv_ct_ratio}")
    print(f"HV tap setting: {hv_tap} A")
    print(f"MV tap setting: {mv_tap} A")
    print(f"LV tap setting: {lv_tap} A")
    print(f"Current slope setting: {slope}%")
    print(f"HV-MV mismatch error: {hv_mv_mismatch:.2f}%")
    print(f"MV-LV mismatch error: {mv_lv_mismatch:.2f}%")
    print(f"LV-HV mismatch error: {lv_hv_mismatch:.2f}%")
    print(f"Maximum mismatch error: {max_mismatch:.2f}%")
    
    # Calculate current/tap ratios
    hv_ratio = hv_ct_ratio_numeric / hv_tap
    mv_ratio = mv_ct_ratio_numeric / mv_tap
    lv_ratio = lv_ct_ratio_numeric / lv_tap
    
    print(f"\nCurrent/Tap Ratios:")
    print(f"HV: {hv_ratio:.2f}")
    print(f"MV: {mv_ratio:.2f}")
    print(f"LV: {lv_ratio:.2f}")
    
    # Provide recommendations
    recommended_slope = 15
    if max_mismatch > 10:
        recommended_slope = 25
    if max_mismatch > 20:
        recommended_slope = 40
    
    if max_mismatch <= 5:
        print("\nAll mismatch errors are within acceptable limits (<= 5%).")
    else:
        print("\nMismatch errors exceed 5%, which may lead to some differential current during load conditions.")
        
        if hv_mv_mismatch > 5:
            print(f"HV-MV mismatch ({hv_mv_mismatch:.2f}%) is significant.")
        if mv_lv_mismatch > 5:
            print(f"MV-LV mismatch ({mv_lv_mismatch:.2f}%) is significant.")
        if lv_hv_mismatch > 5:
            print(f"LV-HV mismatch ({lv_hv_mismatch:.2f}%) is significant.")
    
    if slope < recommended_slope:
        print(f"\nWarning: Current slope setting ({slope}%) may be too low for the maximum mismatch ({max_mismatch:.2f}%).")
        print(f"Recommendation: Consider increasing slope to at least {recommended_slope}%.")
    
    # Estimate differential current during normal load
    expected_diff_current = max_mismatch / 100 * 100  # As percentage of full load
    print(f"\nEstimated differential current during normal load: approximately {expected_diff_current:.1f}% of through current")
    
    return {
        "hv_tap": hv_tap,
        "mv_tap": mv_tap,
        "lv_tap": lv_tap,
        "slope": slope,
        "max_mismatch": max_mismatch,
        "recommended_slope": recommended_slope
    }

def main():
    """Main function to run the BDD relay settings calculator"""
    print("BDD Relay Settings Calculator")
    print("============================")
    print("\nThis program calculates and analyzes tap and relay settings for GE BDD transformer differential relays.")
    print("Please select an option:")
    print("1. Calculate settings for two-winding transformer (BDD15B)")
    print("2. Calculate settings for three-winding transformer (BDD16B)")
    print("3. Analyze existing settings for two-winding transformer")
    print("4. Analyze existing settings for three-winding transformer")
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == "1":
        settings = calculate_two_winding_settings()
        is_two_winding = True
    elif choice == "2":
        settings = calculate_three_winding_settings()
        is_two_winding = False
    elif choice == "3":
        settings = analyze_existing_two_winding_settings()
        is_two_winding = True
    elif choice == "4":
        settings = analyze_existing_three_winding_settings()
        is_two_winding = False
    else:
        print("Invalid choice. Please run the program again.")
        return
    
    print("\nCalculation complete.")
    
    # Save to file option
    save_option = input("\nWould you like to save these results to a file? (y/n): ").lower()
    if save_option == 'y':
        filename = input("Enter filename (default: bdd_relay_settings.txt): ") or "bdd_relay_settings.txt"
        with open(filename, 'w') as f:
            f.write("BDD Relay Settings\n")
            f.write("=================\n\n")
            
            if choice == "1":
                f.write("Two-Winding Transformer (BDD15B) - Calculated Settings\n\n")
                f.write(f"HV winding tap: {settings['hv_tap']} A\n")
                f.write(f"LV winding tap: {settings['lv_tap']} A\n")
                f.write(f"Slope setting: {settings['slope']}%\n")
                f.write(f"Mismatch error: {settings['mismatch_error']:.2f}%\n")
            
            elif choice == "2":
                f.write("Three-Winding Transformer (BDD16B) - Calculated Settings\n\n")
                f.write(f"HV winding tap: {settings['hv_tap']} A\n")
                f.write(f"MV winding tap: {settings['mv_tap']} A\n")
                f.write(f"LV winding tap: {settings['lv_tap']} A\n")
                f.write(f"Slope setting: {settings['slope']}%\n")
                f.write(f"Maximum mismatch error: {settings['max_mismatch']:.2f}%\n")
            
            elif choice == "3":
                f.write("Two-Winding Transformer (BDD15B) - Existing Settings Analysis\n\n")
                f.write(f"HV winding tap: {settings['hv_tap']} A\n")
                f.write(f"LV winding tap: {settings['lv_tap']} A\n")
                f.write(f"Current slope setting: {settings['slope']}%\n")
                f.write(f"Calculated mismatch error: {settings['mismatch_error']:.2f}%\n")
                f.write(f"Recommended slope setting: {settings['recommended_slope']}%\n")
                if settings['slope'] < settings['recommended_slope']:
                    f.write(f"Warning: Current slope setting is lower than recommended.\n")
            
            elif choice == "4":
                f.write("Three-Winding Transformer (BDD16B) - Existing Settings Analysis\n\n")
                f.write(f"HV winding tap: {settings['hv_tap']} A\n")
                f.write(f"MV winding tap: {settings['mv_tap']} A\n")
                f.write(f"LV winding tap: {settings['lv_tap']} A\n")
                f.write(f"Current slope setting: {settings['slope']}%\n")
                f.write

if __name__ == "__main__":
    main()