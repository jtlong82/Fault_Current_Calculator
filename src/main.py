from zbusmenu import zbusmenu
from ZBusClass import ZBus
#from zlinemenu import zlinemenu
from GetExcel import load_impedance_sheets
from GetExcel import load_line_trace
from GetExcel import load_clean_line_imp
from CleanLineTrace import map_impedances

def main():
    # Load impedance sheets and clean dataframes
    bus_dataframes = load_impedance_sheets()
    line_dataframes = load_clean_line_imp()
    zbus_selection = None
    line_trace = None

    while True:
        if zbus_selection == None:
            print("\nMenu Options: ")
        else:
            print(f"\nCurrent Bus Selection: {zbus_selection.station}")
            print("Menu Options: ")
        print("1. Select Station/Bus/Transformer(s)")
        print("2. Load Line Trace")
        print("3. Display Bus Info")
        print("4. Exit")

        choice = int(input("Please enter the number corresponding to your choice: "))

        if choice == 1:
            if bus_dataframes is not None:
                zbus_choice = zbusmenu(bus_dataframes)
                zbus_selection = ZBus(zbus_choice)
            else:
                print("Please load impedance sheets first.")
                
        elif choice == 2:
            line_trace = load_line_trace()
            
            # If df_linetrace is a dictionary, get the DataFrame corresponding to the first sheet
            if isinstance(line_trace, dict):
                first_sheet_name = list(line_trace.keys())[0]
                line_trace = line_trace[first_sheet_name]

            # Similarly for df_impedance
            if isinstance(line_dataframes, dict):
                first_sheet_name = list(line_dataframes.keys())[0]
                line_dataframes = line_dataframes[first_sheet_name]

            line_trace = map_impedances(line_trace, line_dataframes)

        elif choice == 3:
            if zbus_selection is not None:
                print("\nBus Info:")
                zbus_selection.display_info()
            else:
                print("Please select a bus and station/transformer first.")

        elif choice == 4:
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == '__main__':
    main()
