import tkinter as tk
from tkinter import filedialog
from ExcelToDataframe import excel_to_dataframes
from CleanDataframe import clean_dataframe
from zbusmenu import zbusmenu
from ZBusClass import ZBus

def main():
    # Load impedance sheets and clean dataframes
    dataframes = load_impedance_sheets()
    zbus_selection = None

    while True:
        print("\nMenu Options:")
        print("1. Select Bus and Station/Transformer")
        print("2. Display Bus Attributes")
        print("3. Exit")

        choice = int(input("Please enter the number corresponding to your choice: "))

        if choice == 1:
            if dataframes is not None:
                # Menu to select bus and station/transformer to retrieve zbus values and save into ZBus
                zbus_choice = zbusmenu(dataframes)
                zbus_selection = ZBus(zbus_choice)
            else:
                print("Please load impedance sheets first.")

        elif choice == 2:
            if zbus_selection is not None:
                print("\nBus Attributes:")
                zbus_selection.display_info()
            else:
                print("Please select a bus and station/transformer first.")

        elif choice == 3:
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

def load_impedance_sheets():
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

    return dataframes

if __name__ == '__main__':
    main()
