# Importing libraries, modules and the u value__________________________________________________________________________

import pygame
from dynamic_unit import u

# ______________________________________________________________________________________________________________________




class NamePrompt:

    height = 300 * u
    width = 830 * u

    def __init__(self):

        self.top_left_corner = (545*u, 390*u)
        self.rect = pygame.Rect(self.top_left_corner, (self.width, self.height))

    def render(self, screen, colour):
        pygame.draw.rect(screen, colour, self.rect)


class NamePromptText:

    def __init__(self, font, player_name, colour):
        self.colour = colour
        self.player_name = player_name
        self.font = font
        self.top_left_corner = (580*u, 410*u)
        self.top_left_corner_name = (580*u, 560*u)
        self.name_prompt_text_surface = self.font.render(str(self.player_name) + " beat a high score!", True,
                                                         self.colour)
        self.name_prompt_name_text_surface = self.font.render("name: ", True, self.colour)

    def render(self, screen):
        screen.blit(self.name_prompt_text_surface, self.top_left_corner)
        screen.blit(self.name_prompt_name_text_surface, self.top_left_corner_name)

