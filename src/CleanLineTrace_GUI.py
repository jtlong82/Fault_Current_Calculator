import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import messagebox

# Import the original functions
from CleanLineTrace import clean_line_trace

def map_impedances_gui(df_linetrace, df_impedance, parent_window=None):
    """
    GUI version of map_impedances that uses dialog boxes instead of terminal input
    """
    # Import dialog classes
    try:
        from reactor_dialog import ReactorSelectionDialog
        from impedance_matching_dialog import ImpedanceMatchingDialog
    except ImportError:
        # Fallback to terminal version if dialogs not available
        from CleanLineTrace import map_impedances
        return map_impedances(df_linetrace, df_impedance)
    
    # Create new columns in df_linetrace for the impedance values
    df_linetrace['% Z+ @ 100 MVA'] = np.nan
    df_linetrace['% Zo @ 100 MVA'] = np.nan
    df_linetrace['Mapped Wire Type'] = None
    df_linetrace['Pole Type'] = None
    df_linetrace['Ground?'] = None

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

        # If multiple matches, show dialog
        elif len(filtered_df) > 1:
            if parent_window:
                dialog = ImpedanceMatchingDialog(parent_window, row.to_dict(), filtered_df, "multiple_matches")
                selected_row = dialog.get_result()
                
                if selected_row is not None:
                    df_linetrace.at[index, '% Z+ @ 100 MVA'] = selected_row['% Z+ @ 100 MVA']
                    df_linetrace.at[index, '% Zo @ 100 MVA'] = selected_row['% Zo @ 100 MVA']
                    df_linetrace.at[index, 'Mapped Wire Type'] = selected_row['Wire Type']
                    df_linetrace.at[index, 'Pole Type'] = selected_row['Pole Type']
                    df_linetrace.at[index, 'Ground?'] = selected_row['Ground?']
                else:
                    # User cancelled - use first option as default
                    impedance_row = filtered_df.iloc[0]
                    df_linetrace.at[index, '% Z+ @ 100 MVA'] = impedance_row['% Z+ @ 100 MVA']
                    df_linetrace.at[index, '% Zo @ 100 MVA'] = impedance_row['% Zo @ 100 MVA']
                    df_linetrace.at[index, 'Mapped Wire Type'] = impedance_row['Wire Type']
                    df_linetrace.at[index, 'Pole Type'] = impedance_row['Pole Type']
                    df_linetrace.at[index, 'Ground?'] = impedance_row['Ground?']
            else:
                # No parent window - use first match
                impedance_row = filtered_df.iloc[0]
                df_linetrace.at[index, '% Z+ @ 100 MVA'] = impedance_row['% Z+ @ 100 MVA']
                df_linetrace.at[index, '% Zo @ 100 MVA'] = impedance_row['% Zo @ 100 MVA']
                df_linetrace.at[index, 'Mapped Wire Type'] = impedance_row['Wire Type']
                df_linetrace.at[index, 'Pole Type'] = impedance_row['Pole Type']
                df_linetrace.at[index, 'Ground?'] = impedance_row['Ground?']
        
        # If no matches, provide other options based on 'Type' and 'Voltage_Level'
        else:
            filtered_by_type_voltage = df_impedance[
                (df_impedance['Type'] == row['Type']) & 
                (df_impedance['Voltage_Level'] == row['Voltage_Level'])
            ]
    
            if len(filtered_by_type_voltage) > 0:
                if parent_window:
                    dialog = ImpedanceMatchingDialog(parent_window, row.to_dict(), filtered_by_type_voltage, "no_match")
                    selected_row = dialog.get_result()
                    
                    if selected_row is not None:
                        df_linetrace.at[index, '% Z+ @ 100 MVA'] = selected_row['% Z+ @ 100 MVA']
                        df_linetrace.at[index, '% Zo @ 100 MVA'] = selected_row['% Zo @ 100 MVA']
                        df_linetrace.at[index, 'Mapped Wire Type'] = selected_row['Wire Type']
                        df_linetrace.at[index, 'Pole Type'] = selected_row['Pole Type']
                        df_linetrace.at[index, 'Ground?'] = selected_row['Ground?']
                    else:
                        # User cancelled - skip this line
                        messagebox.showwarning("Warning", f"No impedance selected for line at index {index}. Using zero impedance.")
                        df_linetrace.at[index, '% Z+ @ 100 MVA'] = 0j
                        df_linetrace.at[index, '% Zo @ 100 MVA'] = 0j
                else:
                    # No parent window - use first available option
                    impedance_row = filtered_by_type_voltage.iloc[0]
                    df_linetrace.at[index, '% Z+ @ 100 MVA'] = impedance_row['% Z+ @ 100 MVA']
                    df_linetrace.at[index, '% Zo @ 100 MVA'] = impedance_row['% Zo @ 100 MVA']
                    df_linetrace.at[index, 'Mapped Wire Type'] = impedance_row['Wire Type']
                    df_linetrace.at[index, 'Pole Type'] = impedance_row['Pole Type']
                    df_linetrace.at[index, 'Ground?'] = impedance_row['Ground?']
            else:
                messagebox.showwarning("Warning", f"No impedance options available for line at index {index}.")
                df_linetrace.at[index, '% Z+ @ 100 MVA'] = 0j
                df_linetrace.at[index, '% Zo @ 100 MVA'] = 0j

    # Check if the Voltage_Level 11.5 kV is present in the DataFrame
    if 11.5 in df_linetrace['Voltage_Level'].values:
        # Filter out the reactors
        reactor_df = df_impedance[df_impedance['Type'] == 'Reactor']
        
        if parent_window and len(reactor_df) > 0:
            # Show reactor selection dialog
            dialog = ReactorSelectionDialog(parent_window, reactor_df)
            result = dialog.get_result()
            
            if result and result['type'] != 'none':
                # Create a new reactor record
                reactor_record = {
                    'Type': 'Reactor',
                    'Conductor Size': 'Reactor',
                    'Conductor Type': 'Reactor',
                    'Length': 0,  # Reactors have no length
                    'Voltage_Level': 11.5,
                    '% Z+ @ 100 MVA': None,
                    '% Zo @ 100 MVA': 0j,  # Reactors have no Z0 (phase devices only)
                    'Mapped Wire Type': None,
                    'Pole Type': None,
                    'Ground?': None,
                    'Total % Z @ 100 MVA': None,
                    'Total % Zo @ 100 MVA': None
                }
                
                if result['type'] == 'predefined':
                    # Predefined reactor selected
                    reactor_row = result['data']
                    reactor_record['Mapped Wire Type'] = reactor_row['Wire Type']
                    reactor_record['% Z+ @ 100 MVA'] = reactor_row['% Z+ @ 100 MVA']
                elif result['type'] == 'custom':
                    # Custom reactor selected
                    reactor_record['Mapped Wire Type'] = result['name']
                    reactor_record['% Z+ @ 100 MVA'] = result['impedance']
                
                # Append the new reactor record to df_linetrace
                df_linetrace = pd.concat([df_linetrace, pd.DataFrame([reactor_record])], ignore_index=True)
        elif len(reactor_df) > 0:
            # No parent window but reactors available - add a default reactor
            messagebox.showinfo("Info", "11.5kV system detected. Adding default reactor.")
            reactor_row = reactor_df.iloc[0]
            reactor_record = {
                'Type': 'Reactor',
                'Conductor Size': 'Reactor',
                'Conductor Type': 'Reactor',
                'Length': 0,
                'Voltage_Level': 11.5,
                '% Z+ @ 100 MVA': reactor_row['% Z+ @ 100 MVA'],
                '% Zo @ 100 MVA': 0j,
                'Mapped Wire Type': reactor_row['Wire Type'],
                'Pole Type': None,
                'Ground?': None,
                'Total % Z @ 100 MVA': None,
                'Total % Zo @ 100 MVA': None
            }
            df_linetrace = pd.concat([df_linetrace, pd.DataFrame([reactor_record])], ignore_index=True)

    return df_linetrace