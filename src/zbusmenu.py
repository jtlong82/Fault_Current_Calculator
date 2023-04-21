def zbusmenu(dataframes):
    print("Please select bus voltage level:")
    voltage_levels = sorted(set(sheet_name.split('-')[0] for sheet_name in dataframes))
    for idx, voltage in enumerate(voltage_levels):
        print(f"{idx + 1}. {voltage}")

    voltage_choice = int(input("Enter the number corresponding to the voltage level: ")) - 1
    selected_voltage = voltage_levels[voltage_choice]

    # Select a record from the chosen voltage level DataFrame
    voltage_df = dataframes[selected_voltage]
    voltage_df = voltage_df.reset_index(drop=True)  # Reset index to avoid any issues
    stations = voltage_df.iloc[1:, 0].tolist()  # Get station names from the first column, excluding the header row

    # Print menu for station selection
    print("Please select a station:")
    for idx, station in enumerate(stations, start=1):
        print(f"{idx}. {station}")

    # Get user input for station selection
    selected_station = int(input("Enter the number corresponding to the station you want to select: ")) - 1

    selected_record = voltage_df.iloc[selected_station + 1]  # Add 1 to account for the excluded label row
    selected_record.index = voltage_df.iloc[0]  # Set the index of the selected_record to the column names from the original DataFrame

    return selected_record