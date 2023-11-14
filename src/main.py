from menus import zbusmenu
from ZBusClass import ZBus
from ZLineClass import ZLine
from ZTransClass import ZTrans
from GetExcel import load_impedance_sheets
from GetExcel import load_line_trace
from GetExcel import load_clean_line_imp
from CleanLineTrace import map_impedances
from Calcs import primary_line_fault_calculation
from Calcs import locate_primary_line_fault_l_g

def main():
    # Load impedance sheets and clean dataframes
    bus_dataframes = load_impedance_sheets()
    line_dataframes = load_clean_line_imp()
    zbus_selection = None
    zline_selection = None
    ztrans_selection = None
    line_trace = None

    while True:
        if zbus_selection == None:
            print("\nMenu Options: ")
        else:
            print(f"\nCurrent Bus Selection: {zbus_selection.station}")
            print("Menu Options: ")
        print("1. Select Station/Bus/Transformer(s)")
        print("2. Load Line Trace")
        print("3. Load Transformer")
        print("4. Display Bus Info")
        print("5. Calculations")
        print("6. Exit")

        choice = int(input("Select: "))

        if choice == 1:
            if bus_dataframes is not None:
                zbus_choice = zbusmenu(bus_dataframes)
                zbus_selection = ZBus(zbus_choice)
            else:
                print("Please load impedance sheets first.")
                
        elif choice == 2:
            line_trace = load_line_trace()
            if line_trace is not None:
                # If df_linetrace is a dictionary, get the DataFrame corresponding to the first sheet
                if isinstance(line_trace, dict):
                    first_sheet_name_trace = list(line_trace.keys())[0]
                    line_trace = line_trace[first_sheet_name_trace]

                # Similarly for df_impedance
                if isinstance(line_dataframes, dict):
                    first_sheet_name = list(line_dataframes.keys())[0]
                    line_dataframes = line_dataframes[first_sheet_name]

                line_trace = map_impedances(line_trace, line_dataframes)
                zline_selection = ZLine(line_trace)
                zline_selection.get_individual_parameters()

                print(f"\nLine trace {first_sheet_name_trace}:")
                zline_selection.display_info()
            else:
                print("Line trace not selected.")

        elif choice == 3:
            ztrans_selection = ZTrans.menu()
            print(f"{ztrans_selection.Z_pos_trans:.5f} {ztrans_selection.Zo_trans:.5f}")

        elif choice == 4:
            if zbus_selection is not None:
                print("\nBus Info:")
                zbus_selection.display_info()
            else:
                print("Please select a bus and station/transformer first.")

        elif choice == 5:
            if zbus_selection is not None and zline_selection is not None:
                print("\nFault Calculations:")
                primary_line_fault_calculation(zbus_selection, zline_selection)
                closest_distance, closest_fault_current = locate_primary_line_fault_l_g(zbus_selection, zline_selection) # testing
                print(f"\nDistance to fault from station: {closest_distance:.2f} mi") # testing
                print(f"Calculated current at distance: {closest_fault_current:.0f} Amps") # testing

            elif zbus_selection is None:
                print("Please select a bus and station/transformer.")
            else:
                print("Please load a line trace.")
            
        elif choice == 6:
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == '__main__':
    main()
