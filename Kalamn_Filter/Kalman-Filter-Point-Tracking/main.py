import math
import numpy as np
from filterpy.kalman import KalmanFilter
import matplotlib.pyplot as plt

# Constants
g = -9.8  # Acceleration due to gravity

# Initial conditions
x0 = 0
y0 = 30
v0 = 20  # Initial velocity
alpha = np.radians(60)  # Shooting angle in radians
vx0 = v0 * math.cos(alpha)
vy0 = v0 * math.sin(alpha)

t_start = 0
t_end = 5
n_steps = 100
dt = 1 / n_steps  # Time step
t = np.linspace(t_start, t_end, n_steps)
x = vx0 * t
y = y0 + vy0 * t + 0.5 * g * t * t

# Add random noise to x and y
np.random.seed(0)  # For reproducibility
noise_std = 2.0
x_obs = x + np.random.normal(0, noise_std, n_steps)
y_obs = y + np.random.normal(0, noise_std, n_steps)

# Kalman filter setup
kf = KalmanFilter(dim_x=4, dim_z=2)
kf.x = np.array([x0, vx0, y0, vy0])  # Initial state [x, vx, y, vy]
kf.P *= 1.0  # Covariance matrix
kf.R = np.diag([noise_std**2, noise_std**2])  # Measurement noise covariance
kf.Q = np.eye(4) * 0.01  # Process noise covariance
kf.F = np.array([[1, dt, 0, 0],
                 [0, 1, 0, 0],
                 [0, 0, 1, dt],
                 [0, 0, 0, 1]])
kf.H = np.array([[1, 0, 0, 0],
                 [0, 0, 1, 0]])

# Perform Kalman filtering
filtered_state_means = []
for obs in zip(x_obs, y_obs):
    kf.predict()
    kf.update(obs)
    filtered_state_means.append(kf.x)

filtered_state_means = np.array(filtered_state_means)

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='GT', color='red')
plt.plot(x_obs, y_obs, label='Noisy Measurements', marker='o', linestyle='None')
plt.plot(filtered_state_means[:, 0], filtered_state_means[:, 2], label='Filtered', color='green')
plt.legend()
plt.title('Kalman Filter for Ball Trajectory Estimation with Noisy Observations')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.show()
