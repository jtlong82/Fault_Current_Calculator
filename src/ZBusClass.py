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