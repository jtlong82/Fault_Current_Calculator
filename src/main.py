from zbusmenu import zbusmenu
from ZBusClass import ZBus
from zlinechop import zlinechop
from GetExcel import load_impedance_sheets
from GetExcel import load_line_trace

def main():
    # Load impedance sheets and clean dataframes
    bus_dataframes = load_impedance_sheets()
    line_dataframes = bus_dataframes
    zbus_selection = None
    line_param_dataframes = None

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
            line_param_dataframes = load_line_trace()
            #zline_4kv = zlinechop4kv(line_dataframes)
            #for sheet_name, df in zline_4kv.items():
                #print(f'Sheet name: {sheet_name}')
                #print(df)
                #print('\n')

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
