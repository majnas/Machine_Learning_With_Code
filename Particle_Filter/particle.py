import pygame
import random
import sys
import math
import numpy as np
from board import Sensors
from icecream import ic

class Particle(object):
    def __init__(self, x, y, board, heading = None, weight = 1.0, sensor_limit = None, noisy = False):
        if heading is None:
            heading = np.random.uniform(0,360)

        self.x = x
        self.y = y
        self.heading = heading
        self.weight = weight
        self.board = board
        self.sensor_limit = sensor_limit

        if noisy:
            # std = max(self.board.grid_height, self.board.grid_width) * 0.2
            std = max(self.board.cell_size, self.board.cell_size) * 0.2
            # self.x = self.add_noise(x = self.x, std = std)
            # self.y = self.add_noise(x = self.y, std = std)
            # self.heading = self.add_noise(x = self.heading, std = 360 * 0.05)
            self.x = self.x + np.random.normal(0, std)
            self.y = self.y + np.random.normal(0, std)
            self.heading = self.heading + np.random.normal(0, 360 * 0.05)

        # self.is_valid = self.fix_invalid_particles()

    @property
    def is_valid(self):
        col = int(self.x / self.board.cell_size)
        row = int(self.y / self.board.cell_size)
        return self.board.board[row, col] == 0

    # def fix_invalid_particles(self):
    #     # Fix invalid particles
    #     if self.x < 0:
    #         self.x = 0
    #     if self.x > self.board.width:
    #         self.x = self.board.width * 0.9999
    #     if self.y < 0:
    #         self.y = 0
    #     if self.y > self.board.height:
    #         self.y = self.board.height * 0.9999
    #     self.heading = self.heading % 360

    @property
    def state(self):
        return (self.x, self.y, self.heading)

    # def add_noise(self, x, std):
    #     return x + np.random.normal(0, std)

    @staticmethod
    def generate_blue_colors():
        # Define the starting and ending RGB values for light blue and dark blue
        light_blue = (204, 229, 255)  # RGB for light blue
        dark_blue = (0, 51, 102)       # RGB for dark blue
        # Linearly interpolate between the light blue and dark blue colors
        blue_colors = []
        for i in range(100):
            # Interpolate the RGB values for blue component
            r = int(light_blue[0] + (dark_blue[0] - light_blue[0]) * (i / 99))
            g = int(light_blue[1] + (dark_blue[1] - light_blue[1]) * (i / 99))
            b = int(light_blue[2] + (dark_blue[2] - light_blue[2]) * (i / 99))
            # Append the interpolated color to the list
            blue_colors.append((r, g, b))
        return blue_colors

    def read_sensor(self):
        sensors: Sensors = self.board.read_sensors(self.x, self.y)
        sensors.apply_limit(sensor_limit=self.sensor_limit)

    #     heading = self.heading % 360

    #     # Remove the compass from particle
    #     if heading >= 45 and heading < 135:
    #         readings = readings
    #     elif heading >= 135 and heading < 225:
    #         readings = readings[-1:] + readings[:-1]
    #         #readings = [readings[3], readings[0], readings[1], readings[2]]
    #     elif heading >= 225 and heading < 315:
    #         readings = readings[-2:] + readings[:-2]
    #         #readings = [readings[2], readings[3], readings[0], readings[1]]
    #     else:
    #         readings = readings[-3:] + readings[:-3]
    #         #readings = [readings[1], readings[2], readings[3], readings[0]]

    #     if self.sensor_limit is not None:
    #         for i in range(len(readings)):
    #             if readings[i] > self.sensor_limit:
    #                 readings[i] = self.sensor_limit

    #     return readings
        return sensors

    # def try_move(self, speed, board, noisy = False):

    #     heading = self.heading
    #     heading_rad = np.radians(heading)

    #     dx = np.sin(heading_rad) * speed
    #     dy = np.cos(heading_rad) * speed

    #     x = self.x + dx
    #     y = self.y + dy

    #     gj1 = int(self.x // board.grid_width)
    #     gi1 = int(self.y // board.grid_height)
    #     gj2 = int(x // board.grid_width)
    #     gi2 = int(y // board.grid_height)

    #     # Check if the particle is still in the board
    #     if gi2 < 0 or gi2 >= board.num_rows or gj2 < 0 or gj2 >= board.num_cols:
    #         return False

    #     # Move in the same grid
    #     if gi1 == gi2 and gj1 == gj2:
    #         self.x = x
    #         self.y = y
    #         return True
    #     # Move across one grid vertically
    #     elif abs(gi1 - gi2) == 1 and abs(gj1 - gj2) == 0:
    #         if board.board[min(gi1, gi2), gj1] & 4 != 0:
    #             return False
    #         else:
    #             self.x = x
    #             self.y = y
    #             return True
    #     # Move across one grid horizonally
    #     elif abs(gi1 - gi2) == 0 and abs(gj1 - gj2) == 1:
    #         if board.board[gi1, min(gj1, gj2)] & 2 != 0:
    #             return False
    #         else:
    #             self.x = x
    #             self.y = y
    #             return True
    #     # Move across grids both vertically and horizonally
    #     elif abs(gi1 - gi2) == 1 and abs(gj1 - gj2) == 1:

    #         x0 = max(gj1, gj2) * board.grid_width
    #         y0 = (y - self.y) / (x - self.x) * (x0 - self.x) + self.y

    #         if board.board[int(y0 // board.grid_height), min(gj1, gj2)] & 2 != 0:
    #             return False

    #         y0 = max(gi1, gi2) * board.grid_height
    #         x0 = (x - self.x) / (y - self.y) * (y0 - self.y) + self.x

    #         if board.board[min(gi1, gi2), int(x0 // board.grid_width)] & 4 != 0:
    #             return False

    #         self.x = x
    #         self.y = y
    #         return True

    #     else:
    #         raise Exception('Unexpected collision detection.')

    def show(self, screen, color, radius: int = 5):
        # Generate 100 blue colors from light blue to dark blue
        blue_color_range = self.generate_blue_colors()
        color_idx = int(self.weight * 99)
        color = blue_color_range[color_idx]
        ic(color_idx, color)
        pygame.draw.circle(screen, color, (self.x, self.y), radius)


        # Calculate endpoint of the line
        heading_rad = np.radians(self.heading)
        dx = np.sin(heading_rad) * radius
        dy = np.cos(heading_rad) * radius
        endpoint_x = self.x + dx
        endpoint_y = self.y + dy

        # Draw the line from center to endpoint
        pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), (endpoint_x, endpoint_y), 2)



class Robot(Particle):
    def __init__(self, x, y, board, heading = None, speed = 1.0, sensor_limit = None, noisy = True):
        super(Robot, self).__init__(x = x, y = y, board = board, heading = heading, sensor_limit = sensor_limit, noisy = noisy)
        self.step_count = 0
        self.noisy = noisy
        self.time_step = 0
        self.speed = speed

    # def choose_random_direction(self):

    #     self.heading = np.random.uniform(0, 360)

    # def add_sensor_noise(self, x, z = 0.05):

    #     readings = list(x)

    #     for i in range(len(readings)):
    #         std = readings[i] * z / 2
    #         readings[i] = readings[i] + np.random.normal(0, std)

    #     return readings

    # def read_sensor(self, board):

    #     # Robot has error in reading the sensor while particles do not.

    #     readings = super(Robot, self).read_sensor(board = board)
    #     if self.noisy == True:
    #         readings = self.add_sensor_noise(x = readings)

    #     return readings

    # def move(self, board):
    #     while True:
    #         self.time_step += 1
    #         if self.try_move(speed = self.speed, board = board, noisy = False):
    #             break
    #         self.choose_random_direction()



class Resampling():
    def __init__(self, particles) -> None:
        self.particles = particles

        weights = [particle.weight for particle in particles]
        total_weight = sum(weights)
        self.probabilities = [weight / total_weight for weight in weights]

    def get_particles(self):
        new_particles = []
        while len(new_particles) <= len(self.particles):
            # Select a particle index using roulette wheel selection
            index = np.random.choice(len(self.particles), p=self.probabilities)
            # Create a new particle as a copy of the selected one
            new_particle = Particle(x=self.particles[index].x,
                                    y=self.particles[index].y,
                                    board=self.particles[index].board,
                                    heading=self.particles[index].heading,
                                    weight=self.particles[index].weight,
                                    sensor_limit=self.particles[index].sensor_limit,
                                    noisy=True)
            if new_particle.is_valid:
                new_particles.append(new_particle)

        return new_particles