import pymunk
import pygame
import math

# Initialize pygame and pymunk
SCREEN_WIDTH=800
SCREEN_HEIGHT=600

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, -1000)

# Create the ground
ground = pymunk.Segment(space.static_body, (0, 100), (800, 100), 5)
space.add(ground)

# List to store projectiles
projectiles = []

# Variables for tracking mouse button events
mouse_down_time = 0
mouse_up_time = 0
mouse_down_pos = ()
mouse_up_pos = ()
mouse_displacement = 0

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down_pos = event.pos
            mouse_down_time = pygame.time.get_ticks()
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_up_pos = event.pos
            mouse_up_time = pygame.time.get_ticks()

            mouse_displacement = math.sqrt((mouse_up_pos[0]-mouse_down_pos[0])**2 + (mouse_up_pos[1]-mouse_down_pos[1])**2)
            print("mouse_displacement", mouse_displacement)


            # Calculate time held down in milliseconds
            time_held = mouse_up_time - mouse_down_time
            print("time_held", time_held)

            # Create a ball at the mouse `click position
            ball_radius = 10
            ball_mass = 1
            ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
            ball_body = pymunk.Body(ball_mass, ball_moment)
            ball_body.position = (event.pos[0], SCREEN_HEIGHT - event.pos[1])
            ball_shape = pymunk.Circle(ball_body, ball_radius)
            space.add(ball_body, ball_shape)
            projectiles.append(ball_body)

            # Calculate shoot_speed based on time held down
            min_speed = 200  # Minimum shoot speed
            max_speed = 1000  # Maximum shoot speed
            time_factor = 1.0  # Adjust this factor to control speed increase rate
            shoot_speed = min_speed + (max_speed - min_speed) * (time_held * time_factor / 1000)
            print("shoot_speed", shoot_speed)

            # Shoot the ball to the right with the calculated speed
            ball_body.velocity = (shoot_speed, 0)

    screen.fill((255, 255, 255))

    # Update physics simulation
    dt = 1 / 60.0
    space.step(dt)

    # Draw the ground and projectiles
    pygame.draw.line(screen, (0, 0, 0), (0, 100), (800, 100), 5)
    for projectile in projectiles:
        pos = projectile.position
        pygame.draw.circle(screen, (0, 0, 0), (int(pos.x), int(600 - pos.y)), ball_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
