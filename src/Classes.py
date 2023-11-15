import pandas as pd
import cmath
import math
import numpy as np

class ZBus:
    def __init__(self, selected_record):
        self.station = str(selected_record.iloc[0])
        self.supplied_from = str(selected_record.iloc[1])
        self.transformer_kva = str(selected_record.iloc[2])
        self.tap_ratio = str(selected_record.iloc[3])
        self.z_100MVA = complex(selected_record.iloc[4])
        self.d_e_120V = float(selected_record.iloc[5])
        self.short_circuit_MVA_1 = float(selected_record.iloc[6])
        self.voltage_level = float(selected_record['Voltage_Level'])
        self.MVA_base = 100
        self.voltage_level_pu = 1

        # Check if selected_record has enough elements for 4kv bus sheet (only has 8 columns)
        if len(selected_record) > 7:
            self.zo_100MVA = complex(selected_record.iloc[7])
        else:
            self.zo_100MVA = complex(0)

        if len(selected_record) > 8:
            self.z_L_G_100MVA = complex(selected_record.iloc[8])
        else:
            self.z_L_G_100MVA = complex(0)

        if len(selected_record) > 9:
            self.short_circuit_MVA_2 = float(selected_record.iloc[9])
        else:
            self.short_circuit_MVA_2 = 0  # or any default value 

        # Calculating the 3-phase fault current as soon as the object is initiated
        self.Zbase = (self.voltage_level ** 2) / self.MVA_base
        self.Ibase = (self.MVA_base) / ((3 ** 0.5) * self.voltage_level)
        self.X_R_pos = (self.z_100MVA.imag / 100) / (self.z_100MVA.real / 100)

        #3-ph fault
        self.three_ph_fault_pu = self.voltage_level_pu / (self.z_100MVA / 100) # Ipu = Vf/Z1
        self.three_ph_fault_pu_mag = abs(self.three_ph_fault_pu)
        self.three_ph_fault_pu_ang_rads = cmath.phase(self.three_ph_fault_pu)
        self.three_ph_fault_pu_ang_degs = math.degrees(self.three_ph_fault_pu_ang_rads)
        self.three_ph_fault = (self.three_ph_fault_pu_mag * self.Ibase * 1000)
        #Individual phases 3-ph fault
        self.three_ph_fault_Aph = self.three_ph_fault
        self.three_ph_fault_pu_ang_degs_Aph = self.three_ph_fault_pu_ang_degs
        self.three_ph_fault_Bph = self.three_ph_fault
        self.three_ph_fault_pu_ang_degs_Bph = self.three_ph_fault_pu_ang_degs + 120
        self.three_ph_fault_Cph = self.three_ph_fault
        self.three_ph_fault_pu_ang_degs_Cph = self.three_ph_fault_pu_ang_degs - 120

        # Calculating the line-to-line fault current as soon as the object is initiated
        self.l_l_fault_pos = self.voltage_level_pu / ((self.z_100MVA / 100) * 2) #Ia positive sequence
        self.l_l_fault_pu = (-1j) * (3 ** 0.5) * self.l_l_fault_pos #Ib fault current pu
        self.l_l_fault_pu_mag = abs(self.l_l_fault_pu)
        self.l_l_fault_pu_ang_rads = cmath.phase(self.l_l_fault_pu)
        self.l_l_fault_pu_ang_degs = math.degrees(self.l_l_fault_pu_ang_rads)
        self.l_l_fault = self.l_l_fault_pu_mag * self.Ibase * 1000
        #Individual phases line-to-line fault
        self.l_l_fault_Bph = self.l_l_fault
        self.l_l_fault_pu_ang_degs_Bph = self.l_l_fault_pu_ang_degs
        self.l_l_fault_Cph = self.l_l_fault
        self.l_l_fault_pu_ang_degs_Cph = self.l_l_fault_pu_ang_degs + 180
        
        if self.voltage_level != 4.6:
            # Calculating the line to ground fault current
            self.X_R_zero = (2 * (self.z_100MVA.imag / 100) + (self.zo_100MVA.imag / 100)) / (2 * (self.z_100MVA.real / 100) + (self.zo_100MVA.real / 100))
            self.l_g_fault_pu = 2 * (self.z_100MVA / 100) + (self.zo_100MVA / 100)
            self.l_g_fault_pu = ((self.l_g_fault_pu.conjugate()) / ((self.l_g_fault_pu.real) ** 2 + (self.l_g_fault_pu.imag) ** 2))
            self.l_g_fault_pu_mag = abs(self.l_g_fault_pu)
            self.l_g_fault_pu_ang_rads = cmath.phase(self.l_g_fault_pu)
            self.l_g_fault_pu_ang_degs = math.degrees(self.l_g_fault_pu_ang_rads)
            self.l_g_fault = 3 * self.l_g_fault_pu_mag * self.Ibase * 1000

            # Calculating the line-to-line-to-ground fault current as soon as the object is initiated
            self.l_l_g_fault_Z2_pu = (self.z_100MVA / 100)
            #print(f"Z2 pu: {self.l_l_g_fault_Z2_pu}")
            self.l_l_g_fault_Zf_pu = ((self.l_l_g_fault_Z2_pu) * (self.zo_100MVA / 100)) / ((self.zo_100MVA / 100) + (self.l_l_g_fault_Z2_pu))
            #print(f"Zf pu: {self.l_l_g_fault_Zf_pu}")
            self.l_l_g_fault_pos_pu = self.voltage_level_pu / ((self.z_100MVA / 100) + self.l_l_g_fault_Zf_pu) #I1 positive sequence
            #print(f"I1 pu: {self.l_l_g_fault_pos_pu}")
            self.l_l_g_fault_neg_pu = (-self.l_l_g_fault_pos_pu) * ((self.zo_100MVA / 100) / ((self.zo_100MVA / 100) + (self.l_l_g_fault_Z2_pu))) #I2 negative sequence
            #print(f"I2 pu: {self.l_l_g_fault_neg_pu}")
            self.l_l_g_fault_zero_pu = (-self.l_l_g_fault_pos_pu) * ((self.l_l_g_fault_Z2_pu) / ((self.zo_100MVA / 100) + (self.l_l_g_fault_Z2_pu))) #I0 zero sequence
            #print(f"I0 pu: {self.l_l_g_fault_zero_pu}")
            A = np.array([[1, 1, 1],[1, -0.5 - 0.866j, -0.5 + 0.866j],[1, -0.5 + 0.866j, -0.5 - 0.866j]]) #A matrix
            #print(f"A matrix: {A}")
            I_seq = np.array([self.l_l_g_fault_zero_pu, self.l_l_g_fault_pos_pu, self.l_l_g_fault_neg_pu]) #Sequence currents matrix
            #print(f"Sequence Matrix: {I_seq}")
            I_phase = np.dot(A, I_seq)
            #print(f"Phase Matrix: {I_phase}")
            self.l_l_g_fault_Aph_pu, self.l_l_g_fault_Bph_pu, self.l_l_g_fault_Cph_pu = I_phase #Individual phases line-to-line-to-ground fault
            self.l_l_g_fault_Bph = abs(self.l_l_g_fault_Bph_pu) * self.Ibase * 1000
            self.l_l_g_fault_pu_ang_rads_Bph = cmath.phase(self.l_l_g_fault_Bph_pu)
            self.l_l_g_fault_pu_ang_degs_Bph = math.degrees(self.l_l_g_fault_pu_ang_rads_Bph)
            self.l_l_g_fault_Cph = abs(self.l_l_g_fault_Cph_pu) * self.Ibase * 1000
            self.l_l_g_fault_pu_ang_rads_Cph = cmath.phase(self.l_l_g_fault_Cph_pu)
            self.l_l_g_fault_pu_ang_degs_Cph = math.degrees(self.l_l_g_fault_pu_ang_rads_Cph)
        
    def display_info(self):
        print(f"Station: {self.station}")
        print(f"Voltage: {self.voltage_level} kV")
        print(f"Supplied from (System): {self.supplied_from} ")
        print(f"Transformer(s): {self.transformer_kva} kVA")
        print(f"Tap Ratio: {self.tap_ratio} kV")
        print(f"% Z @ 100MVA: {self.z_100MVA}")
        # print(f"D e @ 120 V: {self.d_e_120V:.2f}")
        # print(f"3-Phase Short Circuit MVA: {self.short_circuit_MVA_1:.2f}")
        if self.voltage_level != 4.6:
            print(f"% Zo @ 100MVA: {self.zo_100MVA}")
            # print(f"% Z (L_G) @ 100MVA: {self.z_L_G_100MVA}")
            # print(f"L_G Short Circuit MVA: {self.short_circuit_MVA_2:.2f}")
        print(f"X/R Positive Seq at Bus: {self.X_R_pos:.2f}")
        if self.voltage_level != 4.6:
            print(f"X/R Zero Seq at Bus: {self.X_R_zero:.2f}")
        print("\nAvailable fault currents at Bus: ")
        print(f"ABC: {self.three_ph_fault:.0f}∠{self.three_ph_fault_pu_ang_degs:.2f}° Amps")
        if self.voltage_level != 4.6:
            print(f"AG: {self.l_g_fault:.0f}∠{self.l_g_fault_pu_ang_degs:.2f}° Amps")
        print(f"BC: {self.l_l_fault:.0f}∠{self.l_l_fault_pu_ang_degs:.2f}° Amps")
        if self.voltage_level != 4.6:
            print(f"BCG: {self.l_l_g_fault_Bph:.0f}∠{self.l_l_g_fault_pu_ang_degs_Bph :.2f}° Amps")

        print("\nAvailable fault currents at Bus per phase: ")
        print(f"ABC:")
        print(f"A: {self.three_ph_fault_Aph:.0f}∠{self.three_ph_fault_pu_ang_degs_Aph:.2f}° Amps    B: {self.three_ph_fault_Bph:.0f}∠{self.three_ph_fault_pu_ang_degs_Bph:.2f}° Amps    C: {self.three_ph_fault_Cph:.0f}∠{self.three_ph_fault_pu_ang_degs_Cph:.2f}° Amps")
        if self.voltage_level != 4.6:
            print(f"AG:")
            print(f"A: {self.l_g_fault:.0f}∠{self.l_g_fault_pu_ang_degs:.2f}° Amps    B: {0:.0f}∠{0:.2f}° Amps    C: {0:.0f}∠{0:.2f}° Amps")
        print(f"BC:")
        print(f"A: {0:.0f}∠{0:.2f}° Amps    B: {self.l_l_fault_Bph:.0f}∠{self.l_l_fault_pu_ang_degs_Bph:.2f}° Amps    C: {self.l_l_fault_Cph:.0f}∠{self.l_l_fault_pu_ang_degs_Cph:.2f}° Amps")
        if self.voltage_level != 4.6:
            print(f"BCG:")
            print(f"A: {0:.0f}∠{0:.2f}° Amps    B: {self.l_l_g_fault_Bph:.0f}∠{self.l_l_g_fault_pu_ang_degs_Bph:.2f}° Amps    C: {self.l_l_g_fault_Cph:.0f}∠{self.l_l_g_fault_pu_ang_degs_Cph:.2f}° Amps")




####################################################################################################################################################
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



####################################################################################################################################################
class ZTrans:
    # Predefined transformers dictionary
    predefined_transformers = {
        '45': (2.7, 1.2),
        '75': (2.7, 1.6),
        '112.5': (3.1, 1.9),
        '150': (3.1, 2.2),
        '225': (3.1, 2.6),
        '300': (3.1, 2.9),
        '500': (4.3, 4),
        '750': (5.7, 4.9),
        '1000': (5.7, 5.5),
        '1500': (5.7, 6.5),
        '2000': (5.7, 7.3),
        '2500': (5.7, 7.9)
    }

    def __init__(self, trans_conn, trans_sec_voltage, percent_ztrans, transformer_kva, x_r_trans):
        self.trans_sec_voltage = trans_sec_voltage
        self.trans_conn = trans_conn
        self.percent_ztrans = percent_ztrans
        self.percent_ztrans_pu = percent_ztrans / 100
        self.transformer_kva = transformer_kva
        self.transformer_mva = transformer_kva / 1000
        self.x_r_trans = x_r_trans
        theta_rads = math.atan(self.x_r_trans)
        self.theta_degs = math.degrees(theta_rads)
        self.Z_pos_trans = complex(self.percent_ztrans * (100 / self.transformer_mva) * math.cos(theta_rads), self.percent_ztrans * (100 / self.transformer_mva) * math.sin(theta_rads))
        self.Zo_trans = self.Z_pos_trans

    def display_info(self):
        print(f"\nKVA: {self.transformer_kva}")
        print(f"Z: {self.x_r_trans}%")
        print(f"Connection: {self.trans_conn}")
        print(f"Secondary Voltage: {self.trans_sec_voltage}")

    @staticmethod
    def select_connection_type():
        connection_types = {
            '1': 'Δ-Yg',
            '2': 'Yg-Yg',
            '3': 'Δ-Δ',
            '4': 'Y-Y'
        }
        print("Select the transformer connection type:")
        for key, value in connection_types.items():
            print(f"{key}. {value}")
        choice = input("Enter (1-4): ")
        return connection_types.get(choice, None)

    @classmethod
    def from_predefined(cls):
        print("Select a predefined transformer by its kVA rating:")
        for rating in cls.predefined_transformers:
            print(f"{rating} kVA")
        kva_choice = input("Enter the kVA rating of the transformer: ")
        if kva_choice in cls.predefined_transformers:
            percent_ztrans, x_r_trans = cls.predefined_transformers[kva_choice]
            trans_conn = cls.select_connection_type()
            if trans_conn is None:
                print("Invalid connection type selected.")
                return None
            trans_sec_voltage = float(input("Enter transformer secondary voltage (in kV): "))
            return cls(trans_conn, trans_sec_voltage, percent_ztrans, float(kva_choice), x_r_trans)
        else:
            print("Invalid choice.")
            return None

    @staticmethod
    def get_custom_transformer():
        trans_conn = ZTrans.select_connection_type()
        if trans_conn is None:
            print("Invalid connection type selected.")
            return None
        trans_sec_voltage = float(input("Enter transformer secondary voltage (in kV): "))
        percent_ztrans = float(input("Enter percent impedance (Z%): "))
        transformer_kva = float(input("Enter transformer kVA rating: "))
        x_r_trans = float(input("Enter transformer X/R ratio: "))
        return ZTrans(trans_conn, trans_sec_voltage, percent_ztrans, transformer_kva, x_r_trans)

    @staticmethod
    def menu():
        while True:
            print("\nLoad a transformer:")
            print("1. Select a predefined transformer")
            print("2. Enter a custom transformer")
            print("3. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                transformer = ZTrans.from_predefined()
                if transformer:
                    return transformer
            elif choice == '2':
                return ZTrans.get_custom_transformer()
            elif choice == '3':
                print("Exiting...")
                break
            else:
                print("Invalid choice, please try again.")

'''
def main():
    Ztrans_test = ZTrans
    Ztrans_test = Ztrans_test.menu()

    
    print(f"{Ztrans_test.transformer_kva:.0f}")
    print(f"{Ztrans_test.transformer_mva:.3f}")
    print(f"{Ztrans_test.Z_pos_trans:.5f} {Ztrans_test.Zo_trans:.5f}")

if __name__ == '__main__':

'''