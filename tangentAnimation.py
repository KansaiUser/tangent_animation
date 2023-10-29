import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Define the number of data points
num_points = 500

# Create an array of frame numbers from 1 to num_points
frame_numbers = np.arange(1, num_points + 1)

# Create a parametric equation for a circle with sinusoidal oscillation
t = np.linspace(0, 2 * np.pi, num_points)
radius = 1.0
amplitude = 0.1
frequency = 5.0

X = radius * np.cos(t) + amplitude * np.sin(frequency * t)
Y = radius * np.sin(t) + amplitude * np.cos(frequency * t)


def calculate_unit_tangent_vector(frame_number):
    if frame_number < 0 or frame_number >= num_points:
        return None  # Frame number out of range

    # Calculate the tangent vector at the specified frame number
    dx = X[frame_number + 1] - X[frame_number]
    dy = Y[frame_number + 1] - Y[frame_number]
    magnitude = np.sqrt(dx**2 + dy**2)

    if magnitude == 0:
        return (0, 0)  # Avoid division by zero

    tangent_vector = (dx / magnitude, dy / magnitude)
    return tangent_vector

start_frame = 0
tangent_vector = calculate_unit_tangent_vector(start_frame)
x_tangent, y_tangent = X[start_frame], Y[start_frame]
dx, dy = tangent_vector

fig, ax = plt.subplots()
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-2.0, 2.0)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Circular Trajectory with Sinusoidal Oscillation of X and Y')
ax.grid(True)
ax.axis('equal')

ax.plot(X, Y, marker='o', markersize=3, linestyle='-')
tangent = plt.quiver(x_tangent, y_tangent, dx, dy, color='red', angles='xy',
          scale_units='xy', scale=1, width=0.005)

plt.show()
