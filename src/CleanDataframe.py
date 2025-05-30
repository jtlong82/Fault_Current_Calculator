import pandas as pd
import numpy as np

def clean_dataframe(dataframe):
    cleaned_dataframe = {}
    
    # Define voltage level mappings for common nominal voltages
    voltage_mappings = {
        '11kV': 11.5,     # 11kV nominal is actually 11.5kV
        '13kV': 13.2,     # 13kV nominal is actually 13.2kV
        '13.2kV': 13.2,
        '11.5kV': 11.5,
        '36kV': 36.0,
        '36.0kV': 36.0,
        '4kV': 4.6,       # 4kV nominal is actually 4.6kV
        '4.6kV': 4.6,
    }
    
    for sheet_name, df in dataframe.items():
        # Extract the voltage level from the sheet name
        voltage_level = None
        
        # Check voltage mappings
        for voltage_str, actual_voltage in voltage_mappings.items():
            if voltage_str in sheet_name:
                voltage_level = actual_voltage
                break
        
        # If no mapping found, try to parse the voltage directly
        if voltage_level is None and 'kV' in sheet_name:
            try:
                # Extract number before 'kV'
                import re
                match = re.search(r'(\d+\.?\d*)\s*kV', sheet_name)
                if match:
                    voltage_level = float(match.group(1))
                else:
                    print(f"Warning: Could not parse voltage from sheet name: {sheet_name}")
                    voltage_level = 0.0
            except Exception as e:
                print(f"Error parsing voltage from sheet name '{sheet_name}': {e}")
                voltage_level = 0.0

        # Check if the sheet name contains the word "Bus"
        if "Bus" in sheet_name:
            # Drop the first two rows
            df = df.drop([0, 1], errors='ignore')

            # Get column labels by index
            columns_to_drop = df.columns[[7, 8, 9, 13, 14, 15, 16, 17, 18, 19, 20]]

            # Drop the columns
            df = df.drop(columns=columns_to_drop, errors='ignore')

            # Remove empty rows
            df = df.dropna(axis=0, how='all')

            # Remove empty columns
            df = df.dropna(axis=1, how='all')
            
            # Set the column names to be the first row in the DataFrame
            df = df.rename(columns=df.iloc[0]).drop(df.index[0])

            # Set None values in iloc[7], iloc[8], and iloc[9] to complex(0)
            for col_idx in [7, 8, 9]:
                if col_idx < df.shape[1]:  # Check if the DataFrame has enough columns
                    df.iloc[:, col_idx] = df.iloc[:, col_idx].apply(lambda x: complex(0) if x is None else x)

        # Check if the sheet name contains the word "36kV Line"
        elif "36kV Line" in sheet_name:
            # Drop rows
            df = df.drop([0, 1, 3, 37, 38], errors='ignore')

            # Get column labels by index
            columns_to_drop = df.columns[[2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15]]

            # Drop the columns
            df = df.drop(columns=columns_to_drop, errors='ignore')

            # Remove empty rows
            df = df.dropna(axis=0, how='all')

            # Remove empty columns
            df = df.dropna(axis=1, how='all')

            # Set the column names to be the first row in the DataFrame
            df = df.rename(columns=df.iloc[0]).drop(df.index[0])

        # Check if the sheet name contains the word "13kV Line"
        elif "13.2kV Line" in sheet_name or "13kV Line" in sheet_name:
            # Drop rows
            df = df.drop([0, 1, 3, 11, 13, 22, 23, 24, 25], errors='ignore')

            # Get column labels by index
            columns_to_drop = df.columns[[2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15]]

            # Drop the columns
            df = df.drop(columns=columns_to_drop, errors='ignore')

            # Remove empty rows
            df = df.dropna(axis=0, how='all')

            # Remove empty columns
            df = df.dropna(axis=1, how='all')

            # Set the column names to be the first row in the DataFrame
            df = df.rename(columns=df.iloc[0]).drop(df.index[0])

        # Check if the sheet name contains the word "11kV Line"
        elif "11.5kV Line" in sheet_name or "11kV Line" in sheet_name:
            # Drop rows
            df = df.drop([0, 1, 3, 9, 10, 11, 13, 17, 18, 19, 20, 21, 22, 28, 29], errors='ignore')

            # Get column labels by index
            columns_to_drop = df.columns[[2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15]]

            # Drop the columns
            df = df.drop(columns=columns_to_drop, errors='ignore')

            # Remove empty rows
            df = df.dropna(axis=0, how='all')

            # Remove empty columns
            df = df.dropna(axis=1, how='all')

            # Set the column names to be the first row in the DataFrame
            df = df.rename(columns=df.iloc[0]).drop(df.index[0])

        # Check if the sheet name contains the word "4kV Line"
        elif "4.6kV Line" in sheet_name or "4kV Line" in sheet_name:
            # Drop rows
            df = df.drop([0, 1, 3, 12, 14], errors='ignore')

            # Get column labels by index
            columns_to_drop = df.columns[[2, 3, 4, 5, 6, 7]]

            # Drop the columns
            df = df.drop(columns=columns_to_drop, errors='ignore')

            # Remove empty rows
            df = df.dropna(axis=0, how='all')

            # Remove empty columns
            df = df.dropna(axis=1, how='all')

            # Set the column names to be the first row in the DataFrame
            df = df.rename(columns=df.iloc[0]).drop(df.index[0])

        # Reset index to renumber rows for both "Bus" and "Line" sheets
        df = df.reset_index(drop=True)

        # Add a new column for Voltage_Level
        df["Voltage_Level"] = voltage_level
        
        # Save the cleaned dataframe back to dictionary
        cleaned_dataframe[sheet_name] = df
        
    return cleaned_dataframe