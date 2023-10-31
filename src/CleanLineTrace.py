import pandas as pd
import numpy as np

def clean_line_trace(dataframes):
    cleaned_line_trace = {}
    
    for sheet_name, df in dataframes.items():
        # Set the column names using the row at index 2
        df.columns = df.iloc[2]
        
        # Remove the name of the columns object
        df.columns.name = None

        # Drop the first three rows (index 0, 1, 2)
        df = df.drop([0, 1, 2])
        
        # Reset the index
        df = df.reset_index(drop=True)
        
        # Drop unnecessary columns from the data portion based on column names
        columns_to_drop = ['Conductor Quantity', 'Conductor Description', 'Secondary Voltage', 'Substation', 'Prim Volt', 'Phasing', 'Start Flag', 'Stop Flag']
        df = df.drop(columns=columns_to_drop, errors='ignore')
         
        # Filter out rows containing "Secd.", "Serv.", or "Light" in the 'Type' column
        df = df[~df['Type'].str.contains("Secd.|Serv.|Light", case=False, na=False)]

        # Remove leading and trailing spaces from string columns
        string_cols = ['Type', 'Conductor Type']
        df[string_cols] = df[string_cols].apply(lambda x: x.str.strip())

        # Renaming 'Conductor Type' entries based on their first character
        df['Conductor Type'] = df['Conductor Type'].apply(lambda x: 'AL' if str(x).startswith('A') else ('CU' if str(x).startswith('C') else x))

        # Remove any asterisks from 'Conductor Size'
        df['Conductor Size'] = df['Conductor Size'].str.replace("*", "", regex=False)

        # Convert 'Length' to integers
        df['Length'] = df['Length'].astype('int', errors='ignore')

        # Normalize the 'Type' entries to "OH Pri. Conductor"
        df['Type'] = df['Type'].str.replace("OH Pri. Conductor \(U\)|OH Pri. Conductor \(I\)", "OH Pri. Conductor", regex=True)

        # Group by 'Type', 'Conductor Size', and 'Conductor Type' and sum up the 'Length'
        df = df.groupby(['Type', 'Conductor Size', 'Conductor Type'], as_index=False).agg({'Length': 'sum'})

        cleaned_line_trace[sheet_name] = df

    return cleaned_line_trace

def map_impedances(df_linetrace, df_impedance):
    # Create new columns in df_linetrace for the impedance values
    df_linetrace['% Z+ @ 100 MVA'] = np.nan
    df_linetrace['% Zo @ 100 MVA'] = np.nan
    df_linetrace['Mapped Wire Type'] = None  # Initialize a new column for "Wire Type"
    df_linetrace['Pole Type'] = None  # Initialize a new column for "Pole Type"
    df_linetrace['Ground?'] = None  # Initialize a new column for "Ground?"

    # Iterate over each row in df_linetrace
    for index, row in df_linetrace.iterrows():
        # Filter df_impedance based on 'Type', 'Conductor Size', 'Conductor Type', and 'Voltage_Level'
        filtered_df = df_impedance[
            (df_impedance['Type'] == row['Type']) & 
            (df_impedance['Conductor Size'] == row['Conductor Size']) & 
            (df_impedance['Conductor Type'] == row['Conductor Type']) & 
            (df_impedance['Voltage_Level'] == row['Voltage_Level'])
        ]

        # If there's only one match, update df_linetrace with the impedance values
        if len(filtered_df) == 1:
            impedance_row = filtered_df.iloc[0]
            df_linetrace.at[index, '% Z+ @ 100 MVA'] = impedance_row['% Z+ @ 100 MVA']
            df_linetrace.at[index, '% Zo @ 100 MVA'] = impedance_row['% Zo @ 100 MVA']
            df_linetrace.at[index, 'Mapped Wire Type'] = impedance_row['Wire Type']
            df_linetrace.at[index, 'Pole Type'] = impedance_row['Pole Type']
            df_linetrace.at[index, 'Ground?'] = impedance_row['Ground?']

       # If multiple matches, prompt the user
        elif len(filtered_df) > 1:
            print(f"\nMultiple impedance records found for the following line:")
            print(row.to_string())
            print("\nPlease select one of the available choices:")
    
            # Print header
            print(f"{'Choice':<10} {'Conductor Size':<20} {'Conductor Type':<20} {'Pole Type':<20} {'Ground?':<20}")
            print("="*80)
    
            for idx, (i, f_row) in enumerate(filtered_df.iterrows()):
                conductor_size = f_row['Conductor Size'] if f_row['Conductor Size'] is not None else 'N/A'
                conductor_type = f_row['Conductor Type'] if f_row['Conductor Type'] is not None else 'N/A'
                pole_type = f_row['Pole Type'] if f_row['Pole Type'] is not None else 'N/A'
                ground = f_row['Ground?'] if f_row['Ground?'] is not None else 'N/A'

                print(f"{idx + 1:<10} {conductor_size:<20} {conductor_type:<20} {pole_type:<20} {ground:<20}")

            selection = int(input("Enter the number corresponding to your choice: ")) - 1
            selected_index = filtered_df.index[selection]
            impedance_row = filtered_df.loc[selected_index]
            df_linetrace.at[index, '% Z+ @ 100 MVA'] = impedance_row['% Z+ @ 100 MVA']
            df_linetrace.at[index, '% Zo @ 100 MVA'] = impedance_row['% Zo @ 100 MVA']
            df_linetrace.at[index, 'Mapped Wire Type'] = impedance_row['Wire Type']
            df_linetrace.at[index, 'Pole Type'] = impedance_row['Pole Type']
            df_linetrace.at[index, 'Ground?'] = impedance_row['Ground?']
        
        # If no matches, provide other options based on 'Type' and 'Voltage_Level'
        else:
            print(f"\nNo impedance records found for the following line:")
            print(row.to_string())
            filtered_by_type_voltage = df_impedance[
                (df_impedance['Type'] == row['Type']) & 
                (df_impedance['Voltage_Level'] == row['Voltage_Level'])
            ]
    
            if len(filtered_by_type_voltage) > 0:
                print("\nHowever, there are other options with the same Type and Voltage Level. Please select one:")
        
                # Print header
                print(f"{'Choice':<10} {'Conductor Size':<20} {'Conductor Type':<20} {'Pole Type':<20} {'Ground?':<20}")
                print("="*80)
        
                for idx, (i, f_row) in enumerate(filtered_by_type_voltage.iterrows()):
                    conductor_size = f_row['Conductor Size'] if f_row['Conductor Size'] is not None else 'N/A'
                    conductor_type = f_row['Conductor Type'] if f_row['Conductor Type'] is not None else 'N/A'
                    pole_type = f_row['Pole Type'] if f_row['Pole Type'] is not None else 'N/A'
                    ground = f_row['Ground?'] if f_row['Ground?'] is not None else 'N/A'

                    print(f"{idx + 1:<10} {conductor_size:<20} {conductor_type:<20} {pole_type:<20} {ground:<20}")

                selection = int(input("Enter the number corresponding to your choice: ")) - 1
                selected_index = filtered_by_type_voltage.index[selection]
                impedance_row = filtered_by_type_voltage.loc[selected_index]
                df_linetrace.at[index, '% Z+ @ 100 MVA'] = impedance_row['% Z+ @ 100 MVA']
                df_linetrace.at[index, '% Zo @ 100 MVA'] = impedance_row['% Zo @ 100 MVA']
                df_linetrace.at[index, 'Mapped Wire Type'] = impedance_row['Wire Type']
                df_linetrace.at[index, 'Pole Type'] = impedance_row['Pole Type']
                df_linetrace.at[index, 'Ground?'] = impedance_row['Ground?']
            else:
                print("No alternative options available.")

    # Check if the Voltage_Level 11.5 kV is present in the DataFrame
    if 11.5 in df_linetrace['Voltage_Level'].values:
        # Filter out the reactors
        reactor_df = df_impedance[df_impedance['Type'] == 'Reactor']
        
        print("\nReactor Selection.")
        print("Please select one of the available reactor choices, enter a custom reactor, or select 'No Reactor':")
        
        # Print header
        print(f"{'Choice':<10} {'Type':<20} {'Wire Type':<20} {'% Z+ @ 100 MVA':<20}")
        print("="*80)

        # Display predefined reactors
        for idx, (i, f_row) in enumerate(reactor_df.iterrows()):
            print(f"{idx + 1:<10} {f_row['Type']:<20} {f_row['Wire Type']:<20}  {f_row['% Z+ @ 100 MVA']:<20}")

        # Custom reactor option
        print(f"{len(reactor_df) + 1:<10} Custom")
        
        # No reactor option
        print(f"{len(reactor_df) + 2:<10} No Reactor")

        selection = int(input("Enter the number corresponding to your choice: "))

        reactor_record = {
                'Type': None,
                '% Z+ @ 100 MVA': None,
            }
        
        # Create a new reactor record only if a reactor is selected
        if selection <= len(reactor_df) or selection == len(reactor_df) + 1:
            if selection == len(reactor_df) + 1:  # Custom reactor selected
                reactor_record['Type'] = input("Enter the custom reactor Type: ")
                reactor_record['% Z+ @ 100 MVA'] = complex(input("Enter the custom reactor % Z+ @ 100 MVA: ")) 
                # Append the new reactor record to df_linetrace
                df_linetrace = pd.concat([df_linetrace, pd.DataFrame([reactor_record])], ignore_index=True)
            else:  # Predefined reactor selected
                selected_index = reactor_df.index[selection - 1]
                reactor_row = reactor_df.loc[selected_index]
                reactor_record['Type'] = reactor_row['Type']
                reactor_record['Mapped Wire Type'] = reactor_row['Wire Type']
                reactor_record['% Z+ @ 100 MVA'] = reactor_row['% Z+ @ 100 MVA']
                # Append the new reactor record to df_linetrace
                df_linetrace = pd.concat([df_linetrace, pd.DataFrame([reactor_record])], ignore_index=True)

    # KEEP FOR DEBUGGING
    #print("\nDataFrame: df_linetrace")
    #print(df_linetrace)
    #print('\n')

    return df_linetrace
   