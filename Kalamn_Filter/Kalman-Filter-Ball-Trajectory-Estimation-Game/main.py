from typing import List, Tuple
import pymunk
import pygame
import math
import numpy as np
from filterpy.kalman import KalmanFilter

# Initialize pygame and pymunk
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
NOISE_STD = 20.0
COLOR_LINE = (255, 255, 0)
COLOR_GT = (0, 0, 0 )
COLOR_OBS = (255, 0, 0)
COLOR_PRED = (0, 255, 0)

# Update physics simulation
dt = 1 / 10.0
np.random.seed(0)  # For reproducibility

class Step:
    def __init__(self, gt_pos: tuple, obs_pos: tuple, pred_pos: tuple) -> None:
        self.gt_pos = gt_pos
        self.obs_pos = obs_pos
        self.pred_pos = pred_pos

    def __str__(self) -> str:
        return f"gt:{self.gt_pos} obs:{self.obs_pos} pred:{self.pred_pos}"


class Projectile:
    def __init__(self, body:pymunk.body.Body, kf:KalmanFilter) -> None:
        self.body = body
        self.kf = kf


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

    kf.B = np.array([[0.5*dt*dt, 0],
                     [dt,        0],
                     [0, 0.5*dt*dt],
                     [0,        dt]]).reshape(4,2)

    return kf



x0 = 123
y0 = 224
v0 = 100  # Initial velocity
vx0 = 120 * 5
vy0 = 120 * 5
gx = 0
gy = -981

# Time settings
t_start = 0
t_end = 5
n_steps = 50
dt = (t_end - t_start) / n_steps  # Time step
t = np.linspace(t_start, t_end, n_steps)

# Generate ground truth trajectory
xx = x0 + vx0 * t + 0.5 * gx * t * t
yy = y0 + vy0 * t + 0.5 * gy * t * t

# for (x_, y_) in zip(x,y):
#     print(x_, y_)

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

history:List[List[Step]] = []

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
                history.clear()
            elif event.key == pygame.K_q:  # Check if the pressed key is "q"
                running = False  # Set running to False to exit the loop
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_held = False
            mouse_up_pos = event.pos

            # Calculate mouse displacement
            mouse_displacement_vector = ((mouse_down_pos[0]-mouse_up_pos[0]), (mouse_up_pos[1]-mouse_down_pos[1]))
            mouse_displacement_vector = (120, 120)
            
            # Create a ball at the mouse `click position
            start_pos_x = mouse_down_pos[0]
            start_pos_y = SCREEN_HEIGHT - mouse_down_pos[1]

            start_pos_x = x0
            start_pos_y = y0

            ball_radius = 10
            ball_mass = 1
            ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
            ball_body = pymunk.Body(ball_mass, ball_moment)
            ball_body.position = (start_pos_x, start_pos_y)
            ball_shape = pymunk.Circle(ball_body, ball_radius)
            space.add(ball_body, ball_shape)

            # Calculate shoot_speed based on time held down
            velocity_factor = 5.0  # Adjust this factor to control speed increase rate
            # Apply velocity to the ball in the direction of the shooting segment
            ball_body.velocity = (mouse_displacement_vector[0] * velocity_factor, mouse_displacement_vector[1] * velocity_factor)


            #? Instantiate a Kalman-Filter to track the projectile
            x = [start_pos_x, ball_body.velocity[0], start_pos_y, ball_body.velocity[1]]
            kf = get_kf(x, dt, NOISE_STD)

            projectiles.append(Projectile(body=ball_body, kf=kf))


    screen.fill((255, 255, 255))

    # math
    if midx < 20:
        pos = (xx[midx], SCREEN_HEIGHT-yy[midx])
        pygame.draw.circle(screen, COLOR_PRED, pos, 10)
    else:
        midx = 0
    midx += 1
    print(midx)


    if mouse_held:
        mouse_pos = pygame.mouse.get_pos()
        # draw shooting segment 
        pygame.draw.line(screen, COLOR_LINE, mouse_down_pos, mouse_pos, 5)

    for history_step in history:
        for step in history_step:
            pygame.draw.circle(screen, COLOR_GT, step.gt_pos, ball_radius)
            pygame.draw.circle(screen, COLOR_OBS, step.obs_pos, ball_radius)
            pygame.draw.circle(screen, COLOR_PRED, step.pred_pos, ball_radius)

    space.step(dt)

    # Draw the ground and projectiles
    pygame.draw.line(screen, (0, 0, 0), (0, SCREEN_HEIGHT-100), (SCREEN_WIDTH, SCREEN_HEIGHT-100), 5)
    history_step:List[Step] = []
    for projectile in projectiles:
        gt_pos = projectile.body.position
        gt_pos = (int(gt_pos.x), int(SCREEN_HEIGHT - gt_pos.y))
        pygame.draw.circle(screen, COLOR_GT, gt_pos, ball_radius)

        # Get actual location of projetile and add noise as observation
        obs_pos = gt_pos + np.random.normal(0, NOISE_STD, 2)
        pygame.draw.circle(screen, COLOR_OBS, obs_pos, ball_radius)


        u = np.array(space.gravity).reshape(2,1)

        projectile.kf.predict(u=u)
        projectile.kf.update((obs_pos[0], SCREEN_HEIGHT - obs_pos[1]))
        pred_pos = (projectile.kf.x[0][0], SCREEN_HEIGHT - projectile.kf.x[2][0])

        pygame.draw.circle(screen, COLOR_PRED, pred_pos, ball_radius)

        if (gt_pos[0] > SCREEN_WIDTH) or (gt_pos[1] > SCREEN_HEIGHT):
            continue
        step = Step(gt_pos, obs_pos, pred_pos)
        history_step.append(step)

    history.append(history_step)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
print(len(history))