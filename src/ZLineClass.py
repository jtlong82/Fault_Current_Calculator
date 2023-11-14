import pandas as pd
import cmath
import math

class ZLine:
    def __init__(self, df_linetrace, label):
        self.df_linetrace = df_linetrace
        self.label = label
        self.total_Z_100MVA = 0 
        self.total_Zo_100MVA = 0
        self.total_length_feet = 0
        self.total_length_miles = 0


    def get_individual_parameters(self):
        self.total_Z_100MVA = 0  # Initialize accumulator for 'Total % Z @ 100 MVA'
        self.total_Zo_100MVA = 0
        self.total_length_feet = 0
        self.total_length_miles = 0

        for index, row in self.df_linetrace.iterrows():
            line_type = str(row['Type'])
            conductor_size = str(row['Conductor Size'])
            conductor_type = str(row['Conductor Type'])
            length = float(row['Length'])
            voltage_level = float(row['Voltage_Level'])
            z_100MVA = complex(row['% Z+ @ 100 MVA'])
            zo_100MVA = complex(row['% Zo @ 100 MVA'])
            mapped_wire_type = str(row['Mapped Wire Type'])
            pole_type = str(row['Pole Type'])
            ground = str(row['Ground?'])
            
            conversion_factor = 5280 if (line_type == 'OH Pri. Conductor' and (voltage_level == 36 or voltage_level == 11.5)) else 1000

            total_pos_impedance = z_100MVA * (length / conversion_factor)
            total_zero_impedance = zo_100MVA * (length / conversion_factor)
            
            formatted_pos_impedance = "{:.2f}+{:.2f}j".format(total_pos_impedance.real, total_pos_impedance.imag)
            formatted_zero_impedance = "{:.2f}+{:.2f}j".format(total_zero_impedance.real, total_zero_impedance.imag)

            self.df_linetrace.at[index, 'Total % Z @ 100 MVA'] = formatted_pos_impedance
            self.df_linetrace.at[index, 'Total % Zo @ 100 MVA'] = formatted_zero_impedance

            # Update the accumulators
            self.total_Z_100MVA += total_pos_impedance
            self.total_Zo_100MVA += total_zero_impedance
            self.total_length_feet += length
            self.total_length_miles += length/5280

            #Convert to Ohms
            self.total_Z_100MVA_pu = self.total_Z_100MVA / 100
            self.total_Zo_100MVA_pu = self.total_Zo_100MVA / 100

    def display_info(self):
        print(self.df_linetrace)
        print(f"Z+ Total Line: {self.total_Z_100MVA.real:.2f}+{self.total_Z_100MVA.imag:.2f}j %")
        print(f"Z0 Total Line: {self.total_Zo_100MVA.real:.2f}+{self.total_Zo_100MVA.imag:.2f}j %")
        print(f"Total Length: {self.total_length_feet:.0f} ft - {self.total_length_miles:.3f} mi")



   

