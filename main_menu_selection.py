# Importing libraries, modules and the u value__________________________________________________________________________

import pygame
from dynamic_unit import u

# ______________________________________________________________________________________________________________________


class MainMenuSelectionBox:

    height = 100 * u
    width = 800 * u

    def __init__(self, top_left_corner, colour):

        self.colour = colour
        self.top_left_corner = top_left_corner
        self.rect = pygame.Rect(self.top_left_corner, (self.width, self.height))

    def render(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)
