import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

def find_circle():
    # Function to solve for r (radius)
    def equations(r):
        # Endpoint of diameter at 75 degrees
        x = r * np.cos(np.radians(75))
        y = r * np.sin(np.radians(75))
        
        # Distance from (x,y) to (3,8) should equal r
        return (x-3)**2 + (y-8)**2 - r**2

    # Solve the equation
    radius = fsolve(equations, 10)[0]
    
    # Calculate center
    center_x = radius * np.cos(np.radians(75)) / 2
    center_y = radius * np.sin(np.radians(75)) / 2
    
    return (center_x, center_y), radius

def plot_solution(points, center, radius):
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Plot given points
    ax.scatter(*zip(*points), color='red', label='Given Points')
    
    # Plot center
    ax.scatter(*center, color='green', label='Center')
    
    # Plot circle
    circle = plt.Circle(center, radius, fill=False, color='blue', label='Circle')
    ax.add_artist(circle)
    
    # Plot diameter
    diameter_end = (center[0]*2, center[1]*2)
    ax.plot([0, diameter_end[0]], [0, diameter_end[1]], 'g--', label='Diameter')
    
    # Set limits and labels
    ax.set_xlim(-1, 4)
    ax.set_ylim(-1, 9)
    ax.set_aspect('equal')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()
    ax.grid(True)
    
    plt.title('Circle Solution')
    plt.show()

# Test points
points = [(1, 7), (2.5, 6), (3, 8)]

# Solve and plot
center, radius = find_circle()
plot_solution(points, center, radius)

print(f"Center: {center}")
print(f"Radius: {radius}")
print(f"Diameter: {radius * 2}")


