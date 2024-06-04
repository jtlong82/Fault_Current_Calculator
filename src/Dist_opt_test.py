import numpy as np
import matplotlib.pyplot as plt

def distance_from_origin(point):
    return np.sqrt(point[0]**2 + point[1]**2)

def find_circle_params(angle_deg, points):
    # Convert angle to radians
    angle_rad = np.deg2rad(angle_deg)
    
    # Identify the furthest point from the origin
    furthest_point = max(points, key=distance_from_origin)
    x1, y1 = furthest_point
    
    # Slope of the line that makes an angle with the x-axis
    m = np.tan(angle_rad)
    
    # The line equation is y = mx
    # The center of the circle (h, k) must lie on this line, hence k = mh
    # We need to find the circle that passes through (x1, y1) and touches the origin (0, 0)
    
    # The distance from (h, k) to (0, 0) is the radius r
    # Also, the distance from (h, k) to (x1, y1) is the radius r
    
    # We solve for h and k by using the fact that:
    # (h^2 + (mh)^2) = ((h - x1)^2 + (mh - y1)^2)
    
    a = 1 + m**2
    b = -2 * (x1 + m * y1)
    c = x1**2 + y1**2
    
    # Solving quadratic equation ax^2 + bx + c = 0 for h
    h = -b / (2 * a)
    k = m * h
    r = np.sqrt(h**2 + k**2)
    
    return h, k, r, furthest_point

def plot_circle(h, k, r, points):
    fig, ax = plt.subplots()
    
    # Create the circle
    circle = plt.Circle((h, k), r, color='b', fill=False)
    ax.add_artist(circle)
    
    # Plot the points
    for point in points:
        ax.plot(point[0], point[1], 'ro')  # The points
    
    # Plot the origin
    ax.plot(0, 0, 'go')  # The origin
    
    # Plot the center
    ax.plot(h, k, 'bo')  # The center (h, k)
    
    # Set the aspect of the plot to be equal
    ax.set_aspect('equal')
    
    # Set limits
    ax.set_xlim(-5, 10)
    ax.set_ylim(-5, 10)
    
    # Labels and title
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Circle Touching the Origin and Passing Through the Furthest Point')
    
    plt.grid(True)
    plt.show()

# Example usage
angle_deg = 75
points = [(4, 8), (3, 8), (2.5, 6), (1, 7)]

h, k, r, furthest_point = find_circle_params(angle_deg, points)
plot_circle(h, k, r, points)

print(f"Center of the circle: ({h}, {k})")
print(f"Radius of the circle: {r}")
print(f"Diameter of the circle: {2 * r}")
print(f"Furthest point: {furthest_point}")







