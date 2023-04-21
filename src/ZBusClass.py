import pandas as pd

class ZBus:
    def __init__(self, selected_record):
        self.station = str(selected_record.iloc[0])
        self.supplied_from = str(selected_record.iloc[1])
        self.transformer_kva = str(selected_record.iloc[2])
        self.tap_ratio = str(selected_record.iloc[3])
        self.z_100MVA = complex(selected_record.iloc[4])
        self.d_e_120V = float(selected_record.iloc[5])
        self.short_circuit_MVA_1 = float(selected_record.iloc[6])
        self.zo_100MVA = complex(selected_record.iloc[7])
        self.z_L_G_100MVA = complex(selected_record.iloc[8])
        self.short_circuit_MVA_2 = float(selected_record.iloc[9])

    def display_info(self):
        print(f"Station: {self.station}")
        print(f"Supplied from (System): {self.supplied_from}")
        print(f"Transformer No. - kVA: {self.transformer_kva}")
        print(f"Tap Ratio: {self.tap_ratio}")
        print(f"% Z @ 100MVA: {self.z_100MVA}")
        print(f"D e @ 120 V: {self.d_e_120V}")
        print(f"Short Circuit MVA (1): {self.short_circuit_MVA_1}")
        print(f"% Zo @ 100MVA: {self.zo_100MVA}")
        print(f"% Z (L_G) @ 100MVA: {self.z_L_G_100MVA}")
        print(f"Short Circuit MVA (2): {self.short_circuit_MVA_2}")