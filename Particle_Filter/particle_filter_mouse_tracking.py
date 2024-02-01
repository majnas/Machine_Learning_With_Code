import pygame
import random
import sys 
from typing import List


class Particle():
    def __init__(self, x: int, y: int, weight: float) -> None:
        self.x = x
        self.y = y
        self.weight = weight    


# Particle Filter Parameters
num_particles = 100
particle_radius = 5

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mouse Cursor Tracking with Particle Filter")

particles: List[Particle] = [Particle(x=random.randint(0, 800), y=random.randint(0, 600), weight=1.0 / num_particles) for _ in range(num_particles)]

def predict(particles):
    particles_new = []
    for p in particles:
        x = p.x + random.gauss(0, particle_radius)
        y = p.y + random.gauss(0, particle_radius)
        w = p.weight
        particles_new.append(Particle(x=x, y=y, weight=w))
    return particles_new


def update_weights(particles, mouse_pos):
    for i in range(num_particles):
        particle_x = particles[i].x 
        particle_y = particles[i].y 
        distance = pygame.math.Vector2(particle_x - mouse_pos[0], particle_y - mouse_pos[1]).length()
        particles[i].weight = 1.0 / (distance + 1e-10)
    
    total_weight = sum(p.weight for p in particles)
    for i in range(num_particles):
        particles[i].weight = particles[i].weight / total_weight
    return particles


def resample(particles):
    new_particles = random.choices(particles, weights=[p.weight for p in particles], k=num_particles)
    for i in range(num_particles):
        new_particles[i].weight = 1.0 / num_particles
    return new_particles



# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    particles = predict(particles)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    particles = update_weights(particles, (mouse_x, mouse_y))
    particles = resample(particles)

    screen.fill((255, 255, 255))
    for p in particles:
        pygame.draw.circle(screen, (0, 0, 255), (int(p.x), int(p.y)), particle_radius)

    pygame.draw.circle(screen, (255, 0, 0), pygame.mouse.get_pos(), 10)

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
sys.exit()  # Ensure a clean exit from the script
