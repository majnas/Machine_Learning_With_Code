import pymunk
import pygame
import math

# Initialize pygame and pymunk
SCREEN_WIDTH=1200
SCREEN_HEIGHT=800

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, -1000)

# Create the ground
ground = pymunk.Segment(space.static_body, (0, 100), (SCREEN_WIDTH, 100), 5)
space.add(ground)

# List to store projectiles
projectiles = []

# Variables for tracking mouse button events
mouse_down_pos = ()
mouse_up_pos = ()
mouse_displacement = 0
mouse_held = False

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_held = True
            mouse_down_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_held = False
            mouse_up_pos = event.pos

            # Calculate mouse displacement
            mouse_displacement_vector = ((mouse_down_pos[0]-mouse_up_pos[0]), (mouse_up_pos[1]-mouse_down_pos[1]))
            
            # Create a ball at the mouse `click position
            ball_radius = 10
            ball_mass = 1
            ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
            ball_body = pymunk.Body(ball_mass, ball_moment)
            ball_body.position = (mouse_down_pos[0], SCREEN_HEIGHT - mouse_down_pos[1])
            ball_shape = pymunk.Circle(ball_body, ball_radius)
            space.add(ball_body, ball_shape)
            projectiles.append(ball_body)

            # Calculate shoot_speed based on time held down
            velocity_factor = 5.0  # Adjust this factor to control speed increase rate
            # Apply velocity to the ball in the direction of the shooting segment
            ball_body.velocity = (mouse_displacement_vector[0] * velocity_factor, mouse_displacement_vector[1] * velocity_factor)

    screen.fill((255, 255, 255))

    if mouse_held:
        mouse_pos = pygame.mouse.get_pos()
        # draw shooting segment 
        pygame.draw.line(screen, (255, 0, 0), mouse_down_pos, mouse_pos, 5)

    # Update physics simulation
    dt = 1 / 60.0
    space.step(dt)

    # Draw the ground and projectiles
    pygame.draw.line(screen, (0, 0, 0), (0, SCREEN_HEIGHT-100), (SCREEN_WIDTH, SCREEN_HEIGHT-100), 5)
    for projectile in projectiles:
        pos = projectile.position
        pygame.draw.circle(screen, (0, 0, 0), (int(pos.x), int(SCREEN_HEIGHT - pos.y)), ball_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
