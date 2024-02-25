import pygame
import pygame.font
import random
import numpy as np
from typing import List
from icecream import ic
import argparse

from board import Board, Sensors
from particle import Particle, Robot, Resampling

# Define colors
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Main function
def main(board_width, board_height, cell_size, num_particles, robot_speed, sensor_limit, step_by_keyboard):
    pygame.init()
    screen = pygame.display.set_mode((board_width, board_height))
    pygame.display.set_caption("Particle Filter Robot Localization")
    clock = pygame.time.Clock()

    # Create Board
    board = Board(width=board_width, height=board_height, cell_size=cell_size)
    print(board)

    # Create Robot
    robot_is_not_valid = True
    while robot_is_not_valid:
        x = np.random.uniform(0, board.width)
        y = np.random.uniform(0, board.height)    
        robot = Robot(x=x, y=y, board=board, speed=robot_speed, sensor_limit=sensor_limit)
        robot_is_not_valid = not robot.is_valid()

    # Create Particles
    particles: List[Particle] = list()
    while len(particles) < num_particles:
        x = np.random.uniform(0, board.width)
        y = np.random.uniform(0, board.height)
        particle = Particle(x=x, y=y, board=board)
        if particle.is_valid():
            particles.append(particle)

    screen.fill(WHITE)
    board.draw(screen)

    # Add a global variable to track if the simulation is paused
    run_next_step = True
    step = 1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False  # Exit the loop if Q key is pressed
                elif event.key == pygame.K_SPACE:
                    # Toggle pause state when space key is pressed
                    run_next_step = True

        if run_next_step:
            if step_by_keyboard:
                run_next_step = False
            print(f"Step {step} ...")

            # Read robot sensor
            robot_sensors = robot.read_sensor()
                    
            # Read particle sensors and update particle weight
            for particle in particles:
                particle.weight = robot_sensors.gaussian_distance(particle.read_sensor()) 

            # Show board
            screen.fill(WHITE)
            board.draw(screen)

            # Show step number
            font = pygame.font.SysFont('Comic Sans MS', 20)
            step_text = font.render(f"Step: {step}", True, WHITE)
            robot_text = font.render(f"--Robot", True, RED)
            particles_text = font.render(f"--Particles", True, BLUE)
            best_particle_text = font.render(f"--Best Particle", True, YELLOW)
            screen.blit(step_text, (5, 5))
            screen.blit(robot_text, (70, 5))
            screen.blit(particles_text, (130, 5))
            screen.blit(best_particle_text, (210, 5))

            # Show particles
            # Sort to show particles with heigher weight on top of others
            particles.sort(key=lambda particle: particle.weight)
            for particle in particles:
                particle.show(screen=screen)

            # Show the particle with heigest probablity in yellow
            particles[-1].show(screen=screen, color=YELLOW, radius=10)

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
            heading_old = robot.heading
            robot.move()
            heading_new = robot.heading
            dh = heading_new - heading_old
        
            # Move particles
            for particle in particles:
                # Move particle with same heading changes happened for robot
                particle.heading = (particle.heading + dh) % 360
                particle.try_move(speed=robot_speed)

            step += 1

        pygame.display.flip()
        clock.tick(1)

    pygame.quit()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--board_width", type=int, default=800, help="Width of the board")
    parser.add_argument("--board_height", type=int, default=600, help="Height of the board")
    parser.add_argument("--cell_size", type=int, default=20, help="Size of each cell on the board")
    parser.add_argument("--num_particles", type=int, default=1000, help="Number of particles")
    parser.add_argument("--robot_speed", type=int, default=10, help="Speed of the robot")
    parser.add_argument("--sensor_limit", type=int, default=500, help="Sensor limit for the robot")
    parser.add_argument("--step_by_keyboard", action="store_true", help="Enable stepping through the simulation by keyboard")
    args = parser.parse_args()

    main(args.board_width, args.board_height, args.cell_size, args.num_particles, args.robot_speed, args.sensor_limit, args.step_by_keyboard)
