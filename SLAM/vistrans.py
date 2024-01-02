import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
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


# Function to update the matrix display
def update_matrix_display():
    try:
        scale = sliders['scale'].get()
        theta_x = sliders['theta_x'].get()
        theta_y = sliders['theta_y'].get()
        theta_z = sliders['theta_z'].get()
        translation_x = sliders['translation_x'].get()
        translation_y = sliders['translation_y'].get()
        translation_z = sliders['translation_z'].get()
    except:
        return

    rotation = Rz(theta_z) * Ry(theta_y) * Rx(theta_x)
    rotation = scale * rotation
    translation = np.array([translation_x, translation_y, translation_z]).reshape(3, 1)

    # Build the transformation matrix (M)
    zeros = np.zeros((1, 3))
    ones = np.ones((1, 1))
    Mt = np.hstack((rotation, translation))
    Mb = np.hstack((zeros, ones))
    M = np.vstack((Mt, Mb))

    # Format the display text with fixed positions
    display_text = f"[[{M[0, 0]:>2.3f}   {M[0, 1]:>2.3f}   {M[0, 2]:>2.3f}   {M[0, 3]:>2.3f}] \n" \
                   f" [{M[1, 0]:>2.3f}   {M[1, 1]:>2.3f}   {M[1, 2]:>2.3f}   {M[1, 3]:>2.3f}] \n" \
                   f" [{M[2, 0]:>2.3f}   {M[2, 1]:>2.3f}   {M[2, 2]:>2.3f}   {M[2, 3]:>2.3f}] \n" \
                   f" [{M[3, 0]:>2.3f}   {M[3, 1]:>2.3f}   {M[3, 2]:>2.3f}   {M[3, 3]:>2.3f}]]\n"

    # Update the matrix display
    matrix_var.set(display_text)


def update_plot(val):
    # print("val", val)
    # print("sliders", sliders)
    update_matrix_display()

    try:
        scale = sliders['scale'].get()
        theta_x = sliders['theta_x'].get()
        theta_y = sliders['theta_y'].get()
        theta_z = sliders['theta_z'].get()
        translation_x = sliders['translation_x'].get()
        translation_y = sliders['translation_y'].get()
        translation_z = sliders['translation_z'].get()
    except:
        return

    print("scale", scale)
    print("theta_x", theta_x)
    print("theta_y", theta_y)
    print("theta_z", theta_z)
    print("translation_x", translation_x)
    print("translation_y", translation_y)
    print("translation_z", translation_z)

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
    ax.set_xlim([0, 30])
    ax.set_ylim([0, 30])
    ax.set_zlim([0, 30])

    # Set specific view angle (elevation, azimuth)
    ax.view_init(elev=20, azim=45)

    # Draw canvas
    canvas.draw()


# Sample 3D points
points = np.array([
    [0, 0, 0, 1], [1, 0, 0, 1], [1, 2, 0, 1], [0, 2, 0, 1],
    [0, 0, 3, 1], [1, 0, 3, 1], [1, 2, 3, 1], [0, 2, 3, 1]
])

# Set initial parameters
initial_params = {'scale': 2, 'theta_x': 0, 'theta_y': 0, 'theta_z': 0,
                  'translation_x': 0, 'translation_y': 0, 'translation_z': 0}

# Create main window
root = tk.Tk()
root.title("3D Transformation Visualization")

# Set the size of the Tkinter window
root.geometry("1200x800")  # Adjust the dimensions as needed

# Create frame for sliders
frame = ttk.Frame(root, padding="10")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create Matplotlib figure and canvas with a larger figsize
fig = plt.figure(figsize=(10, 8))  # Adjust the dimensions as needed
ax = fig.add_subplot(111, projection='3d')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=1, row=0, rowspan=2, padx=10, pady=10)

# Create a label to display the transformation matrix
matrix_label = ttk.Label(frame, text="Transformation Matrix (M):")
matrix_label.grid(column=0, row=len(initial_params) + 1, columnspan=2, pady=10)

# Create StringVar to update matrix display dynamically
matrix_var = StringVar()
matrix_text = ttk.Label(frame, textvariable=matrix_var)
matrix_text.grid(column=0, row=len(initial_params) + 2, columnspan=2, pady=5)

# Create sliders
sliders = {}
for i, param in enumerate(initial_params.keys()):
    to_ = 360 if 'theta' in param else 100
    to_ = 20 if 'scale' in param else to_
    ttk.Label(frame, text=param).grid(column=0, row=i, padx=5, pady=5, sticky=tk.W)
    sliders[param] = ttk.Scale(frame, from_=0, to=to_, orient=tk.HORIZONTAL, length=200, command=update_plot)
    sliders[param].set(initial_params[param])
    sliders[param].grid(column=1, row=i, padx=5, pady=5)

# Initial plot
update_plot(0)

# Update the matrix display initially
update_matrix_display()

# Run the Tkinter event loop
root.mainloop()
