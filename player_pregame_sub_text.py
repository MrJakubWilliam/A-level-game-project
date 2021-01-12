

class PlayerSubText:

    def __init__(self, colour, font, player_name, top_left_corner):
        self.colour = colour
        self.font = font
        self.player_name = player_name
        self.top_left_corner = top_left_corner
        self.subtext_render = self.font.render(str(self.player_name), True, self.colour)

    def render(self, screen):
        screen.blit(self.subtext_render, self.top_left_corner)

    def update(self):
        self.subtext_render = self.font.render(str(self.player_name), True, self.colour)

