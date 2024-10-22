import math
import pygame
from functools import reduce
from fractions import Fraction

class Phasor:
    def __init__(self, state, origin = None, color = (255, 255, 255), length = 100.0, coefficient = 1.0, offset_angle = 0.0):
        
        self.small_angle = 0.01
        self.color = color
        self.state = state

        self.points = []
        self.drawing = False
        self.point_limit = 670 # roughly based on current maximum LCM given omega and coefficient limit

        if origin is None:
            self.x = 0
            self.y = 0
            self.origin = None # if no origin, that means it starts at 0,0
        else:
            self.origin = origin
            self.reposition() # sets x,y starting coords
        self.length = length
        self.coefficient = coefficient
        self.angle = offset_angle # radians, thus offset_angle is in radians

    def rotate(self):
        self.angle += self.coefficient * self.small_angle # important, this will need to go at a certain rate according to a desired period
        self.angle %= (2 * math.pi) # normalizes the value so it doesn't keep increasing

    def reposition(self):
        if self.origin is not None:
            self.x = self.origin.find_end()[0]
            self.y = self.origin.find_end()[1]
        else:
            return

    def find_end(self):
        end_x = self.length*math.cos(self.angle) + self.x
        end_y = self.length*math.sin(self.angle) + self.y
        return ((end_x, end_y))
    
    def update(self):
        self.reposition()
        self.rotate()

        self.length = (-self.state.zoom_level * 50) + 100

        #if len(self.points) > self.point_limit:
        #    self.points.pop(0) # doesn't stop drawing but removes first point
        if self.drawing:
            new_pos = self.state.findOffset(self.find_end())
            self.points.append(new_pos)     

    def draw(self, surface):

        transformed_points = [point for point in self.points]

        pygame.draw.line(surface, (self.color), self.state.findOffset((self.x, self.y)), self.state.findOffset(self.find_end()), 2)
        if len(self.points) > 1:
            pygame.draw.lines(surface, self.state.get_rainbow(self.color), False, transformed_points, 2)
    
    def is_close(pos1, pos2, tolerance=.0001):
        return math.hypot(pos1[0] - pos2[0], pos1[1] - pos2[1]) < tolerance
    
    '''def period(self):
        if self.coefficient == 0:
            return float('inf')
        
        return (2 * math.pi) / abs(self.coefficient * self.small_angle *self.state.game.frame_rate)
    
    def lcm_multiple(numbers):
        return reduce(Phasor.lcm, numbers)
    
    def lcm(a, b):
        return abs(a * b) / math.gcd(a, b)'''

