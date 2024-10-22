import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Zooming Example")

# Set up variables
x_offset = width / 2
y_offset = height / 2
zoom_level = 1.0
zoom_increment = 0.1

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEWHEEL:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Convert mouse position to world coordinates
            world_x = (mouse_x - x_offset) / zoom_level
            world_y = (mouse_y - y_offset) / zoom_level
            
            # Update zoom level
            if event.y > 0:  # Zoom in
                zoom_level += zoom_increment
            elif event.y < 0:  # Zoom out
                zoom_level = max(zoom_level - zoom_increment, 0.1)
            
            # Calculate the new screen coordinates of the world coordinates
            new_screen_x = world_x * zoom_level + x_offset
            new_screen_y = world_y * zoom_level + y_offset
            
            # Adjust offsets to keep the mouse position constant
            x_offset += mouse_x - new_screen_x
            y_offset += mouse_y - new_screen_y

    # Fill the screen with white
    screen.fill((255, 255, 255))
    
    # Draw a grid centered based on the zoom level and offsets
    grid_spacing = 50 * zoom_level
    for x in range(int(x_offset % grid_spacing), width, int(grid_spacing)):
        pygame.draw.line(screen, (100, 100, 100), (x, 0), (x, height))
    for y in range(int(y_offset % grid_spacing), height, int(grid_spacing)):
        pygame.draw.line(screen, (100, 100, 100), (0, y), (width, y))
    
    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
