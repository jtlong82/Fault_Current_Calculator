import tkinter as tk
import os
from tkinter import filedialog
from ExcelToDataframe import excel_to_dataframes
from CleanDataframe import clean_dataframe
from CleanLineTrace import clean_line_trace
import pandas as pd

def load_impedance_sheets():
    # Hardcoded file path
    hardcoded_path = r'C:\Users\51192\OneDrive - FirstEnergy Corp\Documents\Python\Updated Copy of Bus Z Calcs(Andy Sheets) 2.16.17.xlsx'

    # Check if the file exists at the hardcoded path
    if os.path.exists(hardcoded_path):
        file_path = hardcoded_path
    else:
        # Create a tkinter root window (it won't be shown)
        root = tk.Tk()
        root.withdraw()

        # Prompt the user to select a file using a file dialog
        file_path = filedialog.askopenfilename(
            title='Load Impedance Sheets (Andy Sheets)',
            filetypes=(('Excel files', '*.xlsx'), ('All files', '*.*'))
        )
    
    # If a file is selected (either from hardcoded path or user), read and clean the sheets
    if file_path:
        dataframes = excel_to_dataframes(file_path)
        dataframes = clean_dataframe(dataframes)

        #KEEP FOR DEBUGGING
        #for sheet_name, df in dataframes.items():
            #print(f'Sheet name: {sheet_name}')
            #print(df)
            #print('\n')
    else:
        print('No file was selected.')
        dataframes = None  # Return None if no file is selected

    return dataframes

def load_clean_line_imp():
     # Hardcoded file path
    hardcoded_path = r'C:\Users\51192\OneDrive - FirstEnergy Corp\Documents\Python\line cleanup.xlsx'

    # Check if the file exists at the hardcoded path
    if os.path.exists(hardcoded_path):
        file_path = hardcoded_path
    else:
        # Create a tkinter root window (it won't be shown)
        root = tk.Tk()
        root.withdraw()

        # Prompt the user to select a file using a file dialog
        file_path = filedialog.askopenfilename(
            title='Load Clean Line Impedances',
            filetypes=(('Excel files', '*.xlsx'), ('All files', '*.*'))
        )
    
    # If a file is selected (either from hardcoded path or user), read and clean the sheets
    if file_path:
        dataframes = excel_to_dataframes(file_path)

        for sheet_name, df in dataframes.items():

            # Set the column names to be the first row in the DataFrame
            df = df.rename(columns=df.iloc[0]).drop(df.index[0])

            # Reset index to renumber rows
            df = df.reset_index(drop=True)

            # Convert the 'Voltage_Level' column to numeric (float64)
            df['Voltage_Level'] = pd.to_numeric(df['Voltage_Level'], errors='coerce')

            dataframes[sheet_name] = df

        #KEEP FOR DEBUGGING
        #for sheet_name, df in dataframes.items():
            #print(f'Sheet name: {sheet_name}')
            #print(df)
            #print('\n')
    else:
        print('No file was selected.')
        dataframes = None  # Return None if no file is selected    

    return dataframes   

def load_line_trace():
    try:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title='Load Line Trace',
            filetypes=(('Excel files', '*.xlsx'), ('All files', '*.*'))
        )

        if file_path:
            # Extract the Excel file name (without extension) to use as the new sheet name
            new_sheet_name = os.path.splitext(os.path.basename(file_path))[0]

            dataframes = excel_to_dataframes(file_path)
            dataframes = clean_line_trace(dataframes)

            # Rename the key in the dictionary to match the Excel file name
            first_sheet_name = list(dataframes.keys())[0]
            dataframes[new_sheet_name] = dataframes.pop(first_sheet_name)
            
            # Add voltage level column to line trace
            voltage_map = {'R': 36.0, 'L': 13.2, 'V': 11.5, 'H': 4.6}
            first_letter = new_sheet_name[0]
            voltage_level = voltage_map.get(first_letter, None)
            if voltage_level is not None:
                dataframes[new_sheet_name]['Voltage_Level'] = voltage_level 
            else:
                print("Warning: Unrecognized line trace sheet name. Cannot determine voltage level. Line trace .xls file name should start with the line name, i.e R-21-MF-G-X.")
        else:
            print('No file was selected.')
            dataframes = None  # Return None if no file is selected  
            
            #DEBUGGING
            #for sheet_name, df in dataframes.items():
                #print(f"Sheet name: {sheet_name}")
                #print(df)
                #print('\n')

        return dataframes

    except Exception as e:
        print(f"An error occurred: {e}")
        return None