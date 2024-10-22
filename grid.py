import pygame

class Grid:
    def __init__(self, game, state, spacing = 50, color=(100, 100, 100)):
        self.game = game
        self.spacing = spacing
        self.color = color
        self.state = state

    def update(self):
        self.spacing = self.state.zoom_level * 50
        pass

    def draw(self, surface):
        # Draw vertical lines
        for x in range(0, self.game.screen_width):
            offset_x = (x - self.state.x_offset)
            if offset_x % self.spacing == 0:
                # Check if it's every 5th line to make it bold
                if (offset_x // self.spacing) % 5 == 0:
                    pygame.draw.line(surface, self.color, (x, 0), (x, self.game.screen_height), 3)
                else:
                    pygame.draw.line(surface, self.color, (x, 0), (x, self.game.screen_height), 1)

        # Draw horizontal lines
        for y in range(0, self.game.screen_height):
            offset_y = (y - self.state.y_offset)
            if offset_y % self.spacing == 0:
                # Check if it's every 5th line to make it bold
                if (offset_y // self.spacing) % 5 == 0:
                    pygame.draw.line(surface, self.color, (0, y), (self.game.screen_width, y), 3)
                else:
                    pygame.draw.line(surface, self.color, (0, y), (self.game.screen_width, y), 1)
    




