import pandas as pd

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



