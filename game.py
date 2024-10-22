import pygame
from gridstate import GridState

class Game():

    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.frame_rate = 60

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GridState(self)


    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.state.draw(self.screen)
            self.state.handle_events(events)
            self.state.update()

            pygame.display.flip()
            self.clock.tick(self.frame_rate)

    def change_state(self, state):
        self.state = state
    
    def quit(self):
        pygame.quit()