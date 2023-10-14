import tkinter as tk
import os
from tkinter import filedialog
from ExcelToDataframe import excel_to_dataframes
from CleanDataframe import clean_dataframe
from CleanLineTrace import clean_line_trace

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

def load_line_trace():
    try:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title='Load Line Trace',
            filetypes=(('Excel files', '*.xlsx'), ('All files', '*.*'))
        )

        if file_path:
            dataframes = excel_to_dataframes(file_path)
            dataframes = clean_line_trace(dataframes)

            for sheet_name, df in dataframes.items():
                print(df)
                print('\n')
            return dataframes
        else:
            print('No file was selected.')
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None