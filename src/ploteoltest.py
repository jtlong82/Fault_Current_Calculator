import numpy as np
import matplotlib.pyplot as plt

def resize_circles(Z_reach, substation_impedances, eol_impedances):
    # Find the eol_impedance with the largest magnitude
    max_eol_impedance = max(eol_impedances, key=lambda z: np.abs(z))
    
    # Adjust the Mho circle so that the largest eol_impedance touches the 15% smaller circle
    r_smaller_based_on_eol = np.abs(max_eol_impedance) / 0.85
    r_mho_based_on_eol = r_smaller_based_on_eol / 0.85
    r_larger_based_on_eol = r_mho_based_on_eol * 1.15
    
    # Check if the smallest substation impedance is within the 15% larger circle based on EOL
    min_substation_impedance = min(substation_impedances, key=lambda z: np.abs(z))
    print(f"Min_sub: {np.abs(min_substation_impedance)}")
    print(f"Large EOL: {r_larger_based_on_eol}")
    if np.abs(min_substation_impedance) < r_larger_based_on_eol:
        # If so, resize the 15% larger circle to just touch the lowest impedance substation
        r_larger = np.abs(min_substation_impedance)
        r_mho = r_larger / 1.15
        r_smaller = r_mho * 0.85
    else:
        # If not, keep the EOL based adjustments
        r_larger = r_larger_based_on_eol
        r_mho = r_mho_based_on_eol
        r_smaller = r_smaller_based_on_eol
    
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
substation_impedances = [(0.6 + 2j), (0.7 + 2.3j), (0.9 + 2.5j), (0.55 + 1.9j), (0.5 + 2.1j)]
eol_impedances = [(0.5 + 1.0j), (0.5 + 1.25j)]

# Adjust the circles based on the substation impedances
Z_reach_adjusted, r_mho, r_larger, r_smaller = resize_circles(Z_reach, substation_impedances, eol_impedances)

# Relay angle remains the same
relay_angle_rad = np.angle(Z_reach)

# Calculate the actual radius of the Mho circle, which is half of Z_reach
radius = np.abs(Z_reach) / 2

# Calculate the offset from the origin to the circle's center, taking into account that Z_reach is the diameter
offset_from_origin = radius * (1 - np.cos(relay_angle_rad))

# Create the circles
theta = np.linspace(0, 2*np.pi, 100)
x_mho = radius * np.cos(theta)
y_mho = radius * np.sin(theta) + offset_from_origin
x_larger = (radius * 1.15) * np.cos(theta)
y_larger = (radius * 1.15) * np.sin(theta) + offset_from_origin
x_smaller = (radius * 0.85) * np.cos(theta)
y_smaller = (radius * 0.85) * np.sin(theta) + offset_from_origin

# Create relay angle line from the origin to the edge of the Mho circle
end_x = radius * np.cos(relay_angle_rad)
end_y = radius * np.sin(relay_angle_rad) + offset_from_origin

# Find the dynamic plot limits including the origin
min_real, max_real, min_imag, max_imag = find_plot_limits_with_origin(substation_impedances + eol_impedances, r_larger)

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