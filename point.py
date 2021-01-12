# Importing libraries, modules and the u value__________________________________________________________________________

import pygame
from dynamic_unit import u

# ______________________________________________________________________________________________________________________


class Points:

    def __init__(self, top_left_corner, colour):
        self.width = 6*u
        self.height = self.width
        self.rect = pygame.Rect(top_left_corner, (self.width, self.height))
        self.color = colour
        self.position = [float(top_left_corner[0]), float(top_left_corner[1])]

    def render(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)
