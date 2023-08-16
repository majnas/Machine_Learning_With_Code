import math
import numpy as np
from filterpy.kalman import KalmanFilter
import matplotlib.pyplot as plt


# Define a function to initialize the Kalman Filter
def get_kf(x, dt, noise_std):
    # Kalman filter setup
    kf = KalmanFilter(dim_x=4, dim_z=2)
    kf.x = np.array(x).reshape(4,1)  # Initial state [x, vx, y, vy]
    kf.P *= 1.0  # Covariance matrix
    kf.R = np.diag([noise_std**2, noise_std**2])  # Measurement noise covariance
    kf.Q = np.eye(4) * 0.01  # Process noise covariance

    # x_new  = x + vx * dt             + 0.5*dt*dt * gx 
    # vx_new =     vx                  + dt * gx 
    # y_new  =             y + vy * dt                  + 0.5*dt*dt * gy 
    # vy_new =                 vy                       + dt * gy
    kf.F = np.array([[1, dt,  0,  0],
                     [0,  1,  0,  0],
                     [0,  0,  1, dt],
                     [0,  0,  0,  1]])

    # Mesuring only x and y 
    kf.H = np.array([[1, 0, 0, 0],
                     [0, 0, 1, 0]])
    return kf

def main():
    # Constants
    gx = 0
    gy = -9.8  # Acceleration due to gravity

    # Initial conditions
    x0 = 0
    y0 = 30
    v0 = 20  # Initial velocity
    alpha = np.radians(60)  # Shooting angle in radians
    vx0 = v0 * math.cos(alpha)
    vy0 = v0 * math.sin(alpha)

    # Time settings
    t_start = 0
    t_end = 10
    n_steps = 30
    dt = (t_end - t_start) / n_steps  # Time step
    t = np.linspace(t_start, t_end, n_steps)

    # Generate ground truth trajectory
    x = x0 + vx0 * t + 0.5 * gx * t * t
    y = y0 + vy0 * t + 0.5 * gy * t * t

    # Add random noise to x and y to simulate measurements
    np.random.seed(0)  # For reproducibility
    noise_std = 1.0
    x_obs = x + np.random.normal(0, noise_std, n_steps)
    y_obs = y + np.random.normal(0, noise_std, n_steps)

    kf1 = get_kf([x0, vx0, y0, vy0], dt, noise_std)
    kf2 = get_kf([x0, vx0, y0, vy0], dt, noise_std)

    # Perform Kalman filtering
    filtered_state_means_1 = []
    filtered_state_means_2 = []
    u = np.array([[gx], 
                  [gy]]).reshape(2,1)

    B = np.array([[0.5*dt*dt, 0],
                [dt,        0],
                [0, 0.5*dt*dt],
                [0,        dt]]).reshape(4,2)
    for obs in zip(x_obs, y_obs):
        kf1.predict()
        kf1.update(obs)
        filtered_state_means_1.append(kf1.x)

        kf2.predict(u=u, B=B)
        kf2.update(obs)
        filtered_state_means_2.append(kf2.x)

    filtered_state_means_1 = np.array(filtered_state_means_1)
    filtered_state_means_2 = np.array(filtered_state_means_2)

    # Plotting the results
    plt.figure(figsize=(10, 6))

    # Plot Ground Truth
    plt.plot(x, y, label='Ground Truth', color='black')

    # Plot Noisy Measurements
    plt.plot(x_obs, y_obs, label='Noisy Measurements', marker='o', linestyle='None', color='red')

    # Plot Filtered Estimate 1
    plt.plot(filtered_state_means_1[:, 0], filtered_state_means_1[:, 2], label='Filtered Estimate 1', marker='o', color='green')

    # Plot Filtered Estimate 2
    plt.plot(filtered_state_means_2[:, 0], filtered_state_means_2[:, 2], label='Filtered Estimate 2', marker='o', color='blue')

    # Add labels and legend
    plt.legend()
    plt.title('Kalman Filter for Ball Trajectory Estimation with Noisy Observations')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()

