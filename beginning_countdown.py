
class StartCountdown:
    def __init__(self, colour, font):
        self.colour = colour
        self.font = font
        self.time_left = 3
        self.countdown_text_render = None

    def update_countdown_text(self):
        self.countdown_text_render = self.font.render(str(self.time_left), True, self.colour)

    def render(self, screen_x, screen_y, screen):  # Rendering the countdown in the middle of the screen
        screen.blit(self. countdown_text_render, self.countdown_text_render.get_rect(centerx=screen_x / 2,
                                                                                     centery=screen_y / 2))
