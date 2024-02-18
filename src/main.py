from menus import zbusmenu, fault_loc_menu, sel_time_menu
from Classes import ZBus, ZLine, ZTrans
from GetExcel import load_impedance_sheets, load_line_trace, load_clean_line_imp
from CleanLineTrace import map_impedances
from Calcs import primary_line_fault_calculation, locate_primary_line_fault_l_g, sec_trans_fault_calculation
from savetxt import savetxt

def main():
    # Load impedance sheets and clean dataframes
    bus_dataframes = load_impedance_sheets()
    line_dataframes = load_clean_line_imp()
    zbus_selection = None
    zline_selection = None
    ztrans_selection = None
    line_trace = None
    buffer = [] #collect data to write to terminal and file at end of calculations

    print("\nMenu Options: ")

    while True:
        print("\nCalculate: ")
        print("1. Available Bus Fault Current")
        print("2. Available Primary Line Fault Current")
        print("3. Available Transformer Secondary Fault Current")
        print("4. Fault Location")
        print("5. Short Circuit Form Letter")
        print("6. SEL U-Curves Operate and Reset Times")
        print("7. Exit")

        choice = int(input("Select: "))

        if choice == 1:
            buffer = []
            if bus_dataframes is not None:
                zbus_choice = zbusmenu(bus_dataframes)
                zbus_selection = ZBus(zbus_choice)
                zbus_selection.display_info(buffer)
                print("".join(buffer))
                savetxt(buffer)
            else:
                print("Please load impedance sheets first.")
                
        elif choice == 2:
            buffer = []
            if bus_dataframes is not None:
                zbus_choice = zbusmenu(bus_dataframes)
                zbus_selection = ZBus(zbus_choice)
                zbus_selection.display_info(buffer)
            else:
                print("Please load impedance sheets first.")
             
            ctr = float(input("CT Ratio on line relay (CTR:1): "))
            ptr = float(input("PT Ratio on line relay (PTR:1): "))
            print("\nLoad Line Trace...")
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
                zline_selection = ZLine(line_trace, first_sheet_name_trace, ctr, ptr)
                zline_selection.get_individual_parameters()
                buffer.append(f"\nLine trace {first_sheet_name_trace}:\n")
                zline_selection.display_info(buffer)

                if zbus_selection is not None and zline_selection is not None:
                    buffer.append(f"CT ratio: {ctr}:1   PT Ratio: {ptr}:1\n")
                    primary_line_fault_calculation(zbus_selection, zline_selection, buffer)
                    print("".join(buffer))
                    savetxt(buffer)
                elif zbus_selection is None:
                    print("Please select a bus and station/transformer.")
                else:
                    print("Please load a line trace.")
            else:
                print("Line trace not selected.")

        elif choice == 3:
            buffer = []
            if bus_dataframes is not None:
                zbus_choice = zbusmenu(bus_dataframes)
                zbus_selection = ZBus(zbus_choice)
                zbus_selection.display_info(buffer)
            else:
                print("Please load impedance sheets first.")
            
            ctr = float(input("CT Ratio on line relay (CTR:1): "))
            ptr = float(input("PT Ratio on line relay (PTR:1): "))
            print("\nLoad Line Trace...")
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
                zline_selection = ZLine(line_trace, first_sheet_name_trace, ctr, ptr)
                zline_selection.get_individual_parameters()
                buffer.append(f"\nLine trace {first_sheet_name_trace}:\n")
                zline_selection.display_info(buffer)

                if zbus_selection is not None and zline_selection is not None:
                    print(f"\n{first_sheet_name_trace}:")
                    primary_line_fault_calculation(zbus_selection, zline_selection, buffer)

                elif zbus_selection is None:
                    print("Please select a bus and station/transformer.")
                else:
                    print("Please load a line trace.")
            else:
                print("Line trace not selected.")

            ztrans_selection = ZTrans.menu()
            ztrans_selection.display_info(buffer)
            sec_trans_fault_calculation(zbus_selection, zline_selection, ztrans_selection, buffer)
            print("".join(buffer))
            savetxt(buffer)

        elif choice == 4:
            if bus_dataframes is not None:
                zbus_choice = zbusmenu(bus_dataframes)
                zbus_selection = ZBus(zbus_choice)
            else:
                print("Please load impedance sheets first.")

            print("\nLoad Line Trace...")
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
                zline_selection = ZLine(line_trace, first_sheet_name_trace, 1, 1) #entering 1 for ctr and ptr, not needed in this routine at moment
                zline_selection.get_individual_parameters()

                print(f"\nLine trace {first_sheet_name_trace}:")
                zline_selection.display_info()

                if zbus_selection is not None and zline_selection is not None:
                    print(f"\n{first_sheet_name_trace}:")
                    fault_loc_menu(zbus_selection, zline_selection)

                elif zbus_selection is None:
                    print("Please select a bus and station/transformer.")
                else:
                    print("Please load a line trace.")

            else:
                print("Line trace not selected.")

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
            sel_time_menu()
            
        elif choice == 7:
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == '__main__':
    main()