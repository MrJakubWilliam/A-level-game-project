# Importing the u value ________________________________________________________________________________________________

from dynamic_unit import u

# ______________________________________________________________________________________________________________________


class GameOverText:
    def __init__(self, colour, font):
        self.colour = colour
        self.font = font
        self.string = "Game Over!"
        self.text_render = self.font.render(self.string, True, self.colour)

    def render(self, screen_x, screen):
        screen.blit(self.text_render, self.text_render.get_rect(centerx=screen_x / 2, centery=100 * u))

