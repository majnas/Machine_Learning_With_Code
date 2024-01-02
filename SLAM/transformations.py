import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math


def Rx(theta):
	return np.matrix([[ 1, 0           , 0           ],
										[ 0, math.cos(theta),-math.sin(theta)],
										[ 0, math.sin(theta), math.cos(theta)]])
 
def Ry(theta):
	return np.matrix([[ math.cos(theta), 0, math.sin(theta)],
										[ 0           , 1, 0           ],
										[-math.sin(theta), 0, math.cos(theta)]])
 
def Rz(theta):
	return np.matrix([[ math.cos(theta), -math.sin(theta), 0 ],
										[ math.sin(theta), math.cos(theta) , 0 ],
										[ 0           , 0            , 1 ]])

def get_XYZ(points):
	X = [x_ for (x_,_,_,_) in points]
	Y = [y_ for (_,y_,_,_) in points]
	Z = [z_ for (_,_,z_,_) in points]
	return X, Y, Z

def draw_joints(ax, points, clr):
	pairs = [(0,1),(1,2),(2,3),(3,0),
			(4,5),(5,6),(6,7),(7,4),
			(0,4),(1,5),(2,6),(3,7)]
	for i,j in pairs:
		x1, y1, z1, _ = points[i]
		x2, y2, z2, _ = points[j]
		ax.plot([x1, x2], [y1, y2], [z1, z2], color=clr)

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


scale = 2
# rotation = Rz(0) * Ry(0) * Rx(0)
rotation = np.eye(3)
rotation = scale * rotation

# translation = np.array([0.5, 0.5, 0.5]).reshape(3, 1)
translation = np.zeros((3, 1))

zeros = np.zeros((1, 3))
ones = np.ones((1,1))
Mt = np.hstack((rotation, translation))
Mb = np.hstack((zeros, ones))
M = np.vstack((Mt, Mb))

print(M, M.shape, points.T.shape)

points_transformed = np.matmul(M, points.T).T
print("points_transformed", points_transformed)

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Scatter plot
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

# Show the plot
plt.show()

