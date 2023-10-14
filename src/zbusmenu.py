def zbusmenu(dataframes):
    # Filter dataframes to only include those with 'Bus' in the sheet name
    bus_dataframes = {k: v for k, v in dataframes.items() if 'Bus' in k}

    print("Please select bus voltage level:")
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
    print("Please select a station:")
    for idx, station in enumerate(stations, start=1):
        print(f"{idx}. {station}")

    # Get user input for station selection
    selected_station = int(input("Enter the number corresponding to the station you want to select: ")) - 1

    selected_record = voltage_df.iloc[selected_station]  # We no longer need to add 1, as we're using the true index
    # The index of selected_record should already be the column names, but you can reset it like this if needed
    # selected_record.index = voltage_df.columns

    return selected_record

