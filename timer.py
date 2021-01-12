from dynamic_unit import u


class Timer:
    def __init__(self, colour, font, time_left):
        self.colour = colour
        self.font = font
        self.time_left = time_left
        self.time_string = None
        self.time_text_render = None

    def update_time_text(self):
        self.time_string = "{:02d}".format(self.time_left)
        self.time_text_render = self.font.render(self.time_string, True, self.colour)

    def render(self, screen_x, screen):  # Rendering the timer in the top middle of the display
        screen.blit(self.time_text_render, self.time_text_render.get_rect(centerx=screen_x / 2, centery=50 * u))
