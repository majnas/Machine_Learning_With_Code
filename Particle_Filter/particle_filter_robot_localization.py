import pygame
import random
import sys
import math
import time
import numpy as np
from typing import List

from board import Board, Sensors
from particle import Particle, Robot, Resampling

# Define colors
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Main function
def main():
    board_width = 800
    board_height = 600
    cell_size = 20
    num_particles = 100
    robot_speed = 10
    sensor_limit = 500

    pygame.init()
    screen = pygame.display.set_mode((board_width, board_height))
    pygame.display.set_caption("Particle Filter Turtle Localization")
    clock = pygame.time.Clock()

    # Create Board
    board = Board(width=board_width, height=board_height, cell_size=cell_size)

    # Create Robot
    x = np.random.uniform(0, board.width)
    y = np.random.uniform(0, board.height)
    robot = Robot(x=x, y=y, board=board, speed=robot_speed, sensor_limit=sensor_limit)

    # Create Particles
    particles: List[Particle] = list()
    while len(particles) < num_particles:
        x = np.random.uniform(0, board.width)
        y = np.random.uniform(0, board.height)
        particle = Particle(x=x, y=y, board=board)
        if particle.is_valid:
            particles.append(particle)

    # time.sleep(1)

    screen.fill(WHITE)
    board.draw(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False  # Exit the loop if Q key is pressed

        # Read robot sensor
        robot_sensors = robot.read_sensor()
                
        # Read particle sensors and update particle weight
        for particle in particles:
            particle.weight = robot_sensors.gaussian_distance(particle.read_sensor()) 

        # Show particles
        for particle in particles:
            particle.show(screen=screen, color=BLUE)        

        # Show robot
        robot.show(screen=screen, color=RED, radius=10)
                
        # Normalize particle weights
        particle_weight_total = sum([p.weight for p in particles])

        for particle in particles:
            particle.weight /= (particle_weight_total + 1e-8)

        # Resampling particles
        resampling = Resampling(particles)
        particles = resampling.get_particles()

        # Move robot
            
        # Move particles


        # Example usage of calculate_distance_to_wall method
        # x, y = pygame.mouse.get_pos()
        # distance: Distance = board.calculate_distance_to_wall(x, y)
        # print(distance)
    
        # particle = Particle(x=x, y=y, board=board)
        # print(particle.is_valid)

        pygame.display.flip()
        clock.tick(1)

    pygame.quit()


if __name__ == "__main__":
    main()
