def clean_dataframe(df):
    # Check if the DataFrame contains the word "bus"
    if any("Bus" in str(val).lower() for val in df.values()):
        # Drop the first two rows
        df = df.iloc[2:]
        # Drop columns B, C, D, H, I, J, N, O, P, Q
        columns_to_drop = ['B', 'C', 'D', 'H', 'I', 'J', 'N', 'O', 'P', 'Q']
        df = df.drop(columns=columns_to_drop, errors='ignore')
    return df
