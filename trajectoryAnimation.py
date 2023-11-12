import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.animation import FuncAnimation

# 1. Code to get data for trajectory

# Define the number of data points
num_points = 500

# Create an array of frame numbers from 1 to num_points
frame_numbers = np.arange(1, num_points + 1)

# Create a parametric equation for a circle with sinusoidal oscillation
t = np.linspace(0, 2 * np.pi, num_points)
radius = 10.0  # 1.0
amplitude = 0.1
frequency = 5.0

X = radius * (np.cos(t) + amplitude * np.sin(frequency * t))
Y = radius * (np.sin(t) + amplitude * np.cos(frequency * t))

XL = (radius + 1) * (np.cos(t) + amplitude * np.sin(frequency * t))
YL = (radius + 1) * (np.sin(t) + amplitude * np.cos(frequency * t))
XR = (radius - 1) * (np.cos(t) + amplitude * np.sin(frequency * t))
YR = (radius - 1) * (np.sin(t) + amplitude * np.cos(frequency * t))

data = pd.DataFrame({'fr': frame_numbers, 'X': X, 'Y': Y, 'XL': XL, 'YL': YL,
                    'XR': XR, 'YR': YR})

# 2. Necessary functions


# function to calculate the unit tangent vector
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


# Function to check if points of the trajectory are in or out
def isin(X, Y):
    X = X - XC
    Y = Y - YC
    X_ = X * cos_theta + Y * sin_theta
    Y_ = -X * sin_theta + Y * cos_theta
    return (
        (-width / 2 <= X_)
        & (X_ <= width / 2)
        & (-height / 2 <= Y_)
        & (Y_ <= height / 2)
    )


# Rotation function
def rotate_coordinates(X, Y, angle, XC, YC):
    # Convert angle to radians
    angle_rad = np.deg2rad(angle)

    # Translate to the origin
    X_translated = X - XC
    Y_translated = Y - YC

    # Perform the rotation
    X_rotated = X_translated * np.cos(angle_rad) - Y_translated * np.sin(angle_rad)
    Y_rotated = X_translated * np.sin(angle_rad) + Y_translated * np.cos(angle_rad)

    # Translate back to the original position
    X_rotated += XC
    Y_rotated += YC

    return X_rotated, Y_rotated


# Width and Height of the rectangle
width = 3
height = 4


# function to calculate the instantaneous rectangle
def calculate_rectangle(XD, YD, XC, YC):
    theta = np.arctan2(YD, XD)
    print("Angle:", math.degrees(theta))
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    rectangle_x = [
        XC + 0.5 * width * cos_theta - 0.5 * height * sin_theta,
        XC - 0.5 * width * cos_theta - 0.5 * height * sin_theta,
        XC - 0.5 * width * cos_theta + 0.5 * height * sin_theta,
        XC + 0.5 * width * cos_theta + 0.5 * height * sin_theta,
        XC + 0.5 * width * cos_theta - 0.5 * height * sin_theta,
    ]

    rectangle_y = [
        YC + 0.5 * width * sin_theta + 0.5 * height * cos_theta,
        YC - 0.5 * width * sin_theta + 0.5 * height * cos_theta,
        YC - 0.5 * width * sin_theta - 0.5 * height * cos_theta,
        YC + 0.5 * width * sin_theta - 0.5 * height * cos_theta,
        YC + 0.5 * width * sin_theta + 0.5 * height * cos_theta,
    ]

    return rectangle_x, rectangle_y


# 3. Start feature
example_frame = 0
tangent_vector = calculate_unit_tangent_vector(example_frame)
print(tangent_vector)
print(X[example_frame], Y[example_frame])
XC, YC = X[example_frame], Y[example_frame]
XD, YD = tangent_vector
rectangle_x, rectangle_y = calculate_rectangle(XD, YD, XC, YC)

# 4. Plot the static plot


fig, ax = plt.subplots()
ax.plot(data["X"], data["Y"], color="b")
ax.plot(data["XL"], data["YL"], color="r")
ax.plot(data["XR"], data["YR"], color="g")
ax.axis("equal")
ax.grid(True)

# 5. Plot the dynamic features once

if tangent_vector is not None:
    x_tangent, y_tangent = X[example_frame], Y[example_frame]
    dx, dy = tangent_vector
    tangent = ax.quiver(x_tangent, y_tangent, dx, dy, color='violet', angles='xy', scale_units='xy', scale=1, width=0.005)

car = ax.scatter(XC, YC, color='r')
rec1, = ax.plot(rectangle_x, rectangle_y, color='purple')
# rec2 = ax.fill(rectangle_x, rectangle_y, color='purple', alpha=0.4)


# 6. Modifies rec1,rec2 and tangent_vector
# receives frame
def animate(frame):
    tangent_vector = calculate_unit_tangent_vector(frame)
    # x_tangent, y_tangent = X[frame], Y[frame]
    # dx, dy = tangent_vector
    XC, YC = X[frame], Y[frame]
    XD, YD = tangent_vector
    rectangle_x, rectangle_y = calculate_rectangle(XD, YD, XC, YC)

    car.set_offsets([XC, YC])

    tangent.set_UVC(XD, YD)
    tangent.set_offsets([XC, YC])
    rec1.set_data(rectangle_x, rectangle_y)
    # rec2.set_data(rectangle_x, rectangle_y)
    # rec2.get_paths()[0].vertices[:, 0] = rectangle_x
    # rec2.get_paths()[0].vertices[:, 1] = rectangle_y

    return tangent, car, rec1,# rec2,

# 7. Call FuncAnimation

animation = FuncAnimation(fig, animate, frames=np.arange(0, num_points, 1),
                          blit=True)


plt.show()


