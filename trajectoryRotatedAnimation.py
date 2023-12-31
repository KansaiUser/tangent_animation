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
    # if frame_number < 0 or frame_number >= num_points:
    #     return None  # Frame number out of range

    if frame_number < 0:
        return None  # Frame number out of range
    if (frame_number+1) >= num_points:
        nextframe = 0
    else:
        nextframe = frame_number + 1

    # Calculate the tangent vector at the specified frame number
    dx = X[nextframe] - X[frame_number]
    dy = Y[nextframe] - Y[frame_number]
    magnitude = np.sqrt(dx**2 + dy**2)

    if magnitude == 0:
        return (0, 0)  # Avoid division by zero

    tangent_vector = (dx / magnitude, dy / magnitude)
    return tangent_vector


# Function to check if points of the trajectory are in or out
def isin(X, Y, theta, XC, YC):
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
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
    # print("Angle:", math.degrees(theta))
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

    return theta, rectangle_x, rectangle_y


# 3. Start feature
example_frame = 0
tangent_vector = calculate_unit_tangent_vector(example_frame)
print(tangent_vector)
print(X[example_frame], Y[example_frame])
XC, YC = X[example_frame], Y[example_frame]
XD, YD = tangent_vector
theta, rectangle_x, rectangle_y = calculate_rectangle(XD, YD, XC, YC)

# 4. Plot the static plot

fig, ax = plt.subplots()
ax.axis("equal")
ax.grid(True)


# 5. Plot the dynamic features once

# we apply the function to isolate the in points
m1 = isin(data['X'], data['Y'], theta, XC, YC)
m2 = isin(data['XL'], data['YL'], theta, XC, YC)
m3 = isin(data['XR'], data['YR'], theta, XC, YC)

angle_degrees = 90 - math.degrees(theta)
print("Angle :", angle_degrees)
rotate_with_parameters = lambda X, Y: rotate_coordinates(X, Y, angle_degrees, XC, YC)
rec = list(map(rotate_with_parameters, rectangle_x, rectangle_y))
print(rec)
RX, RY = zip(*rec)
print(RX, RY)

XCR, YCR = rotate_coordinates(XC, YC, angle_degrees, XC, YC)


rec, = ax.plot(RX, RY, c='k')
XRotated, YRotated = rotate_coordinates(data.loc[m1, 'X'], data.loc[m1, 'Y'], angle_degrees, XC, YC)
LC = ax.scatter(XRotated, YRotated, c='b')
XLRotated, YLRotated = rotate_coordinates(data.loc[m2, 'XL'], data.loc[m2, 'YL'], angle_degrees, XC, YC)
LL = ax.scatter(XLRotated, YLRotated, c='r')
XRRotated, YRRotated = rotate_coordinates(data.loc[m3, 'XR'], data.loc[m3, 'YR'], angle_degrees, XC, YC)
LR = ax.scatter(XRRotated, YRRotated, c='g')
car = ax.scatter(XCR, YCR, color='r')

# the following will not be necessary when we address the translation too
# that we are not doing yet
ax.set_xlim(XCR-1.1*(height/2), XCR+1.1*(height/2))
ax.set_ylim(YCR-width/2, YCR+width/2)

ListX = []
ListY = []

# 6. Animate function
def animate(frame):
    tangent_vector = calculate_unit_tangent_vector(frame)
    XC, YC = X[frame], Y[frame]
    XD, YD = tangent_vector
    theta, rectangle_x, rectangle_y = calculate_rectangle(XD, YD, XC, YC)
    m1 = isin(data['X'], data['Y'], theta, XC, YC)
    m2 = isin(data['XL'], data['YL'], theta, XC, YC)
    m3 = isin(data['XR'], data['YR'], theta, XC, YC)
    angle_degrees = 90 - math.degrees(theta)
    rotate_with_parameters = lambda X, Y: rotate_coordinates(X, Y, angle_degrees, XC, YC)
    rec2 = list(map(rotate_with_parameters, rectangle_x, rectangle_y))

    RX, RY = zip(*rec2)
    XCR, YCR = rotate_coordinates(XC, YC, angle_degrees, XC, YC)
    XRotated, YRotated = rotate_coordinates(data.loc[m1, 'X'], data.loc[m1, 'Y'], angle_degrees, XC, YC)
    XLRotated, YLRotated = rotate_coordinates(data.loc[m2, 'XL'], data.loc[m2, 'YL'], angle_degrees, XC, YC)
    XRRotated, YRRotated = rotate_coordinates(data.loc[m3, 'XR'], data.loc[m3, 'YR'], angle_degrees, XC, YC)

    # modify the plots

    rec.set_data(RX, RY)
    # LC.set_offsets([XRotated, YRotated])
    LC.set_offsets(np.column_stack((XRotated, YRotated)))
    # LL.set_offsets([XLRotated, YLRotated])
    LL.set_offsets(np.column_stack((XLRotated, YLRotated)))
    # LR.set_offsets([XRRotated, YRRotated])
    LR.set_offsets(np.column_stack((XRRotated, YRRotated)))
    car.set_offsets([XCR, YCR])
    print(frame, XCR, YCR)
    ListX.append(XCR)
    ListY.append(YCR)

    # this will later be unnecessary
    ax.set_xlim(XCR-1.1*(height/2), XCR+1.1*(height/2))
    ax.set_ylim(YCR-width/2, YCR+width/2)

    # return  rec,   LC, LL, LR, car,
    return LC,


# 7. Call FuncAnimation
animation = FuncAnimation(fig, animate, frames=np.arange(0, num_points, 1),
                          blit=False)  # False in order to allow the axis to move


plt.show()


# fig2 = plt.figure()
# plt.plot(ListX, ListY)
# plt.grid()
# plt.axis('equal')
# plt.show()
