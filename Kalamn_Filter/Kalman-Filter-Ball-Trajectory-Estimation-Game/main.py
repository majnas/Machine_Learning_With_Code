import time
from typing import List, Tuple
import pymunk
import pygame
import numpy as np
from filterpy.kalman import KalmanFilter

# Initialize pygame and pymunk
GOLDEN_RATIO = (1 + 5**0.5) / 2
SCREEN_HEIGHT = 900
SCREEN_WIDTH = SCREEN_HEIGHT * GOLDEN_RATIO
NOISE_STD = 20.0
COLOR_LINE = (255, 255, 0)
COLOR_GT = (0, 0, 0 )
COLOR_OBS = (255, 0, 0)
COLOR_PRED = (0, 255, 0)

# Update physics simulation
dt = 1 / 10.0
np.random.seed(0)  # For reproducibility

GX = 0
GY = -981
BALL_RADIUS = 10

# Time settings
T_START = 0
T_END = 5
N_STEPS = 50
DT = (T_END - T_START) / N_STEPS  # Time step


class Projectile:
    def __init__(self, initial_state: List[int]) -> None:
        self.x0, self.vx0, self.y0, self.vy0 = initial_state
        self.gt()
        self.obs()
        self.kf = self.get_kf(initial_state, DT, NOISE_STD)
        self.pred()

    # Define a function to initialize the Kalman Filter
    def get_kf(self, x, dt, noise_std):
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

        kf.B = np.array([[0.5*dt*dt, 0],
                         [dt,        0],
                         [0, 0.5*dt*dt],
                         [0,        dt]]).reshape(4,2)
        return kf
    
    def gt(self):
        # Time settings
        t = np.linspace(T_START, T_END, N_STEPS)
        # Generate ground truth trajectory
        self.x = self.x0 + self.vx0 * t + 0.5 * GX * t * t
        self.y = self.y0 + self.vy0 * t + 0.5 * GY * t * t

    def obs(self):
        # Get actual location of projetile and add noise as observation
        self.x_obs = self.x + np.random.normal(0, NOISE_STD, self.x.shape)
        self.y_obs = self.y + np.random.normal(0, NOISE_STD, self.x.shape)

    def pred(self):
        self.x_pred = []
        self.y_pred = []
        u = np.array(space.gravity).reshape(2,1)
        for i in range(N_STEPS):
            self.kf.predict(u=u)
            # projectile.kf.update((obs_pos[0], obs_pos[1]))
            self.kf.update((self.x_obs[i], SCREEN_HEIGHT - self.y_obs[i]))
            self.x_pred.append(self.kf.x[0][0])
            self.y_pred.append(self.kf.x[2][0])

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, -981)

# Create the ground
ground = pymunk.Segment(space.static_body, (0, 100), (SCREEN_WIDTH, 100), 5)
space.add(ground)

# List to store projectiles
projectiles:List[Projectile] = []

# Variables for tracking mouse button events
mouse_down_pos = ()
mouse_up_pos = ()
mouse_displacement = 0
mouse_held = False

# Main loop
running = True
midx = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_held = True
            mouse_down_pos = event.pos
        elif event.type == pygame.KEYDOWN:  # Check for key press event
            if event.key == pygame.K_r:  # Check if the pressed key is "r"
                projectiles.clear()  # Clear the projectiles list
            elif event.key == pygame.K_q:  # Check if the pressed key is "q"
                running = False  # Set running to False to exit the loop
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_held = False
            mouse_up_pos = event.pos

            # Calculate mouse displacement
            mouse_displacement_vector = ((mouse_down_pos[0]-mouse_up_pos[0]), (mouse_up_pos[1]-mouse_down_pos[1]))
            # mouse_displacement_vector = (120, 120)
            
            # Create a ball at the mouse `click position
            start_pos_x = mouse_down_pos[0]
            # start_pos_y = mouse_down_pos[1]
            start_pos_y = SCREEN_HEIGHT - mouse_down_pos[1]

            # Calculate shoot_speed based on time held down
            velocity_factor = 5.0  # Adjust this factor to control speed increase rate
            # Apply velocity to the ball in the direction of the shooting segment

            #? Instantiate a Kalman-Filter to track the projectile
            initial_state = [start_pos_x, 
                             mouse_displacement_vector[0] * velocity_factor, 
                             start_pos_y, 
                             mouse_displacement_vector[1] * velocity_factor]
            projectiles.append(Projectile(initial_state=initial_state))


    screen.fill((255, 255, 255))
    if mouse_held:
        mouse_pos = pygame.mouse.get_pos()
        # draw shooting segment 
        pygame.draw.line(screen, COLOR_LINE, mouse_down_pos, mouse_pos, 5)

    # space.step(DT)

    # Draw the ground and projectiles
    pygame.draw.line(screen, (0, 0, 0), (0, SCREEN_HEIGHT-100), (SCREEN_WIDTH, SCREEN_HEIGHT-100), 5)
    for projectile in projectiles:
        for i in range(N_STEPS-1):
            gt_pos_i = (int(projectile.x[i]), int(SCREEN_HEIGHT - projectile.y[i]))
            gt_pos_j = (int(projectile.x[i+1]), int(SCREEN_HEIGHT - projectile.y[i+1]))
            pygame.draw.circle(screen, COLOR_GT, gt_pos_i, BALL_RADIUS)
            pygame.draw.line(screen, COLOR_GT, gt_pos_i, gt_pos_j, 3)

            # Get actual location of projetile and add noise as observation
            obs_pos_i = (int(projectile.x_obs[i]), int(SCREEN_HEIGHT - projectile.y_obs[i]))
            obs_pos_j = (int(projectile.x_obs[i+1]), int(SCREEN_HEIGHT - projectile.y_obs[i+1]))
            pygame.draw.circle(screen, COLOR_OBS, obs_pos_i, BALL_RADIUS)
            # pygame.draw.line(screen, COLOR_GT, obs_pos_i, obs_pos_j, 3)

            pred_pos_i = (int(projectile.x_pred[i]), int(SCREEN_HEIGHT - projectile.y_pred[i]))
            pred_pos_j = (int(projectile.x_pred[i+1]), int(SCREEN_HEIGHT - projectile.y_pred[i+1]))
            pygame.draw.circle(screen, COLOR_PRED, pred_pos_i, BALL_RADIUS)
            pygame.draw.line(screen, COLOR_GT, pred_pos_i, pred_pos_j, 2)

    pygame.display.flip()
    clock.tick(50)

pygame.quit()