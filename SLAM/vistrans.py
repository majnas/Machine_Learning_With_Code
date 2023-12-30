import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math


def Rx(theta):
    theta = math.radians(theta)
    return np.matrix([[1, 0, 0],
                      [0, math.cos(theta), -math.sin(theta)],
                      [0, math.sin(theta), math.cos(theta)]])


def Ry(theta):
    theta = math.radians(theta)
    return np.matrix([[math.cos(theta), 0, math.sin(theta)],
                     [0, 1, 0],
                     [-math.sin(theta), 0, math.cos(theta)]])


def Rz(theta):
    theta = math.radians(theta)
    return np.matrix([[math.cos(theta), -math.sin(theta), 0],
                      [math.sin(theta), math.cos(theta), 0],
                      [0, 0, 1]])


def get_XYZ(points):
    X = [x_ for (x_, _, _, _) in points]
    Y = [y_ for (_, y_, _, _) in points]
    Z = [z_ for (_, _, z_, _) in points]
    return X, Y, Z


def draw_joints(ax, points, clr):
    pairs = [(0, 1), (1, 2), (2, 3), (3, 0),
             (4, 5), (5, 6), (6, 7), (7, 4),
             (0, 4), (1, 5), (2, 6), (3, 7)]
    for i, j in pairs:
        x1, y1, z1, _ = points[i]
        x2, y2, z2, _ = points[j]
        ax.plot([x1, x2], [y1, y2], [z1, z2], color=clr)


def update_plot(scale, theta_x, theta_y, theta_z, translation_x, translation_y, translation_z):
    rotation = Rz(theta_z) * Ry(theta_y) * Rx(theta_x)
    rotation = scale * rotation
    translation = np.array([translation_x, translation_y, translation_z]).reshape(3, 1)

    # build the transformation matrix (M)
    zeros = np.zeros((1, 3))
    ones = np.ones((1, 1))
    Mt = np.hstack((rotation, translation))
    Mb = np.hstack((zeros, ones))
    M = np.vstack((Mt, Mb))

    # Transfer points
    points_transformed = np.matmul(M, points.T).T
    points_transformed = np.asarray(points_transformed)

    # Clear previous plot
    ax.cla()

    # draw points and transformed points
    XYZ = get_XYZ(points=points)
    transformed_XYZ = get_XYZ(points=points_transformed)

    ax.scatter(*XYZ, c='r', marker='o')
    draw_joints(ax, points, 'r')

    ax.scatter(*transformed_XYZ, c='b', marker='o')
    draw_joints(ax, points_transformed, 'b')

    # Set labels
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    # Set axis limits
    ax.set_xlim([0, 10])
    ax.set_ylim([0, 10])
    ax.set_zlim([0, 10])

    # Set specific view angle (elevation, azimuth)
    ax.view_init(elev=20, azim=45)

    # Draw canvas
    canvas.draw()


# Sample 3D points
points = []
points.append([0, 0, 0, 1])
points.append([1, 0, 0, 1])
points.append([1, 2, 0, 1])
points.append([0, 2, 0, 1])
points.append([0, 0, 3, 1])
points.append([1, 0, 3, 1])
points.append([1, 2, 3, 1])
points.append([0, 2, 3, 1])
points = np.array(points)

# Set initial parameters
initial_params = {'scale': 1, 'theta_x': 45, 'theta_y': 45, 'theta_z': 45,
                  'translation_x': 0, 'translation_y': 0, 'translation_z': 0}

# Create main window
root = tk.Tk()
root.title("3D Transformation Visualization")

# Create frame for sliders
frame = ttk.Frame(root, padding="10")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create sliders
sliders = {}
for i, param in enumerate(initial_params.keys()):
    ttk.Label(frame, text=param).grid(column=0, row=i, padx=5, pady=5, sticky=tk.W)
    sliders[param] = ttk.Scale(frame, from_=0, to=360, orient=tk.HORIZONTAL, length=200)
    sliders[param].set(initial_params[param])
    sliders[param].grid(column=1, row=i, padx=5, pady=5)

# Create button to update plot
update_button = ttk.Button(root, text="Update Plot", command=lambda: update_plot(
    sliders['scale'].get(),
    sliders['theta_x'].get(),
    sliders['theta_y'].get(),
    sliders['theta_z'].get(),
    sliders['translation_x'].get(),
    sliders['translation_y'].get(),
    sliders['translation_z'].get()
))

update_button.grid(column=0, row=1, pady=10)

# Create Matplotlib figure and canvas
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=1, row=0, rowspan=2, padx=10, pady=10)

# Initial plot
update_plot(**initial_params)

# Run the Tkinter event loop
root.mainloop()
