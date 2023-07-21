
    
def clean_dataframe(dataframe):
    cleaned_dataframe = {}
    
    for sheet_name, df in dataframe.items():
        # Check if the sheet name contains the word "Bus"
        if "Bus" in sheet_name:
            # Drop the first two rows
            df = df.drop([0, 1], errors='ignore')

            # Get column labels by index
            columns_to_drop = df.columns[[7, 8, 9, 13, 14, 15, 16, 17, 18, 19, 20]]

            # Drop the columns
            df = df.drop(columns=columns_to_drop, errors='ignore')

            # Remove empty rows
            df = df.dropna(axis=0, how='all')

            # Remove empty columns
            df = df.dropna(axis=1, how='all')
            
            # Renumber columns
            df.columns = range(df.shape[1])

            # Set None values in iloc[7], iloc[8], and iloc[9] to complex(0)
            for col_idx in [7, 8, 9]:
                if col_idx < df.shape[1]:  # Check if the DataFrame has enough columns
                    df.iloc[:, col_idx] = df.iloc[:, col_idx].apply(lambda x: complex(0) if x is None else x)

        # Check if the sheet name contains the word "36kV Line"
        elif "36kV Line" in sheet_name:
            # Drop rows
            df = df.drop([0, 1, 3, 37, 38], errors='ignore')

            # Get column labels by index
            columns_to_drop = df.columns[[2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15]]

            # Drop the columns
            df = df.drop(columns=columns_to_drop, errors='ignore')

            # Remove empty rows
            df = df.dropna(axis=0, how='all')

            # Remove empty columns
            df = df.dropna(axis=1, how='all')

        # Check if the sheet name contains the word "13kV Line"
        elif "13kV Line" in sheet_name:
            # Drop rows
            df = df.drop([0, 1, 3, 11, 13, 22, 23, 24, 25], errors='ignore')

            # Get column labels by index
            columns_to_drop = df.columns[[2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15]]

            # Drop the columns
            df = df.drop(columns=columns_to_drop, errors='ignore')

            # Remove empty rows
            df = df.dropna(axis=0, how='all')

            # Remove empty columns
            df = df.dropna(axis=1, how='all')

        # Check if the sheet name contains the word "11kV Line"
        elif "11kV Line" in sheet_name:
            # Drop rows
            df = df.drop([0, 1, 3, 9, 10, 11, 13, 17, 18, 19, 20, 21, 22, 28, 29], errors='ignore')

            # Get column labels by index
            columns_to_drop = df.columns[[2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15]]

            # Drop the columns
            df = df.drop(columns=columns_to_drop, errors='ignore')

            # Remove empty rows
            df = df.dropna(axis=0, how='all')

            # Remove empty columns
            df = df.dropna(axis=1, how='all')

        # Check if the sheet name contains the word "4kV Line"
        elif "4kV Line" in sheet_name:
            # Drop rows
            df = df.drop([0, 1, 3, 12, 14], errors='ignore')

            # Get column labels by index
            columns_to_drop = df.columns[[2, 3, 4, 5, 6, 7]]

            # Drop the columns
            df = df.drop(columns=columns_to_drop, errors='ignore')

            # Remove empty rows
            df = df.dropna(axis=0, how='all')

            # Remove empty columns
            df = df.dropna(axis=1, how='all')

        # Reset index to renumber rows for both "Bus" and "Line" sheets
        df = df.reset_index(drop=True)
            
        # Renumber columns for both "Bus" and "Line" sheets
        df.columns = range(df.shape[1])
        
        cleaned_dataframe[sheet_name] = df
        
    return cleaned_dataframe
