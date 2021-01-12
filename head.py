# Importing libraries, modules and the u value__________________________________________________________________________

import pygame
from pygame.locals import *
from math import sin, cos
from dynamic_unit import u

# ______________________________________________________________________________________________________________________

# Creating the ControlScheme class______________________________________________________________________________________


class ControlScheme:
    def __init__(self):
        self.right = K_RIGHT
        self.left = K_LEFT


# ______________________________________________________________________________________________________________________

# Creating the Head class_______________________________________________________________________________________________


class Head:

    def __init__(self, top_left_corner, colour, dire, control_scheme, player):
        self.width = 15 * u
        self.height = self.width
        self.rect = pygame.Rect(top_left_corner, (self.width, self.height))
        self.colour = colour
        self.speed = 200.0 * u
        self.position = [float(top_left_corner[0]), float(top_left_corner[1])]
        self.dire = dire
        self.x_component = self.speed * sin(self.dire)
        self.y_component = self.speed * cos(self.dire)
        self.control_scheme = control_scheme
        self.turn_right = False
        self.turn_left = False
        self.head_past_locations = []
        self.following_particles = []
        self.player = player
        self.opponent_hits = 0
        self.points_eaten = 0

    def render(self, screen):  # Rendering the head
        pygame.draw.ellipse(screen, self.colour, self.rect)

    def process_event(self, event):  # Processing the user's input
        if event.type == KEYDOWN:
            if event.key == self.control_scheme.right:
                self.turn_right = True

            if event.key == self.control_scheme.left:
                self.turn_left = True

        if event.type == KEYUP:
            if event.key == self.control_scheme.right:
                self.turn_right = False
            if event.key == self.control_scheme.left:
                self.turn_left = False

    def update(self, dt):  # Updating the position of the head
        self.position[0] += self.x_component * dt
        self.rect.x = self.position[0]

        self.position[1] += self.y_component * dt
        self.rect.y = self.position[1]

        # Handling the turning of the head _____________________________________________________________________________

        if self.turn_right:
            self.dire = self.dire-0.06
            self.x_component = self.speed * sin(self.dire)
            self.y_component = self.speed * cos(self.dire)

        if self.turn_left:
            self.dire = self.dire+0.06
            self.x_component = self.speed * sin(self.dire)
            self.y_component = self.speed * cos(self.dire)

        # ______________________________________________________________________________________________________________

# ______________________________________________________________________________________________________________________
