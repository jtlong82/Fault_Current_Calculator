import pandas as pd
import cmath
import math

class ZLine:
    def __init__(self, line_trace):
        self.type = str(line_trace.iloc['Type'])
        self.conductor_size = str(line_trace.iloc['Conductor Size'])
        self.conductor_type = str(line_trace.iloc['Conductor Type'])
        self.length = float(line_trace.iloc['Length'])
        self.voltage_level = float(line_trace.iloc['Voltage_Level'])
        self.z_100MVA = complex(line_trace.iloc['% Z+ @ 100 MVA'])
        if self.voltage_level != 4.6:
            self.zo_100MVA = complex(line_trace.iloc['% Zo @ 100 MVA'])
        self.mapped_conductor_type = str(line_trace.iloc['Mapped Wire Type'])
        if self.voltage_level == 36 & self.type == 'OH Pri. Conductor':
            self.pole_type = str(line_trace.iloc['Pole Type'])
            self.ground = str(line_trace.iloc['Ground?'])

   

