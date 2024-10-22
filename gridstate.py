import pygame
from gamestate import GameState
from phasor import Phasor
from grid import Grid
from fractions import Fraction
import random
import math
import colorsys

class GridState(GameState):

    def __init__(self, game):
        super().__init__(game)

        self.game = game

        # Panning Variables
        self.x_offset = self.game.screen_width/2
        self.y_offset = self.game.screen_height/2
        self.is_panning = False
        self.pan_start_pos = (0,0)

        # phasor variables
        self.phasors = []
        self.phasor_cooldown = 0 # specifically phasor cooldown incase I want more cooldowns

        # grid, cuz you only need one
        self.grid = Grid(self.game, self)

        # Zooming Variables
        self.zoom_increment = .1
        self.zoom_level = 1

        self.screen_saver = False
        self.ss_cooldown = 0
        self.screen_saver_max = 8 # how many phasors before full reset
        self.ss_refresh = 2

        self.rainbowI = 0
            

    def get_rainbow(self, start_rgb):

        start_hue= self.rgb_to_hsv(start_rgb)[0]
        hue_off = (start_hue + (self.rainbowI/256)) % 1.0

        #hue = self.rainbowI / 256
        saturation = 1.0
        value = 1.0
        r, g, b = colorsys.hsv_to_rgb(hue_off, saturation, value)
        (r,g,b) = (int(r*255), int(g*255), int(b*255))
        return (r,g,b)

    def rgb_to_hsv(self, color):
        r = color[0] / 255.0
        g = color[1] / 255.0
        b = color[2] / 255.0
        return colorsys.rgb_to_hsv(r,g,b)

    def findOffset(self, x_y):
        return(x_y[0]+self.x_offset, x_y[1]+self.y_offset)
    
    def findOffset0(self, x_y):
        return(x_y[0]-self.x_offset, x_y[1]-self.y_offset)

    def handle_events(self, events):
        pressed_keys = pygame.key.get_pressed()
        for event in events:
            if pressed_keys[pygame.K_1] and self.phasor_cooldown == 0: # adds new phasor
                self.addPhasor()
                self.phasor_cooldown += 5
                #self.end_pos = self.findOffset(self.phasors[-1].find_end())
                for phasor in self.phasors:
                    phasor.points = []
                    phasor.drawing = False
                self.phasors[-1].drawing = True # initializes with 0 points
            if pressed_keys[pygame.K_2] and self.phasor_cooldown == 0: #removes phasor
                if self.phasors:
                    self.phasors.pop() # since points are tied to each phasor this removes points
                    self.phasor_cooldown +=5
                    if self.phasors:
                        #self.end_pos = self.findOffset(self.phasors[-1].find_end())
                        self.drawing = True
            if pressed_keys[pygame.K_3] and self.phasor_cooldown == 0: # restarts drawing
                if self.phasors:
                    for phasor in self.phasors: # removes all points
                        phasor.points = []
                        phasor.drawing = False # not all draw
                    self.phasors[-1].drawing = True # last one draws
            if pressed_keys[pygame.K_4]:
                if self.phasors:
                    for phasor in self.phasors:
                        phasor.points = [] # optional?
                        phasor.drawing = True
            if pressed_keys[pygame.K_5] and self.ss_cooldown == 0:
                if self.screen_saver:
                    self.screen_saver = False
                    self.ss_cooldown = 5
                    print("ScreenSaver Off")
                else:
                    self.screen_saver = True
                    self.ss_cooldown = 5
                    print("Screensaver On")
                
            elif event.type == pygame.MOUSEBUTTONDOWN: # if you press mb1 down it starts panning and gets the start pos
                if event.button == 1:
                    self.is_panning = True
                    self.pan_start_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP: # if you let go of mb1 it stops panning
                if event.button == 1:
                    self.is_panning = False
            elif event.type == pygame.MOUSEMOTION: # if you move the mouse while panning it updates the offset from the pos and resets the start pos
                if self.is_panning:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.x_offset += mouse_x - self.pan_start_pos[0]
                    self.y_offset += mouse_y - self.pan_start_pos[1]
                    self.pan_start_pos = (mouse_x, mouse_y)
            elif event.type == pygame.VIDEORESIZE: # adjusts game width/height. Probably should be done in game class
                self.game.screen_width, self.game.screen_height = event.w, event.h
            elif event.type == pygame.MOUSEWHEEL:

                # convert mouse position to coordinates in the world
                mouse_x, mouse_y = pygame.mouse.get_pos()
                world_x = (mouse_x - self.x_offset) / self.grid.spacing
                world_y = (mouse_y - self.y_offset) / self.grid.spacing

                # adjust the spacing of the graph
                if event.y > 0:
                    self.zoom_level += self.zoom_increment
                    print(self.zoom_level)
                if event.y < 0:
                    self.zoom_level -= self.zoom_increment
                    print(self.zoom_level)      


    def addPhasor(self):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        length = random.randint(10, 100)
        coefficient = random.randint(-3, 3)
        angle_offset = math.radians(random.randint(1, 360))

        if len(self.phasors) == 0:
            self.phasors.append(Phasor(self, None, color, length, coefficient, angle_offset))
        else:
            self.phasors.append(Phasor(self, self.phasors[-1], color, length, coefficient, angle_offset))

    def update(self):
        for entity in self.phasors:
            entity.update()
        self.grid.update()

        if self.rainbowI > 256:
            self.rainbowI = 0
        else:
            self.rainbowI += 1

        if self.screen_saver:
            if self.phasors: # if there are phasors
                if (len(self.phasors) == 1 and len(self.phasors[-1].points) > self.phasors[-1].point_limit/2)or (len(self.phasors) != 1 and len(self.phasors[-1].points) > self.phasors[-1].point_limit*self.ss_refresh): # max of current

                    if len(self.phasors) > self.screen_saver_max: # if theres 5 phasors
                        self.phasors = []
                        self.addPhasor()
                        self.phasors[-1].drawing = True
                    else:
                        self.phasors[-1].drawing = False
                        self.phasors[-1].points = []
                        self.addPhasor()
                        self.phasors[-1].drawing = True
            else: # if there aren't phasors
                self.addPhasor()
                self.phasors[-1].drawing = True


        mouse_x, mouse_y = pygame.mouse.get_pos()
        #print(f"{mouse_x-self.x_offset} {mouse_y-self.y_offset} {len(self.points)} ")
        if self.phasors:
            #print(f"{self.phasors[-1].angle}")
            #print(f"{self.phasors[-1].period()} {self.game.clock.get_fps()}")
            '''periods = [phasor.period() for phasor in self.phasors]
            factor = 1000
            integer_periods = [int(p*factor) for p in periods if math.isfinite(p)]
            resulting_lcm = Phasor.lcm_multiple(integer_periods)
            final_lcm = resulting_lcm / factor'''  
            #current = f"{self.phasors[-1].find_end()[0]+self.x_offset:.3f} {self.phasors[-1].find_end()[1]+self.y_offset:.3f}"
            #end = f"{self.end_pos[0]:.3f} {self.end_pos[1]:.3f}"
            #print(f"end:{end} current:{current} ")
            pass


        if self.phasor_cooldown > 0:
            self.phasor_cooldown -= 1
        if self.ss_cooldown > 0:
            self.ss_cooldown -=1

    def draw(self, surface):
        surface.fill((255,255,255))
        for entity in self.phasors:
            entity.draw(surface)
        self.grid.draw(surface)
        pygame.display.update()