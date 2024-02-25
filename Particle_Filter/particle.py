import pygame
import random
import numpy as np
from board import Sensors
from icecream import ic

class Particle(object):
    """
    Class representing a particle in the particle filter.
    """
    def __init__(self, x, y, board, heading = None, weight = 1.0, sensor_limit = None, noisy = False):
        """
        Initialize a particle.

        Args:
            x (float): The x-coordinate of the particle's position.
            y (float): The y-coordinate of the particle's position.
            board (Board): The board on which the particle exists.
            heading (float, optional): The heading angle of the particle in degrees. Defaults to None.
            weight (float, optional): The weight of the particle. Defaults to 1.0.
            sensor_limit (int, optional): The limit for sensor readings. Defaults to None.
            noisy (bool, optional): Whether the particle's initial position and heading should be noisy. Defaults to False.
        """        
        if heading is None:
            heading = np.random.uniform(0,360)

        self.x = x
        self.y = y
        self.heading = heading
        self.weight = weight
        self.board = board
        self.sensor_limit = sensor_limit

        if noisy:
            std = max(self.board.cell_size, self.board.cell_size) * 0.2
            self.x = self.x + np.random.normal(0, std)
            self.y = self.y + np.random.normal(0, std)
            self.heading = self.heading + np.random.normal(0, 360 * 0.05)

    def is_valid(self, x = None, y = None):
        """
        Check if a given position is valid on the board.

        Args:
            x (float, optional): The x-coordinate of the position. Defaults to None.
            y (float, optional): The y-coordinate of the position. Defaults to None.

        Returns:
            bool: True if the position is valid, False otherwise.
        """
        if x is None or y is None:
            x = self.x
            y = self.y
        if x < 0 or y < 0:
            return False
        if x >= self.board.width or y >= self.board.height:
            return False
        col = int(x / self.board.cell_size)
        row = int(y / self.board.cell_size)
        return self.board.board[row, col] == 0

    @property
    def state(self):
        """
        Get the state of the particle.

        Returns:
            tuple: A tuple containing the x-coordinate, y-coordinate, and heading angle of the particle.
        """
        return (self.x, self.y, self.heading)

    @staticmethod
    def generate_blue_colors():
        """
        Generate a range of blue colors from light blue to dark blue.

        Returns:
            list: A list of RGB tuples representing the range of blue colors.
        """
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

    def read_sensor(self)-> Sensors:
        """
        Read sensor values from the particle's current position on the board.

        Returns:
            Sensors: The sensor readings.
        """
        sensors: Sensors = self.board.read_sensors(self.x, self.y)
        sensors.apply_limit(sensor_limit=self.sensor_limit)
        return sensors

    # TODO consider crossing over walls
    def try_move(self, speed):
        """
        Attempt to move the particle in the direction of its heading.

        Args:
            speed (float): The speed of the particle.

        Returns:
            bool: True if the movement is successful (i.e., the new position is valid), False otherwise.
        """
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

    def show(self, screen, color = None, radius: int = 5):
        """
        Draw the particle on the screen.

        Args:
            screen (pygame.Surface): The surface on which to draw the particle.
            color (tuple, optional): The color of the particle. Defaults to None.
            radius (int, optional): The radius of the particle. Defaults to 5.
        """
        if color is None:
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
    """
    Class representing a robot in the particle filter.
    """
    def __init__(self, x, y, board, heading = None, speed = 1.0, sensor_limit = None, noisy = True):
        """
        Initialize a robot.

        Args:
            x (float): The x-coordinate of the robot's position.
            y (float): The y-coordinate of the robot's position.
            board (Board): The board on which the robot exists.
            heading (float, optional): The heading angle of the robot in degrees. Defaults to None.
            speed (float, optional): The speed of the robot. Defaults to 1.0.
            sensor_limit (int, optional): The limit for sensor readings. Defaults to None.
            noisy (bool, optional): Whether the robot's sensor readings should be noisy. Defaults to True.
        """
        super(Robot, self).__init__(x = x, y = y, board = board, heading = heading, sensor_limit = sensor_limit, noisy = noisy)
        self.step_count = 0
        self.noisy = noisy
        self.time_step = 0
        self.speed = speed        

    def read_sensor(self)-> Sensors:
        """
        Read sensor values from the robot's current position on the board.

        Returns:
            Sensors: The sensor readings.
        """
        # Robot has error in reading the sensor while particles do not.
        sensors = super(Robot, self).read_sensor()
        if self.noisy:
            sensors.add_noise()
        return sensors

    def move(self):
        """
        Move the robot in the direction of its heading.
        """
        while True:
            self.time_step += 1
            if self.try_move(speed=self.speed):
                break
            # if hit the wall pick random heading
            self.heading = np.random.uniform(0, 360)


class Resampling():
    """
    Class representing the resampling step of the particle filter.
    """
    def __init__(self, particles) -> None:
        """
        Initialize the Resampling object.

        Args:
            particles (list): A list of particles.
        """
        self.particles = particles
        weights = [particle.weight for particle in particles]
        total_weight = sum(weights)
        self.probabilities = [weight / total_weight for weight in weights]

    def get_particles(self):
        """
        Perform the resampling step of the particle filter.

        Returns:
            list: A list of resampled particles.
        """
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