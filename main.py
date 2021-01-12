# Importing libraries, python classes and the dynamic unit (u)__________________________________________________________

import pygame
import random
import json
from pygame.locals import *
from dynamic_unit import u
from head import Head, ControlScheme
from point import Points
from following_particle import FollowingParticle
from main_menu_selection import MainMenuSelectionBox
from main_menu_text import MainMenuText
from player import Player
from pygame_text_input import TextInput
from snake_colour_choice import ColourChoiceBlock, ColourChoiceBlockBorder
from timer import Timer
from scoreboard import ScoreboardLine, ScoreboardPlayerName, ScoreboardRoundWinnings
from beginning_countdown import StartCountdown
from player_pregame_sub_text import PlayerSubText
from end_round_winner_text import EndRoundText
from game_over_text import GameOverText
from name_prompt import NamePrompt, NamePromptText

# ______________________________________________________________________________________________________________________

# Opening the JSON files _______________________________________________________________________________________________

with open("player_profiles.json", "r") as player_profiles_json:
    player_profiles = json.load(player_profiles_json)

with open("high_scores.json", "r") as high_scores_json:
    high_scores_list = json.load(high_scores_json)

# ______________________________________________________________________________________________________________________

# Setup_________________________________________________________________________________________________________________

pygame.init()
pygame.display.set_caption("Game Project")

screen_x = int(1920*u)
screen_y = int(1080*u)
screen = pygame.display.set_mode((screen_x, screen_y), FULLSCREEN)
background = pygame.Surface(screen.get_size())

light_font = pygame.font.Font("game_fonts\Montserrat-ExtraLight.ttf", int(75 * u))
light_font_for_scoreboard = pygame.font.Font("game_fonts\Montserrat-ExtraLight.ttf", int(20 * u))
light_font_subtext = pygame.font.Font("game_fonts\Montserrat-Light.ttf", int(15 * u))
light_font_for_name_prompt = pygame.font.Font("game_fonts\Montserrat-ExtraLight.ttf", int(40 * u))

heavy_font = pygame.font.Font("game_fonts\Montserrat-Black.ttf", int(75 * u))
heavy_font_large = pygame.font.Font("game_fonts\Montserrat-Black.ttf", int(150 * u))

# Defining colours______________________________________________________________________________________________________

white = pygame.Color("#FFFFFF")
black = pygame.Color("#171717")
red = pygame.Color("#FF595E")
yellow = (255, 202, 58, 255)
green = (138, 201, 38, 255)
blue = (25, 130, 196, 255)
purple = (106, 76, 147, 255)


colours = [yellow, green, blue, purple]
colours_shuffled = random.sample(colours, len(colours))

# ______________________________________________________________________________________________________________________

# Functions_____________________________________________________________________________________________________________


def random_x():  # Randomising the x value for the starting position
    position_x = random.uniform(120 * u, screen_x - (120 * u))
    return position_x


def random_y():  # Randomising the x value for the starting position
    position_y = random.uniform(120 * u, screen_y - (120 * u))
    return position_y


def random_direction():  # Randomising the starting direction of the head
    direction = random.randint(0, 360)
    return direction


def critical_point_decision():  # Deciding whether the following particle should be a critical point
    decision = random.randint(1, 450)
    return decision == 1


def random_critical_point_time_to_live():  # Deciding for how many frames the following point should be a critical point
    decision = random.randint(25, 200)
    return decision

# Collision Detection Algorithm_________________________________________________________________________________________


def collision_detection_algorithm_circles(object1, object2):

    return (((object1[0][0] + (object1[1] / 2)) - (object2[0][0] + (object2[1] / 2))) ** 2) + \
        (((object1[0][1] + (object1[1] / 2)) - (object2[0][1] + (object2[1] / 2))) ** 2) <= \
        (((object1[1] / 2) + (object2[1] / 2)) ** 2)

# ______________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________

# Making the player instances __________________________________________________________________________________________


players = [Player(player_profiles["Player1"]["original_player_name"], player_profiles["Player1"]["player_name"],
                  player_profiles["Player1"]["controls_left"], player_profiles["Player1"]["controls_right"],
                  player_profiles["Player1"]["snake_colour"], player_profiles["Player1"]["set_name"]),

           Player(player_profiles["Player2"]["original_player_name"], player_profiles["Player2"]["player_name"],
                  player_profiles["Player2"]["controls_left"], player_profiles["Player2"]["controls_right"],
                  player_profiles["Player2"]["snake_colour"], player_profiles["Player2"]["set_name"]),

           Player(player_profiles["Player3"]["original_player_name"], player_profiles["Player3"]["player_name"],
                  player_profiles["Player3"]["controls_left"], player_profiles["Player3"]["controls_right"],
                  player_profiles["Player3"]["snake_colour"], player_profiles["Player3"]["set_name"]),

           Player(player_profiles["Player4"]["original_player_name"], player_profiles["Player4"]["player_name"],
                  player_profiles["Player4"]["controls_left"], player_profiles["Player4"]["controls_right"],
                  player_profiles["Player4"]["snake_colour"], player_profiles["Player4"]["set_name"])]

# ______________________________________________________________________________________________________________________

# ______________________________________________________________________________________________________________________

main_menu_selections = [MainMenuSelectionBox(((screen_x/2)-MainMenuSelectionBox.width/2, 190*u), white),
                        MainMenuSelectionBox(((screen_x/2)-MainMenuSelectionBox.width/2, 390*u), white),
                        MainMenuSelectionBox(((screen_x/2)-MainMenuSelectionBox.width/2, 590*u), white),
                        MainMenuSelectionBox(((screen_x/2)-MainMenuSelectionBox.width/2, 790*u), white)]

main_menu_texts = [MainMenuText((((screen_x/2)-MainMenuSelectionBox.width/2) + 10 * u, 190*u), white, light_font, None),
                   MainMenuText((((screen_x/2)-MainMenuSelectionBox.width/2) + 10 * u, 390*u), white, light_font, None),
                   MainMenuText((((screen_x/2)-MainMenuSelectionBox.width/2) + 10 * u, 590*u), white, light_font, None),
                   MainMenuText((((screen_x/2)-MainMenuSelectionBox.width/2) + 10 * u, 790*u), white, light_font, None)]

colour_selection_blocks = [ColourChoiceBlock(white, 472 * u),
                           ColourChoiceBlock(white, 354 * u),
                           ColourChoiceBlock(white, 236 * u),
                           ColourChoiceBlock(white, 118 * u)]

colour_selection_block_border = ColourChoiceBlockBorder(black)

main_menu_main_screen_text = ["Play!", "Settings", "High Scores", "Quit"]
main_settings_text = ["Number of Players: ", "Controls", "Naming Players", "Back"]
controls_settings_text = ["Player: ", "Turn Left: ", "Turn Right: ", "Back"]
naming_players_settings_text = ["Player: ", "New Name: ", "Colour: ", "Back"]

click_counter_for_no_of_players = 0

controls_disallowed_keys = [K_KP_ENTER, K_SPACE, K_TAB, K_CAPSLOCK, K_DELETE, KMOD_SHIFT, KMOD_CTRL, KMOD_ALT, K_ESCAPE,
                            K_LSHIFT, K_LALT, K_LCTRL, K_RCTRL, K_RALT, K_RSHIFT, K_LSUPER, K_RSUPER, K_INSERT,
                            K_DELETE, K_PAGEDOWN, K_PAGEUP, K_HOME, K_END, K_F1, K_F2, K_F3, K_F4, K_F5, K_F6, K_F7,
                            K_F8, K_F9, K_F11, K_F12, K_F13, K_F14, K_F15, K_PRINT, K_RETURN, K_BACKSPACE]

# ______________________________________________________________________________________________________________________

# Running the program __________________________________________________________________________________________________

program_running = True
while program_running:

    pygame.mouse.set_visible(True)
    main_menu_running = True  # Defining the boolean values for the while loops and the page variables
    main_screen = True
    settings = False
    high_scores = False
    controls = False
    naming_players = False
    running_game = False
    selection_colour = white

    controls_player_toggle_click_counter = 0
    naming_players_player_toggle_click_counter = 0
    naming_players_colour_toggle_click_counter = 0

    no_of_players_options = [2, 3, 4]
    colours_options = [None] + colours_shuffled
    background_colour = black

    # Running the main menu_____________________________________________________________________________________________
    while main_menu_running:

        # Event handler ________________________________________________________________________________________________
        user_mouse_click = 0
        mouse_coordinate_x, mouse_coordinate_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                main_menu_running = False

            if event.type == MOUSEBUTTONDOWN:

                if 560 * u <= mouse_coordinate_x <= (560 * u + 800 * u):
                    if 190 * u <= mouse_coordinate_y <= (190 * u + 100 * u):
                        user_mouse_click = 1

                    elif 390 * u <= mouse_coordinate_y <= (390 * u + 100 * u):
                        user_mouse_click = 2

                    elif 590 * u <= mouse_coordinate_y <= (590 * u + 100 * u):
                        user_mouse_click = 3

                    elif 790 * u <= mouse_coordinate_y <= (790 * u + 100 * u):
                        user_mouse_click = 4

            # __________________________________________________________________________________________________________

        screen.blit(background, (0, 0))

        # main screen (front page) logic _______________________________________________________________________________

        if main_screen:

            background.fill(black)

            # Selection boxes click handler ____________________________________________________________________________

            if user_mouse_click == 1:
                main_menu_running = False
                running_game = True
                for player in players:
                    player.matches_won = 0
                for player in players:
                    player.rounds_won = 0
                user_mouse_click = 0

            elif user_mouse_click == 2:
                main_screen = False
                settings = True
                background_colour = main_menu_selections[1].colour
                user_mouse_click = 0

            elif user_mouse_click == 3:
                main_screen = False
                high_scores = True
                background_colour = main_menu_selections[2].colour
                user_mouse_click = 0

            elif user_mouse_click == 4:
                main_screen = False
                main_menu_running = False
                program_running = False
                user_mouse_click = 0

            # __________________________________________________________________________________________________________

            # Rendering selection boxes and the text on top of it ______________________________________________________

            for selection in main_menu_selections:
                selection.colour = colours_shuffled[main_menu_selections.index(selection)]
                selection.render(screen)

            for main_menu_text in main_menu_texts:
                main_menu_text.colour = black
                main_menu_text.text = main_menu_main_screen_text[main_menu_texts.index(main_menu_text)]
                main_menu_text.update()
                main_menu_text.render(screen)

            # __________________________________________________________________________________________________________
        # ______________________________________________________________________________________________________________

        # settings page logic __________________________________________________________________________________________

        if settings:

            background.fill(background_colour)

            # Selection boxes click handler ____________________________________________________________________________

            if user_mouse_click == 1:
                click_counter_for_no_of_players += 1

            elif user_mouse_click == 2:
                settings = False
                controls = True
                selection_colour = background_colour
                user_mouse_click = 0

            elif user_mouse_click == 3:
                settings = False
                naming_players = True
                selection_colour = background_colour
                user_mouse_click = 0

            elif user_mouse_click == 4:
                settings = False
                main_screen = True
                user_mouse_click = 0

            # __________________________________________________________________________________________________________

            # Rendering selection boxes and the text on top of it ______________________________________________________

            for selection in main_menu_selections:
                selection.colour = black
                selection.render(screen)

            for main_menu_text in main_menu_texts:
                main_menu_text.colour = background_colour
                main_menu_text.text = main_settings_text[main_menu_texts.index(main_menu_text)]
                if main_menu_texts.index(main_menu_text) == 0:
                    main_menu_text.text = main_menu_text.text + \
                                          str(no_of_players_options[click_counter_for_no_of_players %
                                                                    len(no_of_players_options)])  # Toggling between the
                    # allowed number of players
                main_menu_text.update()
                main_menu_text.render(screen)

            # __________________________________________________________________________________________________________

        # ______________________________________________________________________________________________________________

        # controls page logic __________________________________________________________________________________________

        if controls:
            background.fill(black)

            # Selection boxes click handler ____________________________________________________________________________

            if user_mouse_click == 1:
                controls_player_toggle_click_counter += 1

            # Key changing______________________________________________________________________________________________

            if user_mouse_click == 2:
                for main_menu_text in main_menu_texts:
                    if main_menu_texts.index(main_menu_text) == 1:
                        main_menu_text.text = main_menu_text.text[0:main_menu_text.text.index(":")+1] + " [set a key]"
                        main_menu_text.update()

                changing_key = True

                while changing_key:
                    events = pygame.event.get()
                    potential_control_key = None
                    control_change_flag = False
                    for event in events:
                        if event.type == MOUSEBUTTONDOWN:
                            changing_key = False
                        if event.type == KEYDOWN:
                            if event.key in controls_disallowed_keys:
                                changing_key = False
                            else:
                                potential_control_key = event.key

                    if potential_control_key is None or potential_control_key == \
                            players[controls_player_toggle_click_counter
                                    % (no_of_players_options[click_counter_for_no_of_players
                                                             % len(no_of_players_options)])].controls_right:

                        control_change_flag = True

                    if not control_change_flag:
                        players[controls_player_toggle_click_counter %
                                (no_of_players_options[click_counter_for_no_of_players %
                                                       len(no_of_players_options)])].controls_left = \
                            potential_control_key

                        player_profiles[players[controls_player_toggle_click_counter
                                                % (no_of_players_options[click_counter_for_no_of_players
                                                                         % len(no_of_players_options)])]
                            .original_player_name]["controls_left"] = \
                            players[controls_player_toggle_click_counter
                                    % (no_of_players_options[click_counter_for_no_of_players
                                                             % len(no_of_players_options)])].controls_left

                        with open("player_profiles.json", "w") as player_profiles_json:
                            json.dump(player_profiles, player_profiles_json)

                        changing_key = False

                    # Rendering selection boxes and the text on top of it ______________________________________________

                    for selection in main_menu_selections:
                        selection.render(screen)

                    for main_menu_text in main_menu_texts:
                        main_menu_text.render(screen)

                    # __________________________________________________________________________________________________

                    pygame.display.update()
            # __________________________________________________________________________________________________________

            # Key changing______________________________________________________________________________________________

            if user_mouse_click == 3:

                for main_menu_text in main_menu_texts:
                    if main_menu_texts.index(main_menu_text) == 2:
                        main_menu_text.text = main_menu_text.text[0:main_menu_text.text.index(":") + 1] + " [set a key]"
                        main_menu_text.update()

                changing_key = True
                while changing_key:
                    events = pygame.event.get()
                    potential_control_key = None
                    control_change_flag = False
                    for event in events:
                        if event.type == MOUSEBUTTONDOWN:
                            changing_key = False
                        if event.type == KEYDOWN:
                            if event.key in controls_disallowed_keys:
                                changing_key = False
                            else:
                                potential_control_key = event.key

                    for player in players:
                        if potential_control_key is None or potential_control_key == player.controls_left:

                            control_change_flag = True

                    if not control_change_flag:
                        players[controls_player_toggle_click_counter %
                                (no_of_players_options[click_counter_for_no_of_players %
                                                       len(no_of_players_options)])].controls_right = \
                            potential_control_key

                        player_profiles[players[controls_player_toggle_click_counter %
                                                (no_of_players_options[click_counter_for_no_of_players
                                                                       % len(no_of_players_options)])]
                            .original_player_name]["controls_right"] = players[controls_player_toggle_click_counter
                                                                               % (no_of_players_options
                        [click_counter_for_no_of_players % len(no_of_players_options)])].controls_right

                        with open("player_profiles.json", "w") as player_profiles_json:
                            json.dump(player_profiles, player_profiles_json)
                        changing_key = False

                    # Rendering selection boxes and the text on top of it ______________________________________________

                    for selection in main_menu_selections:
                        selection.render(screen)

                    for main_menu_text in main_menu_texts:
                        main_menu_text.update()
                        main_menu_text.render(screen)

                    # __________________________________________________________________________________________________

                    pygame.display.update()

            # __________________________________________________________________________________________________________

            if user_mouse_click == 4:
                settings = True
                controls = False

            # __________________________________________________________________________________________________________

            # Rendering selection boxes and the text on top of it ______________________________________________________

            for selection in main_menu_selections:
                selection.colour = selection_colour
                selection.render(screen)

            for main_menu_text in main_menu_texts:
                main_menu_text.colour = black
                main_menu_text.text = controls_settings_text[main_menu_texts.index(main_menu_text)]

                if main_menu_texts.index(main_menu_text) == 0:
                    main_menu_text.text = main_menu_text.text + \
                                          players[controls_player_toggle_click_counter %
                                                  (no_of_players_options[click_counter_for_no_of_players %
                                                                         len(no_of_players_options)])].player_name

                elif main_menu_texts.index(main_menu_text) == 1:
                    main_menu_text.text = main_menu_text.text + \
                                          pygame.key.name(players[controls_player_toggle_click_counter %
                                                                  (no_of_players_options[click_counter_for_no_of_players
                                                                                         % len(no_of_players_options)])]
                                                          .controls_left)

                elif main_menu_texts.index(main_menu_text) == 2:
                    main_menu_text.text = main_menu_text.text + \
                                          pygame.key.name(players[controls_player_toggle_click_counter %
                                                                  (no_of_players_options[click_counter_for_no_of_players
                                                                                         % len(no_of_players_options)])]
                                                          .controls_right)

                main_menu_text.update()
                main_menu_text.render(screen)

            # __________________________________________________________________________________________________________

        # ______________________________________________________________________________________________________________

        # naming players page logic ____________________________________________________________________________________

        if naming_players:
            background.fill(black)

            # Selection boxes click handler ____________________________________________________________________________

            if user_mouse_click == 1:
                naming_players_player_toggle_click_counter += 1

            elif user_mouse_click == 2:

                # Text input____________________________________________________________________________________________

                input_text = \
                    TextInput("", "game_fonts\Montserrat-ExtraLight.ttf", int(50 * u), True, black, black, 400, 35)
                text_write_flag = False

                running_text = True
                while running_text:
                    events = pygame.event.get()
                    for event in events:
                        if event.type == MOUSEBUTTONDOWN:
                            running_text = False
                            text_write_flag = True
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                running_text = False
                                text_write_flag = True
                            if event.key == K_RETURN:
                                running_text = False

                    # Rendering selection boxes, the text on top of them and the colour block __________________________

                    for selection in main_menu_selections:
                        selection.colour = selection_colour
                        selection.render(screen)

                    for main_menu_text in main_menu_texts:
                        main_menu_text.colour = black
                        main_menu_text.text = naming_players_settings_text[main_menu_texts.index(main_menu_text)]
                        if main_menu_texts.index(main_menu_text) == 0:
                            main_menu_text.text = \
                                main_menu_text.text + \
                                players[naming_players_player_toggle_click_counter %
                                        (no_of_players_options[click_counter_for_no_of_players %
                                                               len(no_of_players_options)])].player_name

                        main_menu_text.update()
                        main_menu_text.render(screen)

                    colour_selection_block_border.render(screen)

                    if players[naming_players_player_toggle_click_counter %
                               (no_of_players_options[click_counter_for_no_of_players %
                                                      len(no_of_players_options)])].snake_colour is None:

                        for colour_selection_block in colour_selection_blocks:
                            colour_selection_block.colour = colours_shuffled[
                                colour_selection_blocks.index(colour_selection_block)]
                            colour_selection_block.render(screen)

                    else:
                        for colour_selection_block in colour_selection_blocks:
                            colour_selection_block.colour = \
                                players[naming_players_player_toggle_click_counter
                                        % (no_of_players_options[click_counter_for_no_of_players
                                                                 % len(no_of_players_options)])].snake_colour

                            colour_selection_block.render(screen)
                    # __________________________________________________________________________________________________

                    input_text.update(events)
                    screen.blit(input_text.get_surface(), (1000 * u, 412 * u))

                    pygame.display.update()
                # ______________________________________________________________________________________________________

                # Handling the text input_______________________________________________________________________________

                text_input_in_list_form = list(input_text.get_text())

                invalid_input_flag = True
                for character in text_input_in_list_form:
                    if character != " ":
                        invalid_input_flag = False

                if len(text_input_in_list_form) > 10:
                    invalid_input_flag = True

                if not text_write_flag and input_text.get_text() != "" and not invalid_input_flag:
                    players[naming_players_player_toggle_click_counter %
                            (no_of_players_options[click_counter_for_no_of_players %
                                                   len(no_of_players_options)])].player_name = input_text.get_text()

                    players[naming_players_player_toggle_click_counter %
                            (no_of_players_options[click_counter_for_no_of_players %
                                                   len(no_of_players_options)])].set_name = True

                    player_profiles[players[naming_players_player_toggle_click_counter
                                            % (no_of_players_options[click_counter_for_no_of_players
                                                                     % len
                                                                     (no_of_players_options)])]

                        .original_player_name]["player_name"] = \
                        players[naming_players_player_toggle_click_counter
                                % (no_of_players_options[click_counter_for_no_of_players
                                                         % len(no_of_players_options)])].player_name

                    player_profiles[players[naming_players_player_toggle_click_counter %
                                            (no_of_players_options[click_counter_for_no_of_players %
                                                                   len(no_of_players_options)])]
                        .original_player_name]["set_name"] = \
                        players[naming_players_player_toggle_click_counter
                                % (no_of_players_options[click_counter_for_no_of_players
                                                         % len(no_of_players_options)])].set_name

                    with open("player_profiles.json", "w") as player_profiles_json:
                        json.dump(player_profiles, player_profiles_json)

                # ______________________________________________________________________________________________________

            elif user_mouse_click == 3:
                naming_players_colour_toggle_click_counter += 1

                players[naming_players_player_toggle_click_counter
                        % (no_of_players_options[click_counter_for_no_of_players
                                                 % len(no_of_players_options)])]\
                    .snake_colour = colours_options[naming_players_colour_toggle_click_counter % len(colours_options)]

                player_profiles[players[naming_players_player_toggle_click_counter %
                                        (no_of_players_options[click_counter_for_no_of_players
                                                               % len(no_of_players_options)])]
                    .original_player_name]["snake_colour"] = \
                    players[naming_players_player_toggle_click_counter
                            % (no_of_players_options[click_counter_for_no_of_players
                                                     % len(no_of_players_options)])].snake_colour

                with open("player_profiles.json", "w") as player_profiles_json:
                    json.dump(player_profiles, player_profiles_json)

            elif user_mouse_click == 4:
                settings = True
                naming_players = False

            # __________________________________________________________________________________________________________

            # Rendering selection boxes, the text on top of them and the colour block __________________________________

            for selection in main_menu_selections:
                selection.colour = selection_colour
                selection.render(screen)

            for main_menu_text in main_menu_texts:
                main_menu_text.colour = black
                main_menu_text.text = naming_players_settings_text[main_menu_texts.index(main_menu_text)]

                if main_menu_texts.index(main_menu_text) == 0:
                    main_menu_text.text = main_menu_text.text + \
                                          players[naming_players_player_toggle_click_counter %
                                                  (no_of_players_options[click_counter_for_no_of_players %
                                                                         len(no_of_players_options)])].player_name
                main_menu_text.update()
                main_menu_text.render(screen)

            colour_selection_block_border.render(screen)

            if players[naming_players_player_toggle_click_counter % (no_of_players_options[click_counter_for_no_of_players %
                                                                                           len(no_of_players_options)])].\
                    snake_colour is None:

                for colour_selection_block in colour_selection_blocks:
                    colour_selection_block.colour = colours_shuffled[colour_selection_blocks.index(colour_selection_block)]
                    colour_selection_block.render(screen)

            else:
                for colour_selection_block in colour_selection_blocks:
                    colour_selection_block.colour = players[naming_players_player_toggle_click_counter %
                                                            (no_of_players_options[click_counter_for_no_of_players %
                                                                                   len(no_of_players_options)])]\
                        .snake_colour
                    colour_selection_block.render(screen)
            # __________________________________________________________________________________________________________

        # ______________________________________________________________________________________________________________

        # high scores page logic _______________________________________________________________________________________

        if high_scores:

            high_scores_page_text = ["Longest Snake", "Opponent hits/round", "Most points eaten", "Back"]

            # Handling the hovering over the selection boxes ___________________________________________________________

            mouse_coordinate_x, mouse_coordinate_y = pygame.mouse.get_pos()
            if 560 * u <= mouse_coordinate_x <= (560 * u + 800 * u):

                if 190 * u <= mouse_coordinate_y <= (190 * u + 100 * u):
                    high_scores_page_text[0] = high_scores_list["LongestSnake"]["player"] + " : " + \
                                               str(high_scores_list["LongestSnake"]["score"])

                elif 390 * u <= mouse_coordinate_y <= (390 * u + 100 * u):
                    high_scores_page_text[1] = high_scores_list["OpponentHits"]["player"] + " : " + \
                                               str(high_scores_list["OpponentHits"]["score"])

                elif 590 * u <= mouse_coordinate_y <= (590 * u + 100 * u):
                    high_scores_page_text[2] = high_scores_list["MostPointsEaten"]["player"] + " : " + \
                                               str(high_scores_list["MostPointsEaten"]["score"])

            # __________________________________________________________________________________________________________

            if user_mouse_click == 4:
                high_scores = False
                main_screen = True
                user_mouse_click = 0

            background.fill(background_colour)

            # Rendering selection boxes and the text on top of it ______________________________________________________

            for selection in main_menu_selections:
                selection.colour = black
                selection.render(screen)

            for main_menu_text in main_menu_texts:
                main_menu_text.colour = background_colour
                main_menu_text.text = high_scores_page_text[main_menu_texts.index(main_menu_text)]
                main_menu_text.update()
                main_menu_text.render(screen)
            # __________________________________________________________________________________________________________
        # ______________________________________________________________________________________________________________

        pygame.display.flip()

    # Running the game__________________________________________________________________________________________________

    while running_game:

        pygame.mouse.set_visible(False)

        # Defining the control schemes__________________________________________________________________________________

        control_scheme0 = ControlScheme()
        control_scheme0.right = players[0].controls_right
        control_scheme0.left = players[0].controls_left

        control_scheme1 = ControlScheme()
        control_scheme1.right = players[1].controls_right
        control_scheme1.left = players[1].controls_left

        control_scheme2 = ControlScheme()
        control_scheme2.right = players[2].controls_right
        control_scheme2.left = players[2].controls_left

        control_scheme3 = ControlScheme()
        control_scheme3.right = players[3].controls_right
        control_scheme3.left = players[3].controls_left

        # ______________________________________________________________________________________________________________

        for player_number in range(len(players)):
            if players[player_number].snake_colour is None:
                players[player_number].snake_colour = colours_shuffled[player_number]

        # Creating the instances of the Head____________________________________________________________________________

        all_heads = [Head((random_x(), random_y()), players[0].snake_colour, random_direction(), control_scheme0,
                          players[0]),
                     Head((random_x(), random_y()), players[1].snake_colour, random_direction(), control_scheme1,
                          players[1]),
                     Head((random_x(), random_y()), players[2].snake_colour, random_direction(), control_scheme2,
                          players[2]),
                     Head((random_x(), random_y()), players[3].snake_colour, random_direction(), control_scheme3,
                          players[3])]

        # ______________________________________________________________________________________________________________

        # Creating an array of the heads in the match___________________________________________________________________
        heads_match = []
        for head_in_game in range(no_of_players_options[click_counter_for_no_of_players % len(no_of_players_options)]):
            heads_match.append(all_heads[head_in_game])

        heads_match_non_remove = []
        for head_in_game in range(no_of_players_options[click_counter_for_no_of_players % len(no_of_players_options)]):
            heads_match_non_remove.append(all_heads[head_in_game])

        # ______________________________________________________________________________________________________________

        # Creating the instances of the objects in the game_____________________________________________________________

        timer_instance = Timer(white, heavy_font, 30)
        start_countdown = StartCountdown(white, heavy_font_large)
        scoreboard_line = ScoreboardLine(white, len(heads_match))
        game_over_text = GameOverText(white, heavy_font_large)
        scoreboard_player_names = [ScoreboardPlayerName(white, None, light_font_for_scoreboard, 1,
                                                        len(heads_match_non_remove)),
                                   ScoreboardPlayerName(white, None, light_font_for_scoreboard, 2,
                                                        len(heads_match_non_remove)),
                                   ScoreboardPlayerName(white, None, light_font_for_scoreboard, 3,
                                                        len(heads_match_non_remove)),
                                   ScoreboardPlayerName(white, None, light_font_for_scoreboard, 4,
                                                        len(heads_match_non_remove))]
        scoreboard_round_winnings = [ScoreboardRoundWinnings(white, None, light_font_for_scoreboard, 1,
                                                             len(heads_match)),
                                     ScoreboardRoundWinnings(white, None, light_font_for_scoreboard, 2,
                                                             len(heads_match)),
                                     ScoreboardRoundWinnings(white, None, light_font_for_scoreboard, 3,
                                                             len(heads_match)),
                                     ScoreboardRoundWinnings(white, None, light_font_for_scoreboard, 4,
                                                             len(heads_match))]
        player_subtexts = [PlayerSubText(white, light_font_subtext, None, None),
                           PlayerSubText(white, light_font_subtext, None, None),
                           PlayerSubText(white, light_font_subtext, None, None),
                           PlayerSubText(white, light_font_subtext, None, None)]
        end_round_text = EndRoundText(white, light_font, None, None)
        name_prompt = NamePrompt()
        restart = MainMenuSelectionBox((((screen_x / 2) - MainMenuSelectionBox.width / 2),
                                        (((screen_y / 2) - MainMenuSelectionBox.height) - 25 * u)),
                                       random.choice(colours))
        restart_text = MainMenuText((((screen_x / 2) - MainMenuSelectionBox.width / 2) + 10 * u,
                                     (((screen_y / 2) - MainMenuSelectionBox.height) - 25 * u)), black,
                                    light_font, "Restart")
        back_to_main_menu = MainMenuSelectionBox(
            (((screen_x / 2) - MainMenuSelectionBox.width / 2), (screen_y / 2) + 25 * u), red)
        back_to_main_menu_text = MainMenuText((((screen_x / 2) - MainMenuSelectionBox.width / 2) + 10 * u,
                                               (screen_y / 2) + 25 * u), black,
                                              light_font, "Main Menu")

        # ______________________________________________________________________________________________________________

        # Creating the boolean variable that direct the flow of the code________________________________________________

        running_round = True
        render_points_start = True
        overtime_flag = False
        end_round_flag = False
        render_countdown_flag = False
        restart_screen = False

        # ______________________________________________________________________________________________________________

        # Creating arrays used for recording high scores________________________________________________________________

        longest_snake_round = [0, None, None]  # (score, player name, name_set)
        most_opponent_hits_round = [0, None, None]
        most_points_eaten_round = [0, None, None]

        # ______________________________________________________________________________________________________________

        # Creating the variables related to the timing__________________________________________________________________

        time = 0
        second_cycle = 0
        end_round_time = 0
        end_round_second_cycle = 0
        clock = pygame.time.Clock()
        frame_time = clock.tick(5)
        time_delta = frame_time / 1000.0

        # ______________________________________________________________________________________________________________

        # Restart screen________________________________________________________________________________________________

        for head in heads_match:
            if head.player.rounds_won >= 3:
                restart_screen = True

        if restart_screen:
            background.fill(black)
            screen.blit(background, (0, 0))
            while restart_screen:
                pygame.mouse.set_visible(True)

                # Rendering the restart and the main menu buttons, and the text on top__________________________________

                restart.render(screen)
                back_to_main_menu.render(screen)
                restart_text.render(screen)
                back_to_main_menu_text.render(screen)
                game_over_text.render(screen_x, screen)
                pygame.display.flip()

                # ______________________________________________________________________________________________________

                # Event handler ________________________________________________________________________________________

                mouse_coordinate_x, mouse_coordinate_y = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                        if 560 * u <= mouse_coordinate_x <= (560 * u + MainMenuSelectionBox.width):

                            if (((screen_y / 2) - MainMenuSelectionBox.height) - 25 * u) <= mouse_coordinate_y <= \
                                        ((((screen_y / 2) - MainMenuSelectionBox.height) - 25 * u) +
                                         MainMenuSelectionBox.height):  # Restart
                                restart_screen = False
                                for player in players:
                                    player.rounds_won = 0
                                running_round = True
                                running_game = True
                                frame_time = clock.tick(60)
                                time_delta = frame_time / 1000.0

                            elif ((screen_y / 2) + 25 * u) <= mouse_coordinate_y <= (
                                        ((screen_y / 2) + 25 * u) + MainMenuSelectionBox.height):  # Back to main menu
                                restart_screen = False
                                running_game = False
                                running_round = False
                                main_menu_running = True
                                main_screen = True

                # ______________________________________________________________________________________________________

        # Defining the array point _____________________________________________________________________________________

        points = []

        # ______________________________________________________________________________________________________________

        # Running the round ____________________________________________________________________________________________

        while running_round:
            frame_time = clock.tick(60)
            # print(frame_time)
            time_delta = frame_time / 1000.0
            time += time_delta

            # Event handler_____________________________________________________________________________________________

            for event in pygame.event.get():

                if event.type == QUIT:
                    running_round = False
                    running_game = False

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:

                        # Pause screen__________________________________________________________________________________

                        for head in heads_match:
                            head.turn_right = False
                            head.turn_left = False

                        pygame.mouse.set_visible(True)
                        pause_screen = True

                        # Creating the instances of the buttons and the texts on top of them____________________________

                        resume = MainMenuSelectionBox((((screen_x/2)-MainMenuSelectionBox.width/2),
                                                       (((screen_y/2) - MainMenuSelectionBox.height) - 25 * u)),
                                                      random.choice(colours))
                        resume_text = MainMenuText((((screen_x/2)-MainMenuSelectionBox.width/2) + 10 * u,
                                                    (((screen_y/2) - MainMenuSelectionBox.height) - 25 * u)), black,
                                                   light_font, "Resume")

                        back_to_main_menu = MainMenuSelectionBox((((screen_x/2)-MainMenuSelectionBox.width/2),
                                                                  (screen_y/2) + 25 * u), red)
                        back_to_main_menu_text = MainMenuText((((screen_x / 2) - MainMenuSelectionBox.width / 2)
                                                               + 10 * u,
                                                               (screen_y / 2) + 25 * u), black, light_font, "Main Menu")

                        # ______________________________________________________________________________________________

                        background.fill(black)
                        background.set_alpha(200)
                        screen.blit(background, (0, 0))

                        while pause_screen:
                            resume.render(screen)
                            back_to_main_menu.render(screen)

                            resume_text.render(screen)
                            back_to_main_menu_text.render(screen)

                            pygame.display.flip()

                            mouse_coordinate_x, mouse_coordinate_y = pygame.mouse.get_pos()
                            clock = pygame.time.Clock()

                            # Event handler ____________________________________________________________________________

                            for event_two in pygame.event.get():
                                if event_two.type == MOUSEBUTTONDOWN:
                                    if 560 * u <= mouse_coordinate_x <= (560 * u + MainMenuSelectionBox.width):

                                        if (((screen_y / 2) - MainMenuSelectionBox.height) - 25 * u) <= \
                                                mouse_coordinate_y <= ((((screen_y / 2) -
                                                                         MainMenuSelectionBox.height) - 25 * u) +
                                                                       MainMenuSelectionBox.height):  # Resume
                                            pause_screen = False
                                            frame_time = clock.tick(60)
                                            time_delta = frame_time / 1000.0

                                        elif ((screen_y/2) + 25 * u) <= mouse_coordinate_y <= \
                                                (((screen_y/2) + 25 * u) + MainMenuSelectionBox.height):  # Main Menu
                                            pause_screen = False
                                            running_round = False
                                            running_game = False
                                            main_menu_running = True
                                            main_screen = True

                            # __________________________________________________________________________________________
                        # ______________________________________________________________________________________________

                for head in heads_match:
                    head.process_event(event)

            # __________________________________________________________________________________________________________

            screen.blit(background, (0, 0))

            # Timer_____________________________________________________________________________________________________

            if (time > 0.9 and second_cycle >= 3) or (second_cycle >= 4):
                if time > 1 and second_cycle != 3 and timer_instance.time_left != 0:
                    timer_instance.time_left -= 1

                elif time > 0.5 and not time > 1 and timer_instance.time_left == 0:
                    timer_instance.colour = red

                elif time > 1 and timer_instance.time_left <= 0:
                    if not overtime_flag:
                        best_heads = []
                        heads_compare_variable = 0
                        for head in heads_match:
                            if len(head.following_particles) >= heads_compare_variable:
                                heads_compare_variable = len(head.following_particles)

                        for head in heads_match:
                            if len(head.following_particles) >= heads_compare_variable:
                                best_heads.append(head)

                        for head in heads_match:
                            if head not in best_heads:
                                heads_match.remove(head)

                    if not overtime_flag:
                        best_heads = []
                        heads_compare_variable = 0
                        for head in heads_match:
                            if len(head.following_particles) >= heads_compare_variable:
                                heads_compare_variable = len(head.following_particles)

                        for head in heads_match:
                            if len(head.following_particles) >= heads_compare_variable:
                                best_heads.append(head)

                        for head in heads_match:
                            if head not in best_heads:
                                heads_match.remove(head)

                    overtime_flag = True
                    timer_instance.colour = black

                timer_instance.update_time_text()
                timer_instance.render(screen_x, screen)
            # __________________________________________________________________________________________________________

            # Scoreboard________________________________________________________________________________________________

            scoreboard_line.render(screen)

            for scoreboard_player_no in range(len(heads_match_non_remove)):
                scoreboard_player_names[scoreboard_player_no].player_name = players[scoreboard_player_no].player_name
                scoreboard_player_names[scoreboard_player_no].update()
                scoreboard_player_names[scoreboard_player_no].render(screen)

                scoreboard_round_winnings[scoreboard_player_no].no_of_rounds_won = players[scoreboard_player_no]\
                    .rounds_won
                scoreboard_round_winnings[scoreboard_player_no].update()
                scoreboard_round_winnings[scoreboard_player_no].render(screen)

            # __________________________________________________________________________________________________________

            # Creating the instances of points and rendering them_______________________________________________________
            point_random_decide = random.randint(0, 120)
            if point_random_decide == 100 and not render_points_start:  # Deciding if another point should be
                points.append(Points((random_x(), random_y()), white))  # added on the screen
            elif render_points_start:
                for i in range(0, 100):
                    points.append(Points((random_x(), random_y()), white))

            for point in points:
                point.render(screen)

            # __________________________________________________________________________________________________________

            # Before the round begins __________________________________________________________________________________

            if not ((time == 0 and second_cycle == 0) or (time > 0.9 and second_cycle >= 3) or (second_cycle >= 4)):

                # Rendering the little text appearing above the heads displaying the name of the play corresponding to
                # the head______________________________________________________________________________________________

                for head in heads_match:
                    head.render(screen)
                    player_subtexts[heads_match.index(head)].colour = head.colour
                    player_subtexts[heads_match.index(head)].player_name = head.player.player_name

                    player_subtexts[heads_match.index(head)].top_left_corner = (head.position[0] - 50 * u,
                                                                                head.position[1] - 20 * u)
                    player_subtexts[heads_match.index(head)].update()
                    player_subtexts[heads_match.index(head)].render(screen)

                # ______________________________________________________________________________________________________

                # Countdown_____________________________________________________________________________________________

                if time > 0.5 and not time > 1:
                    render_countdown_flag = True

                if time > 1:
                    start_countdown.time_left -= 1
                    if start_countdown.time_left == 0:
                        start_countdown.time_left = "GO!"
                    render_countdown_flag = False

                if render_countdown_flag:
                    start_countdown.update_countdown_text()
                    start_countdown.render(screen_x, screen_y, screen)
                # ______________________________________________________________________________________________________

            # __________________________________________________________________________________________________________

            # Gameplay _________________________________________________________________________________________________

            else:
                for head in heads_match:

                    delete_head_flag = False
                    head.update(time_delta)
                    head.render(screen)

                    head.head_past_locations.insert(0, (head.position[0], head.position[1]))

                    # Head - point collision detection _________________________________________________________________

                    for point in points:

                        if collision_detection_algorithm_circles([head.position, head.width], [point.position,
                                                                                               point.width]):
                            points.remove(point)
                            head.following_particles.append(FollowingParticle((0, 0), head.colour))
                            head.points_eaten += 1

                    # __________________________________________________________________________________________________

                    # Head - following particle/critical point collision detection _____________________________________

                    for following_particle in head.following_particles:

                        if critical_point_decision() and not following_particle.critical_point_time > 0:

                            time_decision = random_critical_point_time_to_live()
                            following_particle.update(head.head_past_locations[(head.following_particles
                                                                                .index(following_particle)+1) * 6],
                                                      red, time_decision)

                        if following_particle.critical_point_time > 0 and len(head.following_particles)>0:
                            following_particle.update(head.head_past_locations[(head.following_particles
                                                                                .index(following_particle)+1) * 6],
                                                      red, following_particle.critical_point_time)

                            for head_for_collision in heads_match:
                                if collision_detection_algorithm_circles([head_for_collision.position,
                                                                          head_for_collision.width],
                                                                         [following_particle.top_left_corner,
                                                                          following_particle.width]):

                                    if len(head.following_particles) > longest_snake_round[0]:
                                        longest_snake_round = [len(head.following_particles), head.player.player_name,
                                                               head.player.set_name]
                                        colour_longest_snake_round = head.colour

                                    if head_for_collision != head:
                                        head_for_collision.opponent_hits += 1

                                    head.following_particles = []
                                    if timer_instance.time_left == 0:
                                        delete_head_flag = True
                                    head.position[0] = random_x()
                                    head.position[1] = random_y()

                        if following_particle.critical_point_time <= 0:
                            if ((time > 0.17 and second_cycle >= 4) or (second_cycle >= 5)) and len(head.following_particles)>0:
                                following_particle.update(head.head_past_locations[(head.following_particles.index(following_particle)+1) * 6],
                                                          head.colour, 1)

                            for head_for_collision in heads_match:
                                if collision_detection_algorithm_circles([head_for_collision.position, head_for_collision.width],
                                                                         [following_particle.top_left_corner,
                                                                          following_particle.width]):

                                    if len(head_for_collision.following_particles) > longest_snake_round[0]:
                                        longest_snake_round = [len(head_for_collision.following_particles), head_for_collision.player.player_name, head_for_collision.player.set_name]
                                        colour_longest_snake_round = head_for_collision.colour

                                    head_for_collision.following_particles = []
                                    if timer_instance.time_left == 0:
                                        if len(heads_match) > 1:
                                            heads_match.remove(head_for_collision)
                                    head_for_collision.position[0] = random_x()
                                    head_for_collision.position[1] = random_y()

                        following_particle.render(screen)

                    # __________________________________________________________________________________________________

                    # head - wall collision detection___________________________________________________________________

                    if (head.position[0] <= 0 or head.position[0] >= screen_x-head.width) or \
                            (head.position[1] <= 0 or head.position[1] >= screen_y-head.width):

                        if (len(head.following_particles)) > longest_snake_round[0]:
                            longest_snake_round = [len(head.following_particles), head.player.player_name,
                                                   head.player.set_name]
                            colour_longest_snake_round = head.colour

                        head.following_particles = []

                        if timer_instance.time_left == 0:
                            delete_head_flag = True

                        head.position[0] = random_x()
                        head.position[1] = random_y()
                    # __________________________________________________________________________________________________

                    if delete_head_flag:
                        if len(heads_match) > 1:
                            heads_match.remove(head)

                # Rendering the text about who is the winner ___________________________________________________________

                if len(heads_match) == 1:
                    for head in heads_match:

                        if not end_round_flag:
                            head.player.rounds_won += 1
                            if head.player.rounds_won < 3:
                                end_round_text.type_of_win = "round"
                            else:
                                end_round_text.type_of_win = "match"

                            if head.player.player_name is not None:
                                end_round_text.player_name = head.player.player_name

                                end_round_text.update()

                            else:
                                end_round_text.player_name = head.player.original_player_name
                                end_round_text.update()

                            end_round_flag = True

                    end_round_time += time_delta
                    if end_round_time > 1:
                        end_round_time -= 1
                        end_round_second_cycle += 1

                    end_round_text.render(screen, screen_x, screen_y)

                    if (end_round_time > 0.3 and end_round_second_cycle >= 1) or end_round_time >= 2:
                        running_round = False
                        running_game = True

                # ______________________________________________________________________________________________________
            # __________________________________________________________________________________________________________

            render_points_start = False
            # timer += 1
            if time > 1:
                time -= 1
                second_cycle += 1

            pygame.display.flip()

        # ______________________________________________________________________________________________________________

        # After the round - high scores handler ________________________________________________________________________
        colour_longest_snake_round = None
        colour_most_opponent_hits_round = None
        colour_most_points_eaten_round = None

        for head in heads_match:

            if len(head.following_particles) > longest_snake_round[0]:
                longest_snake_round = [len(head.following_particles), head.player.player_name,
                                       head.player.set_name]
                colour_longest_snake_round = head.colour

        for head in heads_match_non_remove:
            if head.opponent_hits > most_opponent_hits_round[0]:
                most_opponent_hits_round = [head.opponent_hits, head.player.player_name, head.player.set_name]
                colour_most_opponent_hits_round = head.colour

        for head in heads_match_non_remove:
            if head.points_eaten > most_points_eaten_round[0]:
                most_points_eaten_round = [head.points_eaten, head.player.player_name, head.player.set_name]
                colour_most_points_eaten_round = head.colour

        if longest_snake_round[0] > high_scores_list["LongestSnake"]["score"]:
            high_scores_list["LongestSnake"]["score"] = longest_snake_round[0]
            if longest_snake_round[2]:
                high_scores_list["LongestSnake"]["player"] = longest_snake_round[1]

            else:

                # Name prompt___________________________________________________________________________________________

                name_prompt_text = NamePromptText(light_font_for_name_prompt, longest_snake_round[1], white)
                name_prompt_running = True
                pygame.mouse.set_visible(True)

                while name_prompt_running:

                    input_text = TextInput("", "game_fonts\Montserrat-ExtraLight.ttf", int(40 * u), True, white, white,
                                           400, 35)

                    text_write_flag = False

                    running_text = True

                    while running_text:
                        events = pygame.event.get()
                        for event in events:

                            if event.type == MOUSEBUTTONDOWN:
                                running_text = False
                                text_write_flag = True

                            if event.type == KEYDOWN:

                                if event.key == K_ESCAPE:

                                    running_text = False
                                    text_write_flag = True

                                if event.key == K_RETURN:
                                    running_text = False

                        name_prompt.render(screen, colour_longest_snake_round)
                        name_prompt_text.render(screen)

                        input_text.update(events)
                        screen.blit(input_text.get_surface(), (710 * u, 560 * u))

                        pygame.display.update()

                    text_input_in_list_form = list(input_text.get_text())

                    invalid_input_flag = True
                    for character in text_input_in_list_form:
                        if character != " ":
                            invalid_input_flag = False

                    if len(text_input_in_list_form) > 10:
                        invalid_input_flag = True

                    if not text_write_flag and input_text.get_text() != "" and not invalid_input_flag:
                        high_scores_list["LongestSnake"]["player"] = input_text.get_text()
                        name_prompt_running = False
                    pygame.display.flip()

                # ______________________________________________________________________________________________________

        if most_opponent_hits_round[0] > high_scores_list["OpponentHits"]["score"]:

            high_scores_list["OpponentHits"]["score"] = most_opponent_hits_round[0]

            if most_opponent_hits_round[2]:
                high_scores_list["OpponentHits"]["player"] = most_opponent_hits_round[1]

            else:

                # Name prompt___________________________________________________________________________________________

                name_prompt_text = NamePromptText(light_font_for_name_prompt, most_opponent_hits_round[1], white)
                name_prompt_running = True
                pygame.mouse.set_visible(True)

                while name_prompt_running:
                    input_text = TextInput("", "game_fonts\Montserrat-ExtraLight.ttf", int(40 * u), True, white, white,
                                           400, 35)

                    text_write_flag = False

                    running_text = True

                    while running_text:
                        events = pygame.event.get()
                        for event in events:

                            if event.type == MOUSEBUTTONDOWN:
                                running_text = False
                                text_write_flag = True

                            if event.type == KEYDOWN:

                                if event.key == K_ESCAPE:
                                    running_text = False
                                    text_write_flag = True

                                if event.key == K_RETURN:
                                    running_text = False

                        name_prompt.render(screen, colour_most_opponent_hits_round)
                        name_prompt_text.render(screen)

                        input_text.update(events)
                        screen.blit(input_text.get_surface(), (710 * u, 560 * u))

                        pygame.display.update()

                    text_input_in_list_form = list(input_text.get_text())

                    invalid_input_flag = True
                    for character in text_input_in_list_form:
                        if character != " ":
                            invalid_input_flag = False

                    if len(text_input_in_list_form) > 10:
                        invalid_input_flag = True

                    if not text_write_flag and input_text.get_text() != "" and not invalid_input_flag:
                        high_scores_list["OpponentHits"]["player"] = input_text.get_text()
                        name_prompt_running = False

                    pygame.display.flip()

                # ______________________________________________________________________________________________________

        if most_points_eaten_round[0] > high_scores_list["MostPointsEaten"]["score"]:
            high_scores_list["MostPointsEaten"]["score"] = most_points_eaten_round[0]
            if most_points_eaten_round[2]:
                high_scores_list["MostPointsEaten"]["player"] = most_points_eaten_round[1]

            else:

                # Name prompt___________________________________________________________________________________________

                pygame.mouse.set_visible(True)
                name_prompt_text = NamePromptText(light_font_for_name_prompt, most_points_eaten_round[1], white)
                name_prompt_running = True

                while name_prompt_running:
                    input_text = TextInput("", "game_fonts\Montserrat-ExtraLight.ttf", int(40 * u), True, white, white,
                                           400, 35)

                    text_write_flag = False

                    running_text = True

                    while running_text:
                        events = pygame.event.get()
                        for event in events:

                            if event.type == MOUSEBUTTONDOWN:
                                running_text = False
                                text_write_flag = True

                            if event.type == KEYDOWN:

                                if event.key == K_ESCAPE:
                                    running_text = False
                                    text_write_flag = True

                                if event.key == K_RETURN:
                                    running_text = False

                        name_prompt.render(screen, colour_most_points_eaten_round)
                        name_prompt_text.render(screen)

                        input_text.update(events)
                        screen.blit(input_text.get_surface(), (710 * u, 560 * u))

                        pygame.display.update()

                    text_input_in_list_form = list(input_text.get_text())

                    invalid_input_flag = True
                    for character in text_input_in_list_form:
                        if character != " ":
                            invalid_input_flag = False

                    if len(text_input_in_list_form) > 10:
                        invalid_input_flag = True

                    if not text_write_flag and input_text.get_text() != "" and not invalid_input_flag:
                        high_scores_list["MostPointsEaten"]["player"] = input_text.get_text()
                        name_prompt_running = False

                    pygame.display.flip()

                # ______________________________________________________________________________________________________

        with open("high_scores.json", "w") as high_scores_json:
            json.dump(high_scores_list, high_scores_json)

        # ______________________________________________________________________________________________________________

    # __________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________
pygame.quit()
