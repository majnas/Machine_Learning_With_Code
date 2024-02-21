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

    def is_valid(self, x = None, y = None):
        if x is None or y is None:
            x = self.x
            y = self.y
        if x >= self.board.width or y >= self.board.height:
            return False
        col = int(x / self.board.cell_size)
        row = int(y / self.board.cell_size)
        return self.board.board[row, col] == 0

    @property
    def state(self):
        return (self.x, self.y, self.heading)

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
        return sensors

    # TODO consider crossing over walls
    def try_move(self, speed):
        heading = self.heading
        heading_rad = np.radians(heading)
        dx = np.sin(heading_rad) * speed
        dy = np.cos(heading_rad) * speed
        x = self.x + dx
        y = self.y + dy

        # Check if new location is valid
        is_valid = self.is_valid(x=x, y=y)
        if is_valid:
            self.x = x
            self.y = y
        return is_valid

    def show(self, screen, color, radius: int = 5):
        # Generate 100 blue colors from light blue to dark blue
        blue_color_range = self.generate_blue_colors()
        color_idx = int(self.weight * 99)
        color = blue_color_range[color_idx]
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

    def move(self):
        while True:
            self.time_step += 1
            if self.try_move(speed=self.speed):
                break

            # reflect your direction
            self.heading = (self.heading + 15) % 360
            # self.heading = np.random.uniform(0, 360)


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