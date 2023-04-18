def zbusmenu(dataframes):
    print("Please select bus voltage level:")
    voltage_levels = sorted(set(sheet_name.split('-')[0] for sheet_name in dataframes))
    for idx, voltage in enumerate(voltage_levels):
        print(f"{idx + 1}. {voltage}")

    voltage_choice = int(input("Enter the number corresponding to the voltage level: ")) - 1
    selected_voltage = voltage_levels[voltage_choice]

    # Get the DataFrame corresponding to the selected voltage level
    voltage_df = dataframes[selected_voltage]

    print("\nPlease select a station:")
    station_names = voltage_df.iloc[1:, 0].tolist()  # Assuming station names are in the first column, starting from row 1
    for idx, station in enumerate(station_names):
        print(f"{idx + 1}. {station}")

    station_choice = int(input("Enter the number corresponding to the station: ")) - 1
    selected_station = station_names[station_choice]

    # Get the selected record from the DataFrame
    selected_record = voltage_df.iloc[station_choice + 1]  # Add 1 to account for the excluded label row

    # Print the selected record with labels
    print("\nSelected Record:")
    for label, value in zip(voltage_df.iloc[0], selected_record):
        print(f"{label}: {value}")

    return selected_record
