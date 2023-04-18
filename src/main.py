import tkinter as tk
from tkinter import filedialog
from ExcelToDataframe import excel_to_dataframes
from CleanDataframe import clean_dataframe

def main():
    # Create a tkinter root window (it won't be shown)
    root = tk.Tk()
    root.withdraw()

    # Prompt the user to select a file using a file dialog
    file_path = filedialog.askopenfilename(
        title='Select an Excel file',
        filetypes=(('Excel files', '*.xlsx'), ('All files', '*.*'))
    )

    # If the user selects a file, read the sheets and print the DataFrames
    if file_path:
        dataframes = excel_to_dataframes(file_path)
        clean_dataframe(dataframes)

        for sheet_name, df in dataframes.items():
            print(f'Sheet name: {sheet_name}')
            print(df)
            print('\n')
    else:
        print('No file was selected.')

if __name__ == '__main__':
    main()
