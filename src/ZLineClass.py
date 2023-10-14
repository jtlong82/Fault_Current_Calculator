from cmath import rect, phase
import numpy as np

def parse_complex(complex_str):
    # Helper function to parse the complex impedance strings like "0.61+4.52j" into complex numbers
    return complex(*map(float, complex_str.replace('j', '').split('+')))


class ZLineClass:
    def __init__(self, line_trace, impedance_sheet):
        self.line_trace = line_trace
        self.impedance_sheet = impedance_sheet
        self.voltage_class = self.get_voltage_class()
        self.filtered_attributes = self.filter_attributes_by_voltage()
        self.special_inputs = {}
        self.mapped_impedances = None
        self.total_impedance = None

    def get_voltage_class(self):
        circuit = self.line_trace[4].iloc[1]
        first_char = circuit[0]
        voltage_mapping = {'R': '36', 'L': '13.2', 'V': '11.5', 'H': '4.6'}
        return voltage_mapping.get(first_char, 'Unknown')

    def filter_attributes_by_voltage(self):
        return self.impedance_sheet[self.impedance_sheet['Voltage_Level'] == self.voltage_class]

    def get_36kV_inputs(self):
        pole_options = ['Wood', 'Steel']
        ground_options = ['With Ground', 'Without Ground']
        
        print("Select the type of pole:")
        for i, option in enumerate(pole_options):
            print(f"{i+1}. {option}")
        selected = int(input("Your choice: ")) - 1
        self.special_inputs["wood_or_steel"] = pole_options[selected]
        
        print("Select the ground option:")
        for i, option in enumerate(ground_options):
            print(f"{i+1}. {option}")
        selected = int(input("Your choice: ")) - 1
        self.special_inputs["with_or_without_ground"] = ground_options[selected]

    def get_11_5kV_reactor(self):
        reactor_options = ['600MCM Cu (400A)', '2-600 MCM Cu (800A)', '4/0 Cu (200A)', 'HL']
        
        print("Select the reactor type:")
        for i, option in enumerate(reactor_options):
            print(f"{i+1}. {option}")
        selected = int(input("Your choice: ")) - 1
        self.special_inputs["reactor"] = reactor_options[selected]

    def map_line_trace_to_impedance(self):
        self.mapped_impedances = []
        for _, row in self.line_trace.iterrows():
            # Match based on Conductor Size and Conductor Type
            matched_row = self.filtered_attributes[
                (self.filtered_attributes['Conductor Size'] == row['Conductor Size']) &
                (self.filtered_attributes['Conductor Type'] == row['Conductor Type'])
            ]
        
            if matched_row.empty:
                print(f"No exact match found for Conductor Size: {row['Conductor Size']}, Conductor Type: {row['Conductor Type']}")
                print("Please select the closest match:")
                # Only list the options relevant to the current voltage class
                for i, option in enumerate(self.filtered_attributes.itertuples()):
                    print(f"{i+1}. {option}")
                selected = int(input("Your choice: ")) - 1
                matched_row = self.filtered_attributes.iloc[selected]
            
            if self.voltage_class == '36':
                # Further refine match based on pole type and grounding
                matched_row = matched_row[
                    matched_row['Pole Type'] == self.special_inputs["wood_or_steel"] &
                    matched_row['Grounding'] == self.special_inputs["with_or_without_ground"]
                ]
                
            elif self.voltage_class == '11.5' and row['Type'] == 'Reactor':
                # If it's a reactor, match based on reactor type
                matched_row = matched_row[matched_row['Reactor Type'] == self.special_inputs["reactor"]]
                
            self.mapped_impedances.append(parse_complex(matched_row['Impedance'].values[0]))
    
    def calculate_total_impedance(self):
        self.total_impedance = np.sum(np.array(self.mapped_impedances) * self.line_trace['Length'].values)

    def run(self):
        if self.voltage_class == '36':
            self.get_36kV_inputs()
        elif self.voltage_class == '11.5':
            self.get_11_5kV_reactor()
        
        self.map_line_trace_to_impedance()
        self.calculate_total_impedance()
