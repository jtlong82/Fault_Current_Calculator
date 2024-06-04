import matplotlib.pyplot as plt
import numpy as np

# Function to convert polar to rectangular form
def polar_to_rectangular(magnitude, angle_degrees):
    angle_radians = np.deg2rad(angle_degrees)
    real = magnitude * np.cos(angle_radians)
    imaginary = magnitude * np.sin(angle_radians)
    return complex(real, imaginary)

# Function to plot the impedance graph
def plot_impedance_graph(relay_reach, relay_angle, end_of_line_impedances, secondary_transformer_impedances):
    fig, ax = plt.subplots()
    
    # Define axes
    ax.set_xlabel('X-axis = R (Real ohms)')
    ax.set_ylabel('Y-axis = X (Imaginary ohms)')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(color='gray', linestyle='--', linewidth=0.5)
    
    # Set equal aspect ratio
    ax.set_aspect('equal', adjustable='box')
    
    # Relay reach and angle
    relay_angle_rad = np.deg2rad(relay_angle)
    relay_reach_x = relay_reach * np.cos(relay_angle_rad)
    relay_reach_y = relay_reach * np.sin(relay_angle_rad)
    
    # Center of the relay circle
    center_x = relay_reach_x / 2
    center_y = relay_reach_y / 2
    
    # Relay circle
    circle = plt.Circle((center_x, center_y), relay_reach / 2, color='blue', fill=False)
    ax.add_artist(circle)
    
    # Relay tolerance circles
    circle_85 = plt.Circle((center_x, center_y), (relay_reach * 0.85) / 2, color='red', linestyle='dotted', fill=False)
    circle_115 = plt.Circle((center_x, center_y), (relay_reach * 1.15) / 2, color='red', linestyle='dotted', fill=False)
    ax.add_artist(circle_85)
    ax.add_artist(circle_115)
    
    # Plot End of Line Impedances
    for impedance in end_of_line_impedances:
        ax.plot(impedance.real, impedance.imag, 'rx', label='End of Line' if impedance == end_of_line_impedances[0] else "")
    
    # Plot Secondary of Transformer Impedances
    for impedance in secondary_transformer_impedances:
        ax.plot(impedance.real, impedance.imag, 'bo', label='Secondary of Transformer' if impedance == secondary_transformer_impedances[0] else "")
    
    # Plot the relay reach line
    ax.plot([0, relay_reach_x], [0, relay_reach_y], 'g--', label='Relay Reach')
    
    ax.legend()
    plt.title('Impedance (Primary Ohms)')
    plt.show()

# Helper function to get a list of impedances in polar form
def get_impedances(prompt):
    impedances = []
    while True:
        magnitude = input(f"Enter the Magnitude of {prompt} Impedance (or 'done' to finish): ")
        if magnitude.lower() == 'done':
            break
        angle = input(f"Enter the Angle (degrees) of {prompt} Impedance: ")
        impedances.append(polar_to_rectangular(float(magnitude), float(angle)))
    return impedances

# User inputs
relay_reach = float(input("Enter the Relay Reach: "))
relay_angle = float(input("Enter the Relay Angle (degrees): "))

# Get multiple end of line impedances
end_of_line_impedances = get_impedances("End of Line")

# Get multiple secondary of transformer impedances
secondary_transformer_impedances = get_impedances("Secondary of Transformer")

# Plot the graph
plot_impedance_graph(relay_reach, relay_angle, end_of_line_impedances, secondary_transformer_impedances)


