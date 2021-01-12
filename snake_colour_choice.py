# Importing libraries, modules and the u value__________________________________________________________________________

import pygame
from dynamic_unit import u

# ______________________________________________________________________________________________________________________


class ColourChoiceBlock:
    def __init__(self, colour, width):
        self.width = width
        self.height = 50 * u
        self.colour = colour
        self.top_left_corner = (850 * u, 615 * u)
        self.rect = pygame.Rect(self.top_left_corner, (self.width, self.height))

    def render(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)


class ColourChoiceBlockBorder:
    def __init__(self, colour):
        self.width = 476 * u
        self.height = 54 * u
        self.colour = colour
        self.top_left_corner = (848 * u, 613 * u)
        self.rect = pygame.Rect(self.top_left_corner, (self.width, self.height))

    def render(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)
