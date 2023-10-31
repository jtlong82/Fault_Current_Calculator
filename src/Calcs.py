import cmath
import math
from ZBusClass import ZBus
from ZLineClass import ZLine
import numpy as np
import matplotlib.pyplot as plt

def primary_line_fault_calculation(ZBus_obj, Zline_obj):
    MVA_base = ZBus_obj.MVA_base
    Zbase = ZBus_obj.Zbase 
    Ibase = ZBus_obj.Ibase
    voltage_level = ZBus_obj.voltage_level
    voltage_level_pu = ZBus_obj.voltage_level_pu
    Zpos_pu = (ZBus_obj.z_100MVA / 100) + (Zline_obj.total_Z_100MVA / 100)
    Zo_pu = (ZBus_obj.zo_100MVA / 100) + (Zline_obj.total_Zo_100MVA /100)

    X_R_pos = Zpos_pu.imag  / Zpos_pu.real

    #3-ph fault
    three_ph_fault_pu = voltage_level_pu / (Zpos_pu)
    three_ph_fault_pu_mag = abs(three_ph_fault_pu)
    three_ph_fault_pu_ang_rads = cmath.phase(three_ph_fault_pu)
    three_ph_fault_pu_ang_degs = math.degrees(three_ph_fault_pu_ang_rads)
    three_ph_fault = (three_ph_fault_pu_mag * Ibase * 1000)
    #Individual phases 3-ph fault
    three_ph_fault_Aph = three_ph_fault
    three_ph_fault_pu_ang_degs_Aph = three_ph_fault_pu_ang_degs
    three_ph_fault_Bph = three_ph_fault
    three_ph_fault_pu_ang_degs_Bph = three_ph_fault_pu_ang_degs + 120
    three_ph_fault_Cph = three_ph_fault
    three_ph_fault_pu_ang_degs_Cph = three_ph_fault_pu_ang_degs - 120


    #line-to-line fault
    l_l_fault_pos = voltage_level_pu / (Zpos_pu * 2) #Ia sequence
    l_l_fault_pu = (-1j) * (3 ** 0.5) * l_l_fault_pos #Ib fault current pu
    l_l_fault_pu_mag = abs(l_l_fault_pu)
    l_l_fault_pu_ang_rads = cmath.phase(l_l_fault_pu)
    l_l_fault_pu_ang_degs = math.degrees(l_l_fault_pu_ang_rads)
    l_l_fault = l_l_fault_pu_mag * Ibase * 1000
    #Individual phases line-to-line fault
    l_l_fault_Bph = l_l_fault
    l_l_fault_pu_ang_degs_Bph = l_l_fault_pu_ang_degs
    l_l_fault_Cph = l_l_fault
    l_l_fault_pu_ang_degs_Cph = l_l_fault_pu_ang_degs + 180

    if voltage_level != 4.6:
        # line to ground fault
        X_R_zero = (2 * Zpos_pu.imag + Zo_pu.imag) / (2 * Zpos_pu.real + Zo_pu.real) 
        l_g_fault_pu = 2 * (Zpos_pu) + (Zo_pu)
        l_g_fault_pu = ((l_g_fault_pu.conjugate()) / ((l_g_fault_pu.real) ** 2 + (l_g_fault_pu.imag) ** 2))
        l_g_fault_pu_mag = abs(l_g_fault_pu)
        l_g_fault_pu_ang_rads = cmath.phase(l_g_fault_pu)
        l_g_fault_pu_ang_degs = math.degrees(l_g_fault_pu_ang_rads)
        l_g_fault = 3 * l_g_fault_pu_mag * Ibase * 1000

        # Calculating the line-to-line-to-ground fault current as soon as the object is initiated
        l_l_g_fault_Z2_pu = Zpos_pu
        #print(f"Z2 pu: {l_l_g_fault_Z2_pu}")
        l_l_g_fault_Zf_pu = (l_l_g_fault_Z2_pu * Zo_pu) / (Zo_pu + l_l_g_fault_Z2_pu)
        #print(f"Zf pu: {l_l_g_fault_Zf_pu}")
        l_l_g_fault_pos_pu = voltage_level_pu / (Zpos_pu + l_l_g_fault_Zf_pu) #I1 positive sequence
        #print(f"I1 pu: {l_l_g_fault_pos_pu}")
        l_l_g_fault_neg_pu = -l_l_g_fault_pos_pu * (Zo_pu / (Zo_pu + l_l_g_fault_Z2_pu)) #I2 negative sequence
        #print(f"I2 pu: {l_l_g_fault_neg_pu}")
        l_l_g_fault_zero_pu = -l_l_g_fault_pos_pu * (l_l_g_fault_Z2_pu / (Zo_pu + l_l_g_fault_Z2_pu)) #I0 zero sequence
        #print(f"I0 pu: {l_l_g_fault_zero_pu}")
        A = np.array([[1, 1, 1],[1, -0.5 - 0.866j, -0.5 + 0.866j],[1, -0.5 + 0.866j, -0.5 - 0.866j]]) #A matrix
        #print(f"A matrix: {A}")
        I_seq = np.array([l_l_g_fault_zero_pu, l_l_g_fault_pos_pu, l_l_g_fault_neg_pu]) #Sequence currents matrix
        #print(f"Sequence Matrix: {I_seq}")
        I_phase = np.dot(A, I_seq)
        #print(f"Phase Matrix: {I_phase}")
        l_l_g_fault_Aph_pu, l_l_g_fault_Bph_pu, l_l_g_fault_Cph_pu = I_phase #Individual phases line-to-line-to Ground fault
        l_l_g_fault_Bph = abs(l_l_g_fault_Bph_pu) * Ibase * 1000
        l_l_g_fault_pu_ang_rads_Bph = cmath.phase(l_l_g_fault_Bph_pu)
        l_l_g_fault_pu_ang_degs_Bph = math.degrees(l_l_g_fault_pu_ang_rads_Bph)
        l_l_g_fault_Cph = abs(l_l_g_fault_Cph_pu) * Ibase * 1000
        l_l_g_fault_pu_ang_rads_Cph = cmath.phase(l_l_g_fault_Cph_pu)
        l_l_g_fault_pu_ang_degs_Cph = math.degrees(l_l_g_fault_pu_ang_rads_Cph)

    print(f"X/R Positive Seq at line trace: {X_R_pos:.2f}")
    if voltage_level != 4.6:
        print(f"X/R Zero Seq at line trace: {X_R_zero:.2f}")
    print("\nAvailable fault currents at line trace: ")
    print(f"ABC: {three_ph_fault:.0f}∠{three_ph_fault_pu_ang_degs:.2f}° Amps")
    if voltage_level != 4.6:
        print(f"AG: {l_g_fault:.0f}∠{l_g_fault_pu_ang_degs:.2f}° Amps")
    print(f"BC: {l_l_fault:.0f}∠{l_l_fault_pu_ang_degs:.2f}° Amps")
    if voltage_level != 4.6:
        print(f"BCG: {l_l_g_fault_Bph:.0f}∠{l_l_g_fault_pu_ang_degs_Bph :.2f}° Amps")

    print(f"\nABC:")
    print(f"A: {three_ph_fault_Aph:.0f}∠{three_ph_fault_pu_ang_degs_Aph:.2f}° Amps    B: {three_ph_fault_Bph:.0f}∠{three_ph_fault_pu_ang_degs_Bph:.2f}° Amps    C: {three_ph_fault_Cph:.0f}∠{three_ph_fault_pu_ang_degs_Cph:.2f}° Amps")
    if voltage_level != 4.6:
        print(f"AG:")
        print(f"A: {l_g_fault:.0f}∠{l_g_fault_pu_ang_degs:.2f}° Amps    B: {0:.0f}∠{0:.2f}° Amps    C: {0:.0f}∠{0:.2f}° Amps")
    print(f"BC:")
    print(f"A: {0:.0f}∠{0:.2f}° Amps    B: {l_l_fault_Bph:.0f}∠{l_l_fault_pu_ang_degs_Bph:.2f}° Amps    C: {l_l_fault_Cph:.0f}∠{l_l_fault_pu_ang_degs_Cph:.2f}° Amps")
    if voltage_level != 4.6:
        print(f"BCG:")
        print(f"A: {0:.0f}∠{0:.2f}° Amps    B: {l_l_g_fault_Bph:.0f}∠{l_l_g_fault_pu_ang_degs_Bph:.2f}° Amps    C: {l_l_g_fault_Cph:.0f}∠{l_l_g_fault_pu_ang_degs_Cph:.2f}° Amps")

    return

def locate_primary_line_fault_l_g(ZBus_obj, Zline_obj):
    #MVA_base = ZBus_obj.MVA_base
    #Zbase = ZBus_obj.Zbase 
    Ibase = ZBus_obj.Ibase
    #voltage_level = ZBus_obj.voltage_level
    #voltage_level_pu = ZBus_obj.voltage_level_pu
    #line_length_ft = Zline_obj.total_length_feet
    line_length_mi = Zline_obj.total_length_miles
    Zpos_line_pu = Zline_obj.total_Z_100MVA / 100
    Zo_line_pu = Zline_obj.total_Zo_100MVA /100
    Zpos_bus_pu = ZBus_obj.z_100MVA / 100
    Zo_bus_pu = ZBus_obj.zo_100MVA /100
    #Zpos_lol_pu = (ZBus_obj.z_100MVA / 100) + (Zline_obj.total_Z_100MVA / 100) #Z1 in pu for length of given length of line trace + bus impedance in pu 
    #Zo_lol_pu = (ZBus_obj.zo_100MVA / 100) + (Zline_obj.total_Zo_100MVA /100) #Z0 in pu for length of given length of line trace + bus impedance in pu
    measured_fault_current = 1102

    #calculate the line impedance per unit length
    Zpos_line_per_mile = Zpos_line_pu / line_length_mi
    Zo_line_per_mile = Zo_line_pu / line_length_mi

    # Initialize distance array and fault current array
    distance = np.linspace(0, line_length_mi, 1000)
    calc_fault_current = np.zeros(distance.shape, dtype=complex)

    for i, d in enumerate(distance):
        # Calculate the total impedance for the line-to-ground fault
        Zpos_total_pu = Zpos_bus_pu + d * Zpos_line_per_mile
        Zo_total_pu = Zo_bus_pu + d * Zo_line_per_mile

        # Calculating the line to ground fault current
        l_g_fault_pu = 2 * Zpos_total_pu + Zo_total_pu
        l_g_fault_pu = ((l_g_fault_pu.conjugate()) / ((l_g_fault_pu.real) ** 2 + (l_g_fault_pu.imag) ** 2))
        l_g_fault_pu_mag = abs(l_g_fault_pu)
        l_g_fault_pu_ang_rads = cmath.phase(l_g_fault_pu)
        l_g_fault_pu_ang_degs = math.degrees(l_g_fault_pu_ang_rads)
        l_g_fault = 3 * l_g_fault_pu_mag * Ibase * 1000

        calc_fault_current[i] = l_g_fault

    # Find the index where the calculated fault current is closest to the given fault current
    closest_idx = np.argmin(np.abs(np.abs(calc_fault_current) - measured_fault_current))
    closest_distance = distance[closest_idx]

    # Plot the fault current
    plt.figure(figsize=(10, 6))
    plt.plot(distance, calc_fault_current, label='Calculated Current Amps')
    plt.axhline(measured_fault_current, color='r', linestyle='--', label=f'Measured fault current = {measured_fault_current:.0f} Amps')
    plt.xlabel('Distance (miles)')
    plt.ylabel('Fault Current (Amps)')
    plt.title('Fault Current vs. Distance')

    # Annotate the point of intersection
    plt.annotate(f'Intersection\n({closest_distance:.2f} miles, {measured_fault_current:.0f} Amps)', 
                 xy=(closest_distance, measured_fault_current), 
                xytext=(closest_distance + 0.5, measured_fault_current + 200), 
                arrowprops=dict(arrowstyle='->'),
                fontsize=9)

    plt.legend()
    plt.grid(True)
    plt.show()

    return closest_distance, np.abs(calc_fault_current[closest_idx])
        



    