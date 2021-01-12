
class MainMenuText:

    def __init__(self, top_left_corner, colour, font, text):
        self.colour = colour
        self.text = text
        self.font = font
        self.top_left_corner = top_left_corner
        self.text_surface = self.font.render(self.text, True, self.colour)

    def render(self, screen):
        screen.blit(self.text_surface, self.top_left_corner)

    def update(self):
        self.text_surface = self.font.render(self.text, True, self.colour)

