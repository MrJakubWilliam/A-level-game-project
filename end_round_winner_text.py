# Importing the u value ________________________________________________________________________________________________

from dynamic_unit import u

# ______________________________________________________________________________________________________________________


class EndRoundText:
    def __init__(self, colour, font, player_name, type_of_win):
        self.colour = colour
        self.type_of_win = str(type_of_win)
        self.font = font
        self.player_name = player_name
        self.top_left_corner = (500*u, 500*u)
        self.end_round_text_surface = self.font.render(str(self.player_name) + " won the " + self.type_of_win + "!",
                                                       True, self.colour)

    def update(self):
        self.end_round_text_surface = self.font.render(str(self.player_name) + " won the " + self.type_of_win + "!",
                                                       True, self.colour)

    def render(self, screen, screen_x, screen_y):  # Rendering the text in the middle of the screen
        screen.blit(self.end_round_text_surface, self.end_round_text_surface.get_rect(centerx=screen_x / 2,
                                                                                     centery=screen_y / 2))
