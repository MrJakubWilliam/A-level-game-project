
class Player:
    def __init__(self, original_player_name, player_name, controls_left, controls_right, snake_colour, set_name):
        self.original_player_name = original_player_name
        self.player_name = player_name
        self.controls_left = controls_left
        self.controls_right = controls_right
        self.snake_colour = snake_colour
        self.set_name = set_name
        self.rounds_won = 0
