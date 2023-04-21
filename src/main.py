import tkinter as tk
from tkinter import filedialog
from ExcelToDataframe import excel_to_dataframes
from CleanDataframe import clean_dataframe
from zbusmenu import zbusmenu
from ZBusClass import ZBus

def main():
    # Create a tkinter root window (it won't be shown)
    root = tk.Tk()
    root.withdraw()

    # Prompt the user to select a file using a file dialog
    file_path = filedialog.askopenfilename(
        title='Load Impedance Sheets (Andy Sheets)',
        filetypes=(('Excel files', '*.xlsx'), ('All files', '*.*'))
    )

    # If the user selects a file, read the sheets, clean them, and print the DataFrames
    if file_path:
        dataframes = excel_to_dataframes(file_path)
        dataframes = clean_dataframe(dataframes)

        for sheet_name, df in dataframes.items():
            print(f'Sheet name: {sheet_name}')
            print(df)
            print('\n')
    else:
        print('No file was selected.')

    #Menu to select bus and station/transformer to retrieve zbus values and save into Zbus class
    zbus_choice = zbusmenu(dataframes)
    zbus_selection = ZBus(zbus_choice)

    print("\nBus Attributes:")
    zbus_selection.display_info()

if __name__ == '__main__':
    main()
