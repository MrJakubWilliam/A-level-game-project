# Importing libraries, modules and the u value__________________________________________________________________________

import pygame
from dynamic_unit import u

# ______________________________________________________________________________________________________________________


class FollowingParticle:

    def __init__(self, top_left_corner, colour):
        self.width = 15*u
        self.height = self.width
        self.colour = colour
        self.top_left_corner = top_left_corner
        self.rect = pygame.Rect(self.top_left_corner, (self.width, self.height))
        self.critical_point_time = 0

    def render(self, screen):
        pygame.draw.ellipse(screen, self.colour, self.rect)

    def update(self, top_left_corner, colour, critical_point_time):  # Updating the position of the following particle
        self.rect.x = top_left_corner[0]
        self.rect.y = top_left_corner[1]
        self.top_left_corner = top_left_corner
        self.colour = colour
        self.critical_point_time = critical_point_time - 1
