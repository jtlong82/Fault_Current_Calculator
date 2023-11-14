import numpy as np
import matplotlib.pyplot as plt

# Initial parameters
Z_reach = 0.25 + 1j  # Relay reach impedance
substation_impedances = [(0.6 + 2j), (0.7 + 2.3j), (0.9 + 2.5j), (0.55 + 1.9j), (0.5 + 2.1j)]
eol_impedances = [(0.5 + 1.0j), (0.5 + 1.25j)]

# Relay angle in radians and diameter
relay_angle_rad = np.angle(Z_reach)
diameter = np.abs(Z_reach)

# Calculate the center of the circle
center_x = (diameter / 2) * np.cos(relay_angle_rad)
center_y = (diameter / 2) * np.sin(relay_angle_rad)

# Create the Mho circle around the center
theta = np.linspace(0, 2*np.pi, 100)
x_circle = (diameter / 2) * np.cos(theta) + center_x
y_circle = (diameter / 2) * np.sin(theta) + center_y

# Z_reach line coordinates (from the origin through the circle's center to the edge of the circle)
line_x = [0, center_x * 2]
line_y = [0, center_y * 2]

# Plotting
plt.figure(figsize=(10, 10))
plt.plot(x_circle, y_circle, label='Mho Circle')
plt.plot(line_x, line_y, label='Z_reach Line', color='orange')

# Plot substation and EOL impedances
for Z in substation_impedances:
    plt.scatter(Z.real, Z.imag, color='blue', marker='o', label='Substation' if 'Substation' not in plt.gca().get_legend_handles_labels()[1] else "")
for Z in eol_impedances:
    plt.scatter(Z.real, Z.imag, color='red', marker='x', label='End of Line' if 'End of Line' not in plt.gca().get_legend_handles_labels()[1] else "")

plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.xlabel('Real (Resistance)')
plt.ylabel('Imaginary (Reactance)')
plt.title('Mho Circle with Relay Angle and Substation Impedances')
plt.legend(loc='upper left')
plt.axis('equal')
plt.grid(True)
plt.show()
