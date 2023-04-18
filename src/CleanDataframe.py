def clean_dataframe(df):
    # Check if the DataFrame contains the word "bus"
    if any("Bus" in str(val).lower() for val in df.values):
        # Drop the first two rows
        df = df.iloc[2:]
        
        # Get column labels by index
        columns_to_drop = df.columns[[1, 2, 3, 7, 8, 9, 13, 14, 15, 16]]
        
        # Drop the columns
        df = df.drop(columns=columns_to_drop, errors='ignore')
    return df
