def zlinechop(dataframes):
    processed_dfs = {}
    for sheet_name, df in dataframes.items():
        if 'Line' in sheet_name:
            df_4kV = df[df['Voltage_Level'] == 4.6].copy()
            if not df_4kV.empty:
                # Drop rows where any of the elements is nan
                df_4kV.dropna(inplace=True)
                
                # Rename the columns for easier manipulation
                new_col_names = ['Type', 'Descriptor', '% Z+ Per 1000\' @ 100 MVA', 'Voltage_Level']
                df_4kV.columns = new_col_names
                
                # Convert impedance to complex number format
                df_4kV['% Z+ Per 1000\' @ 100 MVA'] = df_4kV['% Z+ Per 1000\' @ 100 MVA'].apply(lambda x: complex(x.replace('j', 'j')))
                
                # Label 'Wire Type' and 'Cable Type'
                wire_mask = df_4kV['Type'].str.contains('Wire Type')
                cable_mask = df_4kV['Type'].str.contains('Cable Type')
                df_4kV.loc[wire_mask, 'Type'] = 'Wire Type'
                df_4kV.loc[cable_mask, 'Type'] = 'Cable Type'
                
                processed_dfs[sheet_name] = df_4kV
                
    return processed_dfs