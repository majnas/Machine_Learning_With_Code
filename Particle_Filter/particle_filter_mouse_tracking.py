import pygame
import random
import sys 
from typing import List, Tuple


class Particle():
    def __init__(self, x: int, y: int, weight: float) -> None:
        """
        Initialize a particle with given x, y coordinates, and weight.

        Parameters:
        - x (int): X-coordinate of the particle.
        - y (int): Y-coordinate of the particle.
        - weight (float): Weight of the particle.
        """
        self.x = x
        self.y = y
        self.weight = weight

    def predict(self, particle_radius: int):
        """
        Predict the next position of the particle by adding random Gaussian noise.

        Parameters:
        - particle_radius (int): Radius for random Gaussian noise.

        Returns:
        - Particle: Predicted particle with updated coordinates.
        """
        x = self.x + random.gauss(0, particle_radius)
        y = self.y + random.gauss(0, particle_radius)
        return Particle(x=x, y=y, weight=self.weight)
    
    def update(self, mouse_pos: Tuple):
        """
        Update the weight of the particle based on the distance to the mouse cursor.

        Parameters:
        - mouse_pos (Tuple): Tuple containing x, y coordinates of the mouse cursor.
        """
        distance = pygame.math.Vector2(self.x - mouse_pos[0], self.y - mouse_pos[1]).length()
        self.weight = 1.0 / (distance + 1e-10)

    def __str__(self) -> str:
        return f"x:{self.x} y:{self.y} weight:{self.weight}"


class Swarm():
    def __init__(self, 
                 num_particles: int = 100, 
                 particle_radius: int = 5,
                 display_width: int = 800,
                 display_height: int = 600) -> None:
        """
        Initialize a swarm of particles.

        Parameters:
        - num_particles (int): Number of particles in the swarm.
        - particle_radius (int): Radius for random Gaussian noise during prediction.
        - display_width (int): Width of the display window.
        - display_height (int): Height of the display window.
        """
        self.num_particles = num_particles 
        self.particle_radius = particle_radius
        self.display_width = display_width 
        self.display_height = display_height
        # Initialize particles with random positions and equal weights
        self.particles: List[Particle] = [Particle(x=random.randint(0, display_width), y=random.randint(0, display_height), weight=1.0 / num_particles) for _ in range(num_particles)]

    def predict(self):
        """Predict the next position for each particle in the swarm."""
        for i in range(self.num_particles):
            self.particles[i] = self.particles[i].predict(self.particle_radius)

    def update(self, mouse_pos: Tuple):
        """
        Update the weights of particles based on the distance to the mouse cursor.

        Parameters:
        - mouse_pos (Tuple): Tuple containing x, y coordinates of the mouse cursor.
        """
        for i in range(self.num_particles):
            self.particles[i].update(mouse_pos)
        
        # Normalize particle weights
        total_weight = sum(p.weight for p in self.particles)
        for i in range(self.num_particles):
            self.particles[i].weight = self.particles[i].weight / total_weight

    def resample(self):
        """Resample particles based on their weights."""
        new_particles = random.choices(self.particles, weights=[p.weight for p in self.particles], k=self.num_particles)
        for i in range(self.num_particles):
            new_particles[i].weight = 1.0 / self.num_particles
        self.particles = new_particles


# Display parameters
display_width = 800
display_height = 600

# Particle Filter Parameters
swarm = Swarm(num_particles=100,
              particle_radius=5,
              display_width=display_width, 
              display_height=display_height)

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Mouse Cursor Tracking with Particle Filter")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Particle filter operations
    swarm.predict()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    swarm.update((mouse_x, mouse_y))
    swarm.resample()

    # Drawing on the screen
    screen.fill((255, 255, 255))
    for p in swarm.particles:
        pygame.draw.circle(screen, (0, 0, 255), (int(p.x), int(p.y)), swarm.particle_radius)

    pygame.draw.circle(screen, (255, 0, 0), pygame.mouse.get_pos(), 10)

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
sys.exit()
