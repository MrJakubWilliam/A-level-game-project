# Importing libraries, modules and the u value__________________________________________________________________________

import pygame
from dynamic_unit import u

# ______________________________________________________________________________________________________________________


class ScoreboardLine:  # Line separating the player names and the number of rounds won
    def __init__(self, colour, no_of_players):
        self.width = 2 * u
        self.height = no_of_players * 50 * u
        self.colour = colour
        self.top_left_corner = (160 * u, ((1080 * u)/2)-(self.height/2))
        self.rect = pygame.Rect(self.top_left_corner, (self.width, self.height))

    def render(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)


class ScoreboardPlayerName:
    def __init__(self, colour, player_name, font, sequence_no, no_of_players):
        self.colour = colour
        self.player_name = player_name
        self.no_of_players = no_of_players
        self.sequence_no = sequence_no
        self.y_coordinate = ((((1080 * u)/2)-((self.no_of_players * 50 * u)/2)) - (25 * u)) + \
                            (50 * u * self.sequence_no) - (10 * u)  # The x coordinate for all of the player names is
        # the same, but the y coordinate has to be worked out.

        self.font = font
        self.player_name_render = self.font.render(self.player_name, True, self.colour)

    def update(self):
        self.player_name_render = self.font.render(self.player_name, True, self.colour)

    def render(self, screen):
        screen.blit(self.player_name_render, (10 * u, self.y_coordinate))


class ScoreboardRoundWinnings:
    def __init__(self, colour, no_of_rounds_won, font, sequence_no, no_of_players):
        self.colour = colour
        self.no_of_rounds_won = no_of_rounds_won
        self.no_of_players = no_of_players
        self.sequence_no = sequence_no
        self.y_coordinate = ((((1080 * u)/2)-((self.no_of_players * 50 * u)/2)) - (25 * u)) + \
                            (50 * u * self.sequence_no) - (10 * u)
        self.font = font
        self.player_name_render = self.font.render(str(self.no_of_rounds_won), True, self.colour)

    def update(self):
        self.player_name_render = self.font.render(str(self.no_of_rounds_won), True, self.colour)

    def render(self, screen):
        screen.blit(self.player_name_render, (180 * u, self.y_coordinate))
