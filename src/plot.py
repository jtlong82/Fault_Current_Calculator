import numpy as np
import matplotlib.pyplot as plt

# Function to resize the Mho circles
def resize_circles(Z_reach, substation_impedances):
    # Find the substation with the lowest impedance magnitude
    min_substation_impedance = min(substation_impedances, key=lambda z: np.abs(z))
    
    # Calculate the radius of the 15% larger circle to be equal to the distance from the origin to this substation
    r_larger = np.abs(min_substation_impedance)
    
    # Adjust the original Mho circle's radius to be 15% smaller than the new larger circle's radius
    r_mho = r_larger / 1.15
    r_smaller = r_mho * 0.85  # 15% smaller than the adjusted Mho circle radius
    
    # Calculate the new reach impedance Z_reach for the adjusted Mho circle
    Z_reach_adjusted = r_mho * (Z_reach / np.abs(Z_reach))
    
    return Z_reach_adjusted, r_mho, r_larger, r_smaller

def find_plot_limits_with_origin(substation_impedances, r_larger):
    # Extract real and imaginary parts of the substation impedances
    real_parts = [z.real for z in substation_impedances]
    imag_parts = [z.imag for z in substation_impedances]

    # Include the radius of the largest circle to ensure it is within the limits
    real_parts.append(r_larger)
    imag_parts.append(r_larger)

    # Include origin in the plot range
    real_parts.append(0)
    imag_parts.append(0)

    # Find the maximum and minimum values with some padding
    padding = 0.1  # 10% padding
    min_real = min(real_parts) - (max(real_parts) - min(real_parts)) * padding
    max_real = max(real_parts) + (max(real_parts) - min(real_parts)) * padding
    min_imag = min(imag_parts) - (max(imag_parts) - min(imag_parts)) * padding
    max_imag = max(imag_parts) + (max(imag_parts) - min(imag_parts)) * padding

    # Ensure we have a little bit into the negative axis regions
    min_real = min(min_real, -0.1 * max_real)
    min_imag = min(min_imag, -0.1 * max_imag)

    return min_real, max_real, min_imag, max_imag

# Initial parameters
Z_reach = 0.25 + 1j  # Relay reach impedance
substation_impedances = [(0.6 + 1.7j), (0.7 + 1.8j), (0.9 + 2.5j), (0.55 + 1.9j), (0.5 + 1.7j)]
eol_impedances = [(0.5 + 1.0j), (0.5 + 1.25j)]

# Adjust the circles based on the substation impedances
Z_reach_adjusted, r_mho, r_larger, r_smaller = resize_circles(Z_reach, substation_impedances)

# Relay angle remains the same
relay_angle_rad = np.angle(Z_reach)

# Create the circles
theta = np.linspace(0, 2*np.pi, 100)
x_mho = r_mho * np.cos(theta)
y_mho = r_mho * np.sin(theta)
x_larger = r_larger * np.cos(theta)
y_larger = r_larger * np.sin(theta)
x_smaller = r_smaller * np.cos(theta)
y_smaller = r_smaller * np.sin(theta)

# Create relay angle line
end_x = r_mho * np.cos(relay_angle_rad)
end_y = r_mho * np.sin(relay_angle_rad)

# Find the dynamic plot limits including the origin
min_real, max_real, min_imag, max_imag = find_plot_limits_with_origin(substation_impedances, r_larger)

# Plotting
plt.figure(figsize=(10, 10))
plt.plot(x_mho, y_mho, label='Adjusted Mho Circle')
plt.plot(x_larger, y_larger, 'c:', label='15% Larger Circle')
plt.plot(x_smaller, y_smaller, 'c:', label='15% Smaller Circle')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.plot([0, end_x], [0, end_y], label='Relay Angle Line')

# Plot substation impedances with dots
for Z in substation_impedances:
    plt.scatter(Z.real, Z.imag, color='b', label='Substation' if 'Substation' not in plt.gca().get_legend_handles_labels()[1] else "")

# Plot end of line impedances with 'X's
for Z in eol_impedances:
    plt.scatter(Z.real, Z.imag, marker='x', color='r', label='End of Line' if 'End of Line' not in plt.gca().get_legend_handles_labels()[1] else "")

plt.xlabel('Real (Resistance)')
plt.ylabel('Imaginary (Reactance)')
plt.title('Adjusted Mho Circle with Relay Angle and Substation Impedances')
plt.legend(loc='upper left')
plt.axis('equal')
plt.xlim(min_real, max_real)
plt.ylim(min_imag, max_imag)
plt.grid(True)
plt.show()