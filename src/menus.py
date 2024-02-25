from Calcs import locate_primary_line_fault_3ph, locate_primary_line_fault_l_g, locate_primary_line_fault_l_l, locate_primary_line_fault_l_l_g
import tkinter as tk
from tkinter import filedialog

def zbusmenu(dataframes):
    # Filter dataframes to only include those with 'Bus' in the sheet name
    bus_dataframes = {k: v for k, v in dataframes.items() if 'Bus' in k}

    print("\nPlease select bus voltage level:")
    voltage_levels = sorted(set(sheet_name.split('-')[0] for sheet_name in bus_dataframes))
    for idx, voltage in enumerate(voltage_levels):
        print(f"{idx + 1}. {voltage}")

    voltage_choice = int(input("Enter the number corresponding to the voltage level: ")) - 1
    selected_voltage = voltage_levels[voltage_choice]

    # Select a record from the chosen voltage level DataFrame
    voltage_df = bus_dataframes[selected_voltage]
    voltage_df = voltage_df.reset_index(drop=True)  # Reset index to avoid any issues
    stations = voltage_df.iloc[:, 0].tolist()  # Assuming that the first column now has a name and contains the station names

    # Print menu for station selection
    print("\nSelect a station:")
    for idx, station in enumerate(stations, start=1):
        print(f"{idx}. {station}")

    # Get user input for station selection
    selected_station = int(input("Enter the number corresponding to the station you want to select: ")) - 1

    selected_record = voltage_df.iloc[selected_station]  # We no longer need to add 1, as we're using the true index
    # The index of selected_record should already be the column names, but you can reset it like this if needed
    # selected_record.index = voltage_df.columns

    return selected_record

def fault_loc_menu(ZBus_obj, Zline_obj):
    if ZBus_obj.voltage_level != 4.6:
        fault_types = {
                '1': '3 Phase',
                '2': 'Line to Line',
                '3': 'Line to Ground',
                '4': 'Double Line to Ground'
            }
        print("Select the fault type:")
        for key, value in fault_types.items():
            print(f"{key}. {value}")
        choice = input("Enter (1-4): ")
        fault_type = fault_types.get(choice, None) 
    else:
        fault_types = {
                '1': '3 Phase',
                '2': 'Line to Line',
            }
        print("Select the fault type:")
        for key, value in fault_types.items():
            print(f"{key}. {value}")
        choice = input("Enter (1-2): ")
        fault_type = fault_types.get(choice, None) 

    fault_mag = int(input("Enter the fault magnitude to the nearest amp: "))

    while True:
        print("\nCalculate Fault Location: ")
        print("1. Quick")
        print("2. Accurate")
        print("3. Exit")
        print(f"Fault Mag = {fault_mag}") #DEBUG
        print(f"Fault Type = {fault_type}") #DEBUG

        choice = int(input("Select: "))

        if choice == 1 and fault_type == '3 Phase':
            locate_primary_line_fault_3ph(ZBus_obj, Zline_obj, fault_mag)
        elif choice == 1 and fault_type == 'Line to Ground':
            locate_primary_line_fault_l_g(ZBus_obj, Zline_obj, fault_mag)
        elif choice == 1 and fault_type == 'Line to Line':
            locate_primary_line_fault_l_l(ZBus_obj, Zline_obj, fault_mag)
        elif choice == 1 and fault_type == 'Double Line to Ground':
            locate_primary_line_fault_l_l_g(ZBus_obj, Zline_obj, fault_mag)
        elif choice == 2 and fault_type == '3 Phase':
            break
        elif choice == 2 and fault_type == 'Line to Ground':
            break
        elif choice == 2 and fault_type == 'Line to Line':
            break
        elif choice == 2 and fault_type == 'Double Line to Ground':
            break
        else:
            break

    return

def sel_time_menu():
    time_curves = {
        '1': 'U1',
        '2': 'U2',
        '3': 'U3',
        '4': 'U4',
        '5': 'U5',
    }

    print("\nSelect the SEL U-Curve:")
    for key, value in time_curves.items():
        print(f"{key}. {value}")
    choice = input("Enter (1-5): ")
    time_curve = time_curves.get(choice, None)

    td = float(input("Time Dial Setting: "))
    tap = float(input("Tap Setting: "))
    ctr = float(input("CT Ratio (CTR:1): "))
    pri_fault = float(input("Primary Fault Current: "))
    m = pri_fault / (tap * ctr)
    
    if time_curve == 'U1':
        op_time = td * (0.0226 + (0.0104 / ((m ** 0.02) - 1)))
        rst_time = td * (1.08 / (1 - (m ** 2)))
    elif time_curve == 'U2':
        op_time = td * (0.180 + (5.95 / ((m ** 2) - 1)))
        rst_time = td * (5.95 / (1 - (m ** 2)))
    elif time_curve == 'U3':
        op_time = td * (0.0963 + (3.88 / ((m ** 2) - 1)))
        rst_time = td * (3.88 / (1 - (m ** 2)))
    elif time_curve == 'U4':
        op_time = td * (0.0352 + (5.67 / ((m ** 2) - 1)))
        rst_time = td * (5.67/ (1 - (m ** 2)))
    elif time_curve == 'U5':
        op_time = td * (0.0262 + (0.00342/ ((m ** 0.02) - 1)))
        rst_time = td * (0.323 / (1 - (m ** 2)))
    else:
        return    
    
    op_time_cy = op_time / 0.0166666666666666667
    rst_time_cy = rst_time / 0.0166666666666666667
    
    print(f"Operation time: {op_time:.2f} seconds, {op_time_cy:.1f} cycles")
    print(f"Reset time: {-rst_time:.2f} seconds, {-rst_time_cy:.1f} cycles")

    return

def savetxt(buffer):
    # Initialize Tkinter root
    root = tk.Tk()
    root.withdraw()  # Hides the small Tkinter window

    # Ask user if they want to save the output using a Tkinter dialog
    save_file = input("Save file to .txt? (y/n)")
    if save_file and save_file.strip().lower() == 'y':
        # Open save file dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Choose filename"
        )

        # Check if a file path was provided
        if file_path:
            # Write the buffer to the file with UTF-8 encoding
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write("".join(buffer))
        else:
            print("File save cancelled.")

    # Destroy the Tkinter root (clean up)
    root.destroy()