import math
import numpy as np
from filterpy.kalman import KalmanFilter
import matplotlib.pyplot as plt
import matplotlib.animation as animation


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
    noise_std = 5.0
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

    # Create a list to store Kalman gain values
    kalman_gain_history = []
    for obs in zip(x_obs, y_obs):
        kf1.predict()
        kf1.update(obs)
        filtered_state_means_1.append(kf1.x)

        kf2.predict(u=u, B=B)
        kf2.update(obs)
        filtered_state_means_2.append(kf2.x)

        # Append the Kalman gain matrix to the history list
        kalman_gain_history.append(kf2.K)

    filtered_state_means_1 = np.array(filtered_state_means_1)
    filtered_state_means_2 = np.array(filtered_state_means_2)


    # Create a figure and axis for the animation
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title('Kalman Filter for Ball Trajectory Estimation with Noisy Observations')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.grid(True)

    # Set initial y-axis limits based on the ground truth trajectory
    ax.set_ylim(min(y) - 10, max(y) + 50)

    # Plot Ground Truth
    ax.plot(x, y, label='Ground Truth', color='black')

    # Initialize empty lines for each plot
    ground_truth_line, = ax.plot([], [], color='black')
    noisy_measurements_line, = ax.plot([], [], marker='o', linestyle='None', color='red', label='Noisy Measurements')
    filtered_est1_line, = ax.plot([], [], marker='o', color='green', label='Filtered Estimate 1')
    filtered_est2_line, = ax.plot([], [], marker='o', color='blue', label='Filtered Estimate 2')

    # Set up the animation function
    def animate(i):
        ground_truth_line.set_data(x[i], y[i])
        noisy_measurements_line.set_data(x_obs[:i+1], y_obs[:i+1])
        filtered_est1_line.set_data(filtered_state_means_1[:i+1, 0], filtered_state_means_1[:i+1, 2])
        filtered_est2_line.set_data(filtered_state_means_2[:i+1, 0], filtered_state_means_2[:i+1, 2])
        
        ax.legend()

    # Create the animation
    ani = animation.FuncAnimation(fig, animate, frames=n_steps, interval=200)

    # Save the animation as a GIF file
    ani.save('trajectory_estimation_animation.gif', writer='pillow')
    # Display the animation
    plt.show()

    # Convert the Kalman gain history list into a NumPy array
    kalman_gain_history = np.array(kalman_gain_history)

    # Plotting the Kalman gain values for each component (x and y)
    plt.figure(figsize=(10, 6))
    plt.plot(t, kalman_gain_history[:, 0, 0], label='Kalman Gain (x)', marker='o', color='green', linestyle='None')
    plt.plot(t, kalman_gain_history[:, 1, 0], label='Kalman Gain (vx)', marker='o', color='red', linestyle='None')
    plt.plot(t, kalman_gain_history[:, 2, 1], label='Kalman Gain (y)', color='black')
    plt.plot(t, kalman_gain_history[:, 3, 1], label='Kalman Gain (vy)')

    # Add labels and legend
    plt.legend()
    plt.title('Kalman Gain Visualization')
    plt.xlabel('Time')
    plt.ylabel('Kalman Gain')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()

