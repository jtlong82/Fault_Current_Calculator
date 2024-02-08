import numpy as np
import cmath
import math

# Given parameters
Vf = 1.0  # Line-to-neutral voltage in per unit (pu) (example value)
Z1 = 0.262+1.294j  # Positive sequence impedance in per unit (pu) (example value)
Z2 = Z1  # Negative sequence impedance in per unit (pu) (example value)
Z0 = 0.053+0.665j  # Zero sequence impedance in per unit (pu) (example value)

V_seq_matrix = np.array([[0], [Vf], [0]])
Z_seq_matrix = np.array([[Z0, 0, 0], [0, Z1, 0], [0, 0, Z2]])

Sbase = 100
Vbase = 13.2
Ibase = Sbase / (((3 ** 0.5)) * Vbase)

# Symmetrical components transformation matrix
a = np.exp(1j * np.pi * 2/3)  # 120 degree phase shift
a_rads = cmath.phase(a)
a_degs = math.degrees(a_rads)

a2 = a**2
a2_rads = cmath.phase(a2)
a2_degs = math.degrees(a2_rads)

#ACB Rotation
A = np.array([[1, 1, 1], [1, a, a**2], [1, a**2, a]])

# Inverse of the symmetrical components transformation matrix
A_inv = (1/3) * np.linalg.inv(A)

#########################3-phase FAULT#############################
# Calculate sequence currents (series connection of sequence impedances)
I1 = Vf / Z1
I0 = I2 = 0
I_seq_matrix = np.array([[I0], [I1], [I2]]) 
I0_rads = cmath.phase(I0)
I0_degs = math.degrees(I0_rads)
I1_rads = cmath.phase(I1)
I1_degs = math.degrees(I1_rads)
I2_rads = cmath.phase(I2)
I2_degs = math.degrees(I2_rads)

# Convert sequence currents to phase currents
IA = I0 + I1 + I2
IB = I0 + (a * I1) + (a**2 * I2)
IC = I0 + (a**2 * I1) + (a * I2)
IA_rads = cmath.phase(IA)
IA_degs = math.degrees(IA_rads)
IB_rads = cmath.phase(IB)
IB_degs = math.degrees(IB_rads)
IC_rads = cmath.phase(IC)
IC_degs = math.degrees(IC_rads)

V_seq = V_seq_matrix - np.dot(Z_seq_matrix, I_seq_matrix)
     
V0, V1, V2 = V_seq
V0 = V0[0]  # Extract the first element from the array
V1 = V1[0]
V2 = V2[0]

V0_rads = cmath.phase(V0)
V0_degs = math.degrees(V0_rads)
V1_rads = cmath.phase(V1)
V1_degs = math.degrees(V1_rads)
V2_rads = cmath.phase(V2)
V2_degs = math.degrees(V2_rads)

# Calculate phase voltages using sequence currents and impedances
VA, VB, VC = np.dot(A, V_seq)
VA = VA[0]  # Extract the first element from the array
VB = VB[0]
VC = VC[0]
VA_rads = cmath.phase(VA)
VA_degs = math.degrees(VA_rads)
VB_rads = cmath.phase(VB)
VB_degs = math.degrees(VB_rads)
VC_rads = cmath.phase(VC)
VC_degs = math.degrees(VC_rads)

print("\n3ph Fault")
print(f"V0 = {abs(V0 * Vbase):.2f}∠{V0_degs:.2f}° kV, V1 = {abs(V1 * Vbase):.2f}∠{V1_degs:.2f}° kV, V2 = {abs(V2 * Vbase):.2f}∠{V2_degs:.2f}° kV")
print(f"I0 = {abs(I0 * Ibase):.3f}∠{I0_degs:.2f}° kA, I1 = {abs(I1 * Ibase):.3f}∠{I1_degs:.2f}° kA, I2 = {abs(I2 * Ibase):.3f}∠{I2_degs:.2f}° kA")
print(f"VA = {abs(VA * Vbase):.2f}∠{VA_degs:.2f}° kV, VB = {abs(VB * Vbase):.2f}∠{VB_degs:.2f}° kV, VC = {abs(VC * Vbase):.2f}∠{VC_degs:.2f}° kV")
print(f"IA = {abs(IA * Ibase):.3f}∠{IA_degs:.2f}° kA, IB = {abs(IB * Ibase):.3f}∠{IB_degs:.2f}° kA, IC = {abs(IC * Ibase):.3f}∠{IC_degs:.2f}° kA")

#########################SINGLE LINE TO GROUND FAULT#############################
# Calculate sequence currents (series connection of sequence impedances)
I0 = I1 = I2 = Vf / (Z1 + Z2 + Z0)
I_seq_matrix = np.array([[I0], [I1], [I2]]) 
I0_rads = cmath.phase(I0)
I0_degs = math.degrees(I0_rads)
I1_rads = cmath.phase(I1)
I1_degs = math.degrees(I1_rads)
I2_rads = cmath.phase(I2)
I2_degs = math.degrees(I2_rads)

# Convert sequence currents to phase currents
IA = I0 + I1 + I2
IB = IC = 0 + 0j
IA_rads = cmath.phase(IA)
IA_degs = math.degrees(IA_rads)
IB_rads = cmath.phase(IB)
IB_degs = math.degrees(IB_rads)
IC_rads = cmath.phase(IC)
IC_degs = math.degrees(IC_rads)

V_seq = V_seq_matrix - np.dot(Z_seq_matrix, I_seq_matrix)
     
V0, V1, V2 = V_seq
V0 = V0[0]  # Extract the first element from the array
V1 = V1[0]
V2 = V2[0]

V0_rads = cmath.phase(V0)
V0_degs = math.degrees(V0_rads)
V1_rads = cmath.phase(V1)
V1_degs = math.degrees(V1_rads)
V2_rads = cmath.phase(V2)
V2_degs = math.degrees(V2_rads)

# Calculate phase voltages using sequence currents and impedances
VA, VB, VC = np.dot(A, V_seq)
VA = VA[0]  # Extract the first element from the array
VB = VB[0]
VC = VC[0]
VA_rads = cmath.phase(VA)
VA_degs = math.degrees(VA_rads)
VB_rads = cmath.phase(VB)
VB_degs = math.degrees(VB_rads)
VC_rads = cmath.phase(VC)
VC_degs = math.degrees(VC_rads)

print("\nSLG Fault")
print(f"V0 = {abs(V0 * Vbase):.2f}∠{V0_degs:.2f}° kV, V1 = {abs(V1 * Vbase):.2f}∠{V1_degs:.2f}° kV, V2 = {abs(V2 * Vbase):.2f}∠{V2_degs:.2f}° kV")
print(f"I0 = {abs(I0 * Ibase):.3f}∠{I0_degs:.2f}° kA, I1 = {abs(I1 * Ibase):.3f}∠{I1_degs:.2f}° kA, I2 = {abs(I2 * Ibase):.3f}∠{I2_degs:.2f}° kA")
print(f"VA = {abs(VA * Vbase):.2f}∠{VA_degs:.2f}° kV, VB = {abs(VB * Vbase):.2f}∠{VB_degs:.2f}° kV, VC = {abs(VC * Vbase):.2f}∠{VC_degs:.2f}° kV")
print(f"IA = {abs(IA * Ibase):.3f}∠{IA_degs:.2f}° kA, IB = {abs(IB * Ibase):.3f}∠{IB_degs:.2f}° kA, IC = {abs(IC * Ibase):.3f}∠{IC_degs:.2f}° kA")

print(f"{abs(a):.2f}∠{a_degs:.2f}°")
print(f"{abs(a ** 2):.2f}∠{a2_degs:.2f}°")


