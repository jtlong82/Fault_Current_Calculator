import cmath
import math
import numpy as np
import matplotlib.pyplot as plt

def primary_line_fault_calculation(ZBus_obj, Zline_obj, buffer):
    MVA_base = ZBus_obj.MVA_base
    Zbase = ZBus_obj.Zbase 
    Ibase = ZBus_obj.Ibase
    voltage_level = ZBus_obj.voltage_level
    voltage_level_pu = ZBus_obj.voltage_level_pu

    #Getting Zline in pri. ohms
    Z_pos_line_pohms_mag = abs(Zline_obj.total_Z_100MVA_pu) * Zbase
    Z_pos_angle_rads = cmath.phase(Zline_obj.total_Z_100MVA_pu)
    Z_pos_angle_degs = math.degrees(Z_pos_angle_rads)
    Zo_line_pohms_mag = abs(Zline_obj.total_Zo_100MVA_pu) * Zbase
    Zo_angle_rads = cmath.phase(Zline_obj.total_Zo_100MVA_pu)
    Zo_angle_degs = math.degrees(Zo_angle_rads)

    #Getting Zline in sec. ohms
    Z_pos_line_sohms_mag = Z_pos_line_pohms_mag * (Zline_obj.ctr/Zline_obj.ptr)
    Zo_line_sohms_mag = Zo_line_pohms_mag * (Zline_obj.ctr/Zline_obj.ptr)

    #Getting line Z%
    Zpos_per_mag = abs(Zline_obj.total_Z_100MVA)
    Zo_per_mag = abs(Zline_obj.total_Zo_100MVA)

    #Getting total Zpu
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
    
    #Print to buffer
    buffer.append(f"\nLine Impedance: \n")
    buffer.append(f"Z+: {Z_pos_line_pohms_mag:.2f}∠{Z_pos_angle_degs:.2f}° Pri. Ohms,    {Z_pos_line_sohms_mag:.2f}∠{Z_pos_angle_degs:.2f}° Sec. Ohms,    {Zpos_per_mag:.2f}∠{Z_pos_angle_degs:.2f}° %\n")
    if voltage_level != 4.6:
        buffer.append(f"Z0: {Zo_line_pohms_mag:.2f}∠{Zo_angle_degs:.2f}° Pri. Ohms,    {Zo_line_sohms_mag:.2f}∠{Zo_angle_degs:.2f}° Sec. Ohms,    {Zo_per_mag:.2f}∠{Zo_angle_degs:.2f}° %\n")
    buffer.append(f"\nX/R Positive Seq: {X_R_pos:.2f}\n")
    if voltage_level != 4.6:
        buffer.append(f"X/R Zero Seq: {X_R_zero:.2f}\n")
    
    #Print faults to buffer in alignment
    line_format = "{:<4} {:>15} {:>4} {:>15} {:>4} {:>15} {:>4} {:>15}"
    buffer.append(f"\nAvailable fault currents at {Zline_obj.label}: \n")

    #Print formatted abc fault to buffer
    abc_fault = f"{three_ph_fault:.0f}∠{three_ph_fault_pu_ang_degs:.2f}°A"
    a_phase_fault = f"{three_ph_fault_Aph:.0f}∠{three_ph_fault_pu_ang_degs_Aph:.2f}°A"
    b_phase_fault = f"{three_ph_fault_Bph:.0f}∠{three_ph_fault_pu_ang_degs_Bph:.2f}°A"
    c_phase_fault = f"{three_ph_fault_Cph:.0f}∠{three_ph_fault_pu_ang_degs_Cph:.2f}°A"
    output_line = line_format.format("ABC:", abc_fault, "A:", a_phase_fault, "B:", b_phase_fault, "C:", c_phase_fault)
    buffer.append(output_line + "\n")
    
    #Print formatted AG fault to buffer
    if voltage_level != 4.6:
        ag_fault = f"{l_g_fault:.0f}∠{l_g_fault_pu_ang_degs:.2f}°A"
        a_phase_fault = f"{l_g_fault:.0f}∠{l_g_fault_pu_ang_degs:.2f}°A"
        b_phase_fault = f"{0:.0f}∠{0:.2f}°A"
        c_phase_fault = f"{0:.0f}∠{0:.2f}°A"
        output_line = line_format.format("AG:", ag_fault, "A:", a_phase_fault, "B:", b_phase_fault, "C:", c_phase_fault)
        buffer.append(output_line + "\n")
        
    #Print formatted BC fault to buffer
    bc_fault = f"{l_l_fault:.0f}∠{l_l_fault_pu_ang_degs:.2f}°A"
    a_phase_fault = f"{0:.0f}∠{0:.2f}°A"
    b_phase_fault = f"{l_l_fault_Bph:.0f}∠{l_l_fault_pu_ang_degs_Bph:.2f}°A"
    c_phase_fault = f"{l_l_fault_Cph:.0f}∠{l_l_fault_pu_ang_degs_Cph:.2f}°A"
    output_line = line_format.format("BC:", bc_fault, "A:", a_phase_fault, "B:", b_phase_fault, "C:", c_phase_fault)
    buffer.append(output_line + "\n")    
    
    #Print formatted BCG fault to buffer
    if voltage_level != 4.6:
        bcg_fault = f"{l_l_g_fault_Bph:.0f}∠{l_l_g_fault_pu_ang_degs_Bph:.2f}°A"
        a_phase_fault = f"{0:.0f}∠{0:.2f}°A"
        b_phase_fault = f"{l_l_g_fault_Bph:.0f}∠{l_l_g_fault_pu_ang_degs_Bph:.2f}°A"
        c_phase_fault = f"{l_l_g_fault_Cph:.0f}∠{l_l_g_fault_pu_ang_degs_Cph:.2f}°A"
        output_line = line_format.format("BCG:", bcg_fault, "A:", a_phase_fault, "B:", b_phase_fault, "C:", c_phase_fault)
        buffer.append(output_line + "\n") 
        
    return

def sec_trans_fault_calculation(ZBus_obj, Zline_obj, Ztrans_obj, buffer):
    MVA_base = ZBus_obj.MVA_base 
    Zbase = ZBus_obj.Zbase
    voltage_level = ZBus_obj.voltage_level
    voltage_level_pu = ZBus_obj.voltage_level_pu
    Ibase = MVA_base / (Ztrans_obj.trans_sec_voltage * (3 ** 0.5))

    #Getting total Z of bus, line and TR
    Zpos_pu = (ZBus_obj.z_100MVA / 100) + (Zline_obj.total_Z_100MVA / 100) + (Ztrans_obj.Z_pos_trans / 100)

    if Ztrans_obj.trans_conn == 'Δ-Yg': 
        Zo_pu = 2 * ((ZBus_obj.z_100MVA / 100) + (Zline_obj.total_Z_100MVA / 100)) + (3 * (Ztrans_obj.Z_pos_trans / 100))
    elif Ztrans_obj.trans_conn == 'Yg-Yg': 
        Zo_pu = 2 * ((ZBus_obj.z_100MVA / 100) + (Zline_obj.total_Z_100MVA / 100)) + (ZBus_obj.zo_100MVA / 100) + (Zline_obj.total_Zo_100MVA / 100) + (3 * (Ztrans_obj.Z_pos_trans / 100))
    else:
        Zo_pu = 0 + 0j

    X_R_pos = Zpos_pu.imag  / Zpos_pu.real

    #Getting total Z of line and TR for distance relaying and calculating impedances
    Zpos_lt_pu = (Zline_obj.total_Z_100MVA / 100) + (Ztrans_obj.Z_pos_trans / 100)

    if Ztrans_obj.trans_conn == 'Δ-Yg': 
        Zo_lt_pu = 2 * (Zline_obj.total_Z_100MVA / 100) + (3 * (Ztrans_obj.Z_pos_trans / 100))
    elif Ztrans_obj.trans_conn == 'Yg-Yg': 
        Zo_lt_pu = 2 * (Zline_obj.total_Z_100MVA / 100) + (Zline_obj.total_Zo_100MVA / 100) + (3 * (Ztrans_obj.Z_pos_trans / 100))
    else:
        Zo_lt_pu = 0 + 0j

    if Ztrans_obj.trans_conn == 'Δ-Yg': 
        Zo_lt_pu = 2 * (Zline_obj.total_Z_100MVA / 100) + (3 * (Ztrans_obj.Z_pos_trans / 100))
    elif Ztrans_obj.trans_conn == 'Yg-Yg': 
        Zo_lt_pu = 2 * (Zline_obj.total_Z_100MVA / 100) + (Zline_obj.total_Zo_100MVA / 100) + (3 * (Ztrans_obj.Z_pos_trans / 100))
    else:
        Zo_lt_pu = 0 + 0j

    #In pri. ohms
    Zpos_lt_pohms_mag = abs(Zpos_lt_pu) * Zbase
    Zpos_lt_angle_rads = cmath.phase(Zpos_lt_pu)
    Zpos_lt_angle_degs = math.degrees(Zpos_lt_angle_rads)
    Zo_lt_pohms_mag = abs(Zo_lt_pu) * Zbase
    Zo_lt_angle_rads = cmath.phase(Zo_lt_pu)
    Zo_lt_angle_degs = math.degrees(Zo_lt_angle_rads)

    #In sec. ohms
    Zpos_lt_sohms_mag = Zpos_lt_pohms_mag * (Zline_obj.ctr/Zline_obj.ptr)
    Zo_lt_sohms_mag = Zo_lt_pohms_mag * (Zline_obj.ctr/Zline_obj.ptr)

    #3-ph fault
    three_ph_fault_pu = voltage_level_pu / (Zpos_pu)
    three_ph_fault_pu_mag = abs(three_ph_fault_pu)
    three_ph_fault_pu_ang_rads = cmath.phase(three_ph_fault_pu)
    three_ph_fault_pu_ang_degs = math.degrees(three_ph_fault_pu_ang_rads)
    three_ph_fault = (three_ph_fault_pu_mag * Ibase * 1000)
    three_ph_fault_pri_side = three_ph_fault * (Ztrans_obj.trans_sec_voltage/ZBus_obj.voltage_level)
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
    l_l_fault_pri_side = l_l_fault * (Ztrans_obj.trans_sec_voltage/ZBus_obj.voltage_level)
    #Individual phases line-to-line fault
    l_l_fault_Bph = l_l_fault
    l_l_fault_pu_ang_degs_Bph = l_l_fault_pu_ang_degs
    l_l_fault_Cph = l_l_fault
    l_l_fault_pu_ang_degs_Cph = l_l_fault_pu_ang_degs + 180

    if Ztrans_obj.trans_conn == 'Δ-Yg' or Ztrans_obj.trans_conn == 'Yg-Yg':
        # line to ground fault
        X_R_zero = Zo_pu.imag / Zo_pu.real
        l_g_fault_pu = Zo_pu
        l_g_fault_pu = ((l_g_fault_pu.conjugate()) / ((l_g_fault_pu.real) ** 2 + (l_g_fault_pu.imag) ** 2))
        l_g_fault_pu_mag = abs(l_g_fault_pu)
        l_g_fault_pu_ang_rads = cmath.phase(l_g_fault_pu)
        l_g_fault_pu_ang_degs = math.degrees(l_g_fault_pu_ang_rads)
        l_g_fault = 3 * l_g_fault_pu_mag * Ibase * 1000
        if Ztrans_obj.trans_conn == 'Δ-Yg':
            l_g_fault_pri_side = l_g_fault * (Ztrans_obj.trans_sec_voltage/ZBus_obj.voltage_level) / (3 ** 0.5)
        else:
            l_g_fault_pri_side = l_g_fault * (Ztrans_obj.trans_sec_voltage/ZBus_obj.voltage_level)

        # Calculating the line-to-line-to-ground fault current
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
        l_l_g_fault_pri_side = l_l_g_fault_Bph * (Ztrans_obj.trans_sec_voltage/ZBus_obj.voltage_level)
    
    #Print to buffer
    buffer.append(f"\nLine + Transformer Impedances (used for distance calculations): \n")
    buffer.append(f"+Z: {Zpos_lt_pohms_mag:.2f}∠{Zpos_lt_angle_degs:.2f}° Pri. Ohms,   +Z: {Zpos_lt_sohms_mag:.2f}∠{Zpos_lt_angle_degs:.2f}° Sec. Ohms\n")
    if voltage_level != 4.6:
        buffer.append(f"Z0: {Zo_lt_pohms_mag:.2f}∠{Zo_lt_angle_degs:.2f}° Pri. Ohms,   +Z: {Zo_lt_sohms_mag:.2f}∠{Zo_lt_angle_degs:.2f}° Sec. Ohms\n")

    buffer.append(f"\nBus + Line + Transformer Impedances (p.u.): \n")
    buffer.append(f"+Z: {Zpos_pu:.3f} \n")
    buffer.append(f"Z0: {Zo_pu:.3f} \n")

    buffer.append(f"\nX/R Positive Seq at secondary of transformer: {X_R_pos:.2f}\n")
    if Ztrans_obj.trans_conn == 'Δ-Yg' or Ztrans_obj.trans_conn == 'Yg-Yg':
        buffer.append(f"X/R Zero Seq on secondary of transformer: {X_R_zero:.2f}\n")
    #Print faults to buffer in alignment
    line_format = "{:<4} {:>15} {:>4} {:>15} {:>4} {:>15} {:>4} {:>15}"
    buffer.append(f"\nAvailable fault currents at secondary of transformer: \n")

    #Print formatted abc fault to buffer
    abc_fault = f"{three_ph_fault:.0f}∠{three_ph_fault_pu_ang_degs:.2f}°A"
    a_phase_fault = f"{three_ph_fault_Aph:.0f}∠{three_ph_fault_pu_ang_degs_Aph:.2f}°A"
    b_phase_fault = f"{three_ph_fault_Bph:.0f}∠{three_ph_fault_pu_ang_degs_Bph:.2f}°A"
    c_phase_fault = f"{three_ph_fault_Cph:.0f}∠{three_ph_fault_pu_ang_degs_Cph:.2f}°A"
    output_line = line_format.format("ABC:", abc_fault, "A:", a_phase_fault, "B:", b_phase_fault, "C:", c_phase_fault)
    buffer.append(output_line + "\n")
    
    #Print formatted AG fault to buffer
    if Ztrans_obj.trans_conn == 'Δ-Yg' or Ztrans_obj.trans_conn == 'Yg-Yg':
        ag_fault = f"{l_g_fault:.0f}∠{l_g_fault_pu_ang_degs:.2f}°A"
        a_phase_fault = f"{l_g_fault:.0f}∠{l_g_fault_pu_ang_degs:.2f}°A"
        b_phase_fault = f"{0:.0f}∠{0:.2f}°A"
        c_phase_fault = f"{0:.0f}∠{0:.2f}°A"
        output_line = line_format.format("AG:", ag_fault, "A:", a_phase_fault, "B:", b_phase_fault, "C:", c_phase_fault)
        buffer.append(output_line + "\n")
        
    #Print formatted BC fault to buffer
    bc_fault = f"{l_l_fault:.0f}∠{l_l_fault_pu_ang_degs:.2f}°A"
    a_phase_fault = f"{0:.0f}∠{0:.2f}°A"
    b_phase_fault = f"{l_l_fault_Bph:.0f}∠{l_l_fault_pu_ang_degs_Bph:.2f}°A"
    c_phase_fault = f"{l_l_fault_Cph:.0f}∠{l_l_fault_pu_ang_degs_Cph:.2f}°A"
    output_line = line_format.format("BC:", bc_fault, "A:", a_phase_fault, "B:", b_phase_fault, "C:", c_phase_fault)
    buffer.append(output_line + "\n")    
    
    #Print formatted BCG fault to buffer
    if Ztrans_obj.trans_conn == 'Δ-Yg' or Ztrans_obj.trans_conn == 'Yg-Yg':
        bcg_fault = f"{l_l_g_fault_Bph:.0f}∠{l_l_g_fault_pu_ang_degs_Bph:.2f}°A"
        a_phase_fault = f"{0:.0f}∠{0:.2f}°A"
        b_phase_fault = f"{l_l_g_fault_Bph:.0f}∠{l_l_g_fault_pu_ang_degs_Bph:.2f}°A"
        c_phase_fault = f"{l_l_g_fault_Cph:.0f}∠{l_l_g_fault_pu_ang_degs_Cph:.2f}°A"
        output_line = line_format.format("BCG:", bcg_fault, "A:", a_phase_fault, "B:", b_phase_fault, "C:", c_phase_fault)
        buffer.append(output_line + "\n")

    buffer.append(f"\nTR Secondary fault magnitudes as seen by transformer high side: \n")
    buffer.append(f"ABC: {three_ph_fault_pri_side:.0f}A\n")
    if Ztrans_obj.trans_conn == 'Δ-Yg' or Ztrans_obj.trans_conn == 'Yg-Yg':
        buffer.append(f"AG: {l_g_fault_pri_side:.0f}A\n")
    buffer.append(f"BC: {l_l_fault_pri_side:.0f}A\n")
    if Ztrans_obj.trans_conn == 'Δ-Yg' or Ztrans_obj.trans_conn == 'Yg-Yg':
        buffer.append(f"BCG: {l_l_g_fault_pri_side:.0f}A\n")

    return
    
def locate_primary_line_fault_l_g(ZBus_obj, Zline_obj, measured_mag):
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
    closest_idx = np.argmin(np.abs(np.abs(calc_fault_current) - measured_mag))
    closest_distance = distance[closest_idx]

    # Plot the fault current
    plt.figure(figsize=(10, 6))
    plt.plot(distance, calc_fault_current, label='Calculated Current Amps')
    plt.axhline(measured_mag, color='r', linestyle='--', label=f'Measured fault current = {measured_mag:.0f} Amps')
    plt.xlabel('Distance (miles)')
    plt.ylabel('Fault Current (Amps)')
    plt.title('SLG Fault Current vs. Distance')

    # Annotate the point of intersection
    plt.annotate(f'Intersection\n({closest_distance:.2f} miles, {measured_mag:.0f} Amps)', 
                 xy=(closest_distance, measured_mag), 
                xytext=(closest_distance + 0.5, measured_mag + 200), 
                arrowprops=dict(arrowstyle='->'),
                fontsize=9)

    plt.legend()
    plt.grid(True)
    plt.show()

    return closest_distance, np.abs(calc_fault_current[closest_idx])
        
def locate_primary_line_fault_3ph(ZBus_obj, Zline_obj, measured_mag):
    #MVA_base = ZBus_obj.MVA_base
    #Zbase = ZBus_obj.Zbase 
    Ibase = ZBus_obj.Ibase
    voltage_level = ZBus_obj.voltage_level
    voltage_level_pu = ZBus_obj.voltage_level_pu
    #line_length_ft = Zline_obj.total_length_feet
    line_length_mi = Zline_obj.total_length_miles
    Zpos_line_pu = Zline_obj.total_Z_100MVA / 100
    Zo_line_pu = Zline_obj.total_Zo_100MVA /100
    Zpos_bus_pu = ZBus_obj.z_100MVA / 100
    Zo_bus_pu = ZBus_obj.zo_100MVA /100
    #Zpos_lol_pu = (ZBus_obj.z_100MVA / 100) + (Zline_obj.total_Z_100MVA / 100) #Z1 in pu for length of given length of line trace + bus impedance in pu 
    #Zo_lol_pu = (ZBus_obj.zo_100MVA / 100) + (Zline_obj.total_Zo_100MVA /100) #Z0 in pu for length of given length of line trace + bus impedance in pu

    #calculate the line impedance per unit length
    Zpos_line_per_mile = Zpos_line_pu / line_length_mi
    Zo_line_per_mile = Zo_line_pu / line_length_mi

    # Initialize distance array and fault current array
    distance = np.linspace(0, line_length_mi, 1000)
    calc_fault_current = np.zeros(distance.shape, dtype=complex)

    for i, d in enumerate(distance):
        # Calculate the total impedance for the 3-ph fault
        Zpos_total_pu = Zpos_bus_pu + d * Zpos_line_per_mile

        # Calculating the line to ground fault current
        #3-ph fault
        three_ph_fault_pu = voltage_level_pu / (Zpos_total_pu)
        three_ph_fault_pu_mag = abs(three_ph_fault_pu)
        three_ph_fault_pu_ang_rads = cmath.phase(three_ph_fault_pu)
        three_ph_fault_pu_ang_degs = math.degrees(three_ph_fault_pu_ang_rads)
        three_ph_fault = (three_ph_fault_pu_mag * Ibase * 1000)

        calc_fault_current[i] = three_ph_fault

    # Find the index where the calculated fault current is closest to the given fault current
    closest_idx = np.argmin(np.abs(np.abs(calc_fault_current) - measured_mag))
    closest_distance = distance[closest_idx]

    # Plot the fault current
    plt.figure(figsize=(10, 6))
    plt.plot(distance, calc_fault_current, label='Calculated Current Amps')
    plt.axhline(measured_mag, color='r', linestyle='--', label=f'Measured fault current = {measured_mag:.0f} Amps')
    plt.xlabel('Distance (miles)')
    plt.ylabel('Fault Current (Amps)')
    plt.title('3 Phase Fault Current vs. Distance')

    # Annotate the point of intersection
    plt.annotate(f'Intersection\n({closest_distance:.2f} miles, {measured_mag:.0f} Amps)', 
                 xy=(closest_distance, measured_mag), 
                xytext=(closest_distance + 0.5, measured_mag + 200), 
                arrowprops=dict(arrowstyle='->'),
                fontsize=9)

    plt.legend()
    plt.grid(True)
    plt.show()

    return closest_distance, np.abs(calc_fault_current[closest_idx])

def locate_primary_line_fault_l_l(ZBus_obj, Zline_obj, measured_mag):
    #MVA_base = ZBus_obj.MVA_base
    #Zbase = ZBus_obj.Zbase 
    Ibase = ZBus_obj.Ibase
    voltage_level = ZBus_obj.voltage_level
    voltage_level_pu = ZBus_obj.voltage_level_pu
    #line_length_ft = Zline_obj.total_length_feet
    line_length_mi = Zline_obj.total_length_miles
    Zpos_line_pu = Zline_obj.total_Z_100MVA / 100
    Zo_line_pu = Zline_obj.total_Zo_100MVA /100
    Zpos_bus_pu = ZBus_obj.z_100MVA / 100
    Zo_bus_pu = ZBus_obj.zo_100MVA /100
    #Zpos_lol_pu = (ZBus_obj.z_100MVA / 100) + (Zline_obj.total_Z_100MVA / 100) #Z1 in pu for length of given length of line trace + bus impedance in pu 
    #Zo_lol_pu = (ZBus_obj.zo_100MVA / 100) + (Zline_obj.total_Zo_100MVA /100) #Z0 in pu for length of given length of line trace + bus impedance in pu

    #calculate the line impedance per unit length
    Zpos_line_per_mile = Zpos_line_pu / line_length_mi
    Zo_line_per_mile = Zo_line_pu / line_length_mi

    # Initialize distance array and fault current array
    distance = np.linspace(0, line_length_mi, 1000)
    calc_fault_current = np.zeros(distance.shape, dtype=complex)

    for i, d in enumerate(distance):
        # Calculate the total impedance for the l-l fault
        Zpos_total_pu = Zpos_bus_pu + d * Zpos_line_per_mile

        #line-to-line fault
        l_l_fault_pos = voltage_level_pu / (Zpos_total_pu * 2) #Ia sequence
        l_l_fault_pu = (-1j) * (3 ** 0.5) * l_l_fault_pos #Ib fault current pu
        l_l_fault_pu_mag = abs(l_l_fault_pu)
        l_l_fault_pu_ang_rads = cmath.phase(l_l_fault_pu)
        l_l_fault_pu_ang_degs = math.degrees(l_l_fault_pu_ang_rads)
        l_l_fault = l_l_fault_pu_mag * Ibase * 1000

        calc_fault_current[i] = l_l_fault

    # Find the index where the calculated fault current is closest to the given fault current
    closest_idx = np.argmin(np.abs(np.abs(calc_fault_current) - measured_mag))
    closest_distance = distance[closest_idx]

    # Plot the fault current
    plt.figure(figsize=(10, 6))
    plt.plot(distance, calc_fault_current, label='Calculated Current Amps')
    plt.axhline(measured_mag, color='r', linestyle='--', label=f'Measured fault current = {measured_mag:.0f} Amps')
    plt.xlabel('Distance (miles)')
    plt.ylabel('Fault Current (Amps)')
    plt.title('Line to Line Fault Current vs. Distance')

    # Annotate the point of intersection
    plt.annotate(f'Intersection\n({closest_distance:.2f} miles, {measured_mag:.0f} Amps)', 
                 xy=(closest_distance, measured_mag), 
                xytext=(closest_distance + 0.5, measured_mag + 200), 
                arrowprops=dict(arrowstyle='->'),
                fontsize=9)

    plt.legend()
    plt.grid(True)
    plt.show()

    return closest_distance, np.abs(calc_fault_current[closest_idx])

def locate_primary_line_fault_l_l_g(ZBus_obj, Zline_obj, measured_mag):
    #MVA_base = ZBus_obj.MVA_base
    #Zbase = ZBus_obj.Zbase 
    Ibase = ZBus_obj.Ibase
    #voltage_level = ZBus_obj.voltage_level
    voltage_level_pu = ZBus_obj.voltage_level_pu
    #line_length_ft = Zline_obj.total_length_feet
    line_length_mi = Zline_obj.total_length_miles
    Zpos_line_pu = Zline_obj.total_Z_100MVA / 100
    Zo_line_pu = Zline_obj.total_Zo_100MVA /100
    Zpos_bus_pu = ZBus_obj.z_100MVA / 100
    Zo_bus_pu = ZBus_obj.zo_100MVA /100
    #Zpos_lol_pu = (ZBus_obj.z_100MVA / 100) + (Zline_obj.total_Z_100MVA / 100) #Z1 in pu for length of given length of line trace + bus impedance in pu 
    #Zo_lol_pu = (ZBus_obj.zo_100MVA / 100) + (Zline_obj.total_Zo_100MVA /100) #Z0 in pu for length of given length of line trace + bus impedance in pu

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

        # Calculating the line-to-line-to-ground fault current
        l_l_g_fault_Z2_pu = Zpos_total_pu
        l_l_g_fault_Zf_pu = (l_l_g_fault_Z2_pu * Zo_total_pu) / (Zo_total_pu + l_l_g_fault_Z2_pu)
        l_l_g_fault_pos_pu = voltage_level_pu / (Zpos_total_pu + l_l_g_fault_Zf_pu) #I1 positive sequence
        l_l_g_fault_neg_pu = -l_l_g_fault_pos_pu * (Zo_total_pu / (Zo_total_pu + l_l_g_fault_Z2_pu)) #I2 negative sequence
        l_l_g_fault_zero_pu = -l_l_g_fault_pos_pu * (l_l_g_fault_Z2_pu / (Zo_total_pu + l_l_g_fault_Z2_pu)) #I0 zero sequence
        A = np.array([[1, 1, 1],[1, -0.5 - 0.866j, -0.5 + 0.866j],[1, -0.5 + 0.866j, -0.5 - 0.866j]]) #A matrix
        I_seq = np.array([l_l_g_fault_zero_pu, l_l_g_fault_pos_pu, l_l_g_fault_neg_pu]) #Sequence currents matrix
        I_phase = np.dot(A, I_seq)
        l_l_g_fault_Aph_pu, l_l_g_fault_Bph_pu, l_l_g_fault_Cph_pu = I_phase #Individual phases line-to-line-to Ground fault
        l_l_g_fault_Bph = abs(l_l_g_fault_Bph_pu) * Ibase * 1000
        l_l_g_fault_pu_ang_rads_Bph = cmath.phase(l_l_g_fault_Bph_pu)
        l_l_g_fault_pu_ang_degs_Bph = math.degrees(l_l_g_fault_pu_ang_rads_Bph)
        l_l_g_fault_Cph = abs(l_l_g_fault_Cph_pu) * Ibase * 1000
        l_l_g_fault_pu_ang_rads_Cph = cmath.phase(l_l_g_fault_Cph_pu)
        l_l_g_fault_pu_ang_degs_Cph = math.degrees(l_l_g_fault_pu_ang_rads_Cph)

        calc_fault_current[i] = l_l_g_fault_Bph

    # Find the index where the calculated fault current is closest to the given fault current
    closest_idx = np.argmin(np.abs(np.abs(calc_fault_current) - measured_mag))
    closest_distance = distance[closest_idx]

    # Plot the fault current
    plt.figure(figsize=(10, 6))
    plt.plot(distance, calc_fault_current, label='Calculated Current Amps')
    plt.axhline(measured_mag, color='r', linestyle='--', label=f'Measured fault current = {measured_mag:.0f} Amps')
    plt.xlabel('Distance (miles)')
    plt.ylabel('Fault Current (Amps)')
    plt.title('Double Line to Ground Fault Current vs. Distance')

    # Annotate the point of intersection
    plt.annotate(f'Intersection\n({closest_distance:.2f} miles, {measured_mag:.0f} Amps)', 
                 xy=(closest_distance, measured_mag), 
                xytext=(closest_distance + 0.5, measured_mag + 200), 
                arrowprops=dict(arrowstyle='->'),
                fontsize=9)

    plt.legend()
    plt.grid(True)
    plt.show()

    return closest_distance, np.abs(calc_fault_current[closest_idx])


    