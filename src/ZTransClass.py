import pandas as pd
import cmath
import math
import numpy as np

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