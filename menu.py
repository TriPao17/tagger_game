from game_mechanics import *


# Credits Menu
def credits_menu():
    # Runtime Loop
    running = True
    while running:
        # Blitting Background
        Game.screen.fill(Game.background_color)

        # Blitting Credits
        centered_message('Michel De Buren', y_displacement=-Game.height / 3)
        centered_message('Eloïse Robyr')
        centered_message('Paolo Trifoni', y_displacement=Game.height / 3)

        # Drawing Backward Arrow
        arrow_rect = arrow_polygon_draw((Game.width / 15, Game.height / 15), Game.details_color, flipped=True)

        # Checking for Events
        for event in pygame.event.get():
            # Quit Option
            if event.type == pygame.QUIT:
                return False

            # Checking for Key Inputs
            if event.type == pygame.KEYDOWN:
                if key_menu_back(event):
                    Game.menu_back.play()
                    return None

            # Checking for Mouse Inputs
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if arrow_rect.collidepoint(event.pos):
                    Game.menu_back.play()
                    return None

        # Updating Display
        pygame.display.update()


# Player Option Menu
def player_options_menu():
    # Offsets
    offset = Game.height / 10
    box_offset = Game.width / 4
    ini_offset = 4 * offset
    offset_w_p1 = Game.width / 7
    offset_w_p2 = Game.width - Game.width / 7 - box_offset

    # Converting Tuples to Lists
    Game.player_one_rgb = list(Game.player_one_rgb)
    Game.player_two_rgb = list(Game.player_two_rgb)

    # Player One
    p1_name = input_text('Name: ', Game.player_one_name, offset_w_p1, ini_offset + 0 * offset, box_offset)
    p1_R = input_text('R: ', Game.player_one_rgb[0], offset_w_p1, ini_offset + 1 * offset, box_offset, max_char=3,
                      rtype='rgb')
    p1_G = input_text('G: ', Game.player_one_rgb[1], offset_w_p1, ini_offset + 2 * offset, box_offset, max_char=3,
                      rtype='rgb')
    p1_B = input_text('B: ', Game.player_one_rgb[2], offset_w_p1, ini_offset + 3 * offset, box_offset, max_char=3,
                      rtype='rgb')
    p1_preview_text = Game.font.render('Preview: ', True, Game.font_color)

    # Player Two
    p2_name = input_text('Name: ', Game.player_two_name, offset_w_p2, ini_offset + 0 * offset, box_offset)
    p2_R = input_text('R: ', Game.player_two_rgb[0], offset_w_p2, ini_offset + 1 * offset, box_offset, max_char=3,
                      rtype='rgb')
    p2_G = input_text('G: ', Game.player_two_rgb[1], offset_w_p2, ini_offset + 2 * offset, box_offset, max_char=3,
                      rtype='rgb')
    p2_B = input_text('B: ', Game.player_two_rgb[2], offset_w_p2, ini_offset + 3 * offset, box_offset, max_char=3,
                      rtype='rgb')
    p2_preview_text = Game.font.render('Preview: ', True, Game.font_color)

    # Runtime Loop
    running = True
    while running:
        # Blitting Background
        Game.screen.fill(Game.background_color)

        # Player One Blitting
        centered_message('Player One', x_displacement=-Game.width / 2 + offset_w_p1 + box_offset / 2,
                         y_displacement=-Game.height / 2 + Game.height / 5)
        p1_name.blit()
        p1_R.blit()
        p1_G.blit()
        p1_B.blit()
        Game.screen.blit(p1_preview_text, (offset_w_p1, ini_offset + 4 * offset - p1_preview_text.get_size()[1]))
        draw_circle(Game.screen, offset_w_p1 + box_offset - 50,
                    ini_offset + 4 * offset - p1_preview_text.get_size()[1] / 2, Game.circle_radius,
                    tuple(Game.player_one_rgb))

        # Player Two Blitting
        centered_message('Player Two', x_displacement=-Game.width / 2 + offset_w_p2 + box_offset / 2,
                         y_displacement=-Game.height / 2 + Game.height / 5)
        p2_name.blit()
        p2_R.blit()
        p2_G.blit()
        p2_B.blit()
        Game.screen.blit(p2_preview_text, (offset_w_p2, ini_offset + 4 * offset - p1_preview_text.get_size()[1]))
        draw_circle(Game.screen, offset_w_p2 + box_offset - 50,
                    ini_offset + 4 * offset - p2_preview_text.get_size()[1] / 2, Game.circle_radius,
                    tuple(Game.player_two_rgb))

        # Arrow Blitting
        arrow_rect = arrow_polygon_draw((Game.width / 15, Game.height / 15), Game.details_color, flipped=True)

        # Checking For Events
        for event in pygame.event.get():
            # Quit Option
            if event.type == pygame.QUIT:
                return False

            # Checking fot Key Inputs
            if event.type == pygame.KEYDOWN:
                if key_menu_back(event):
                    Game.menu_back.play()
                    Game.player_one_rgb = tuple(Game.player_one_rgb)
                    Game.player_two_rgb = tuple(Game.player_two_rgb)
                    return None
            # Checking for Mouse Clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if arrow_rect.collidepoint(event.pos):
                    Game.menu_back.play()
                    Game.player_one_rgb = tuple(Game.player_one_rgb)
                    Game.player_two_rgb = tuple(Game.player_two_rgb)
                    return None

            # Player One Detection
            Game.player_one_name = p1_name.run_detect(event)
            Game.player_one_rgb[0] = p1_R.run_detect(event)
            Game.player_one_rgb[1] = p1_G.run_detect(event)
            Game.player_one_rgb[2] = p1_B.run_detect(event)

            # Player Two Detection
            Game.player_two_name = p2_name.run_detect(event)
            Game.player_two_rgb[0] = p2_R.run_detect(event)
            Game.player_two_rgb[1] = p2_G.run_detect(event)
            Game.player_two_rgb[2] = p2_B.run_detect(event)

        # Updating Display
        pygame.display.update()


def gameplay_options_menu():
    # Offsets
    ini_offset_adjustment = Game.height / 12
    offset = Game.height / 10
    box_offset = Game.width / 3
    ini_offset = 4 * offset + ini_offset_adjustment
    offset_w_powers = Game.width / 9
    offset_w_gameplay = Game.width - offset_w_powers - box_offset

    # Powers
    power_infinity = input_bool('Infinity: ', offset_w_powers, ini_offset + 0 * offset, box_offset,
                                default_input=("On" if Game.power_infinity_activation is True else "Off"))
    power_speed = input_bool('Speed: ', offset_w_powers, ini_offset + 1 * offset, box_offset,
                             default_input=("On" if Game.power_speed_activation is True else "Off"))
    power_invisibility = input_bool('Invisibility: ', offset_w_powers, ini_offset + 2 * offset, box_offset,
                                    default_input=("On" if Game.power_invisibility_activation is True else "Off"))
    power_size = input_bool('Size: ', offset_w_powers, ini_offset + 3 * offset, box_offset,
                            default_input=("On" if Game.power_size_activation is True else "Off"))

    # Gameplay
    time_round = input_text('Time: ', Game.max_time, offset_w_gameplay, ini_offset + 0 * offset, box_offset, 3,
                            rtype='int')
    score_round = input_text('Score: ', Game.max_score, offset_w_gameplay, ini_offset + 1 * offset, box_offset,
                             3, rtype='int')
    points_game = input_text('Points: ', Game.max_points, offset_w_gameplay, ini_offset + 2 * offset, box_offset,
                             1, rtype='int')
    speed_player = input_text('Player Speed: ', Game.movement_size, offset_w_gameplay, ini_offset + 3 * offset,
                              box_offset, 3, rtype='float')

    # Runtime Loop
    running = True
    while running:
        # Blitting Background
        Game.screen.fill(Game.background_color)

        # Powers Settings Blitting
        centered_message('Powers', x_displacement=-Game.width / 2 + offset_w_powers + box_offset / 2,
                         y_displacement=-Game.height / 2 + Game.height / 5 + ini_offset_adjustment)
        power_infinity.blit()
        power_speed.blit()
        power_size.blit()
        power_invisibility.blit()

        # Gameplay Settings Blitting
        centered_message('Gameplay', x_displacement=-Game.width / 2 + offset_w_gameplay + box_offset / 2,
                         y_displacement=-Game.height / 2 + Game.height / 5 + ini_offset_adjustment)
        time_round.blit()
        score_round.blit()
        points_game.blit()
        speed_player.blit()

        # Arrow Blitting
        arrow_rect = arrow_polygon_draw((Game.width / 15, Game.height / 15), Game.details_color, flipped=True)

        # Checking for Events
        for event in pygame.event.get():
            # Quit Option
            if event.type == pygame.QUIT:
                return False

            # Checking for Key Inputs
            elif event.type == pygame.KEYDOWN:
                if key_menu_back(event):
                    Game.menu_back.play()
                    return None

            # Checking for Mouse Clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if arrow_rect.collidepoint(event.pos):
                    Game.menu_back.play()
                    return None

            # Powers Settings Detection
            Game.power_infinity_activation = power_infinity.run_detect(event)
            Game.power_speed_activation = power_speed.run_detect(event)
            Game.power_size_activation = power_size.run_detect(event)
            Game.power_invisibility_activation = power_invisibility.run_detect(event)

            # Gameplay Settings Detection
            Game.max_time = time_round.run_detect(event)
            Game.max_score = score_round.run_detect(event)
            Game.max_points = max(1, points_game.run_detect(event))
            Game.movement_size = speed_player.run_detect(event)

        # Updating Display
        pygame.display.update()


# Style Options Menu
def style_options_menu():
    # Offsets
    ini_offset_adjustment = Game.height / 12
    offset = Game.height / 10
    box_offset = Game.width / 6
    ini_offset = 4 * offset + ini_offset_adjustment
    offset_w_background = Game.width / 10
    offset_w_details = Game.width / 2 - box_offset / 2
    offset_w_font = Game.width - Game.width / 10 - box_offset

    # Background
    background_R = input_text('R: ', Game.background_color[0], offset_w_background, ini_offset + 0 * offset, box_offset,
                              max_char=3, rtype='rgb')
    background_G = input_text('G: ', Game.background_color[1], offset_w_background, ini_offset + 1 * offset, box_offset,
                              max_char=3, rtype='rgb')
    background_B = input_text('B: ', Game.background_color[2], offset_w_background, ini_offset + 2 * offset, box_offset,
                              max_char=3, rtype='rgb')

    # Details
    details_R = input_text('R: ', Game.details_color[0], offset_w_details, ini_offset + 0 * offset, box_offset,
                           max_char=3, rtype='rgb')
    details_G = input_text('G: ', Game.details_color[1], offset_w_details, ini_offset + 1 * offset, box_offset,
                           max_char=3, rtype='rgb')
    details_B = input_text('B: ', Game.details_color[2], offset_w_details, ini_offset + 2 * offset, box_offset,
                           max_char=3, rtype='rgb')

    # Font
    font_R = input_text('R: ', Game.font_color[0], offset_w_font, ini_offset + 0 * offset, box_offset, max_char=3,
                        rtype='rgb')
    font_G = input_text('G: ', Game.font_color[1], offset_w_font, ini_offset + 1 * offset, box_offset, max_char=3,
                        rtype='rgb')
    font_B = input_text('B: ', Game.font_color[2], offset_w_font, ini_offset + 2 * offset, box_offset, max_char=3,
                        rtype='rgb')

    # Runtime Loop
    running = True
    while running:
        # Filling Background
        Game.screen.fill(Game.background_color)

        # Backward Arrow
        arrow_rect = arrow_polygon_draw((Game.width / 15, Game.height / 15), Game.details_color, flipped=True)

        # Background Settings Blitting
        centered_message('Background', x_displacement=-Game.width / 2 + offset_w_background + box_offset / 2,
                         y_displacement=-Game.height / 2 + Game.height / 5 + ini_offset_adjustment)
        background_R.blit()
        background_G.blit()
        background_B.blit()

        # Details Settings Blitting
        centered_message('Details', x_displacement=-Game.width / 2 + offset_w_details + box_offset / 2,
                         y_displacement=-Game.height / 2 + Game.height / 5 + ini_offset_adjustment)
        details_R.blit()
        details_G.blit()
        details_B.blit()

        # Font Settings Blitting
        centered_message('Font', x_displacement=-Game.width / 2 + offset_w_font + box_offset / 2,
                         y_displacement=-Game.height / 2 + Game.height / 5 + ini_offset_adjustment)
        font_R.blit()
        font_G.blit()
        font_B.blit()

        # Checking for Events
        for event in pygame.event.get():
            # Quit Option
            if event.type == pygame.QUIT:
                return False

            # Checking for Mouse Clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if arrow_rect.collidepoint(event.pos):
                    Game.menu_back.play()
                    return None

            # Checking for Key Inputs
            elif event.type == pygame.KEYDOWN:
                if key_menu_back(event):
                    Game.menu_back.play()
                    return None

            # Converting to lists
            Game.background_color = list(Game.background_color)
            Game.details_color = list(Game.background_color)
            Game.font_color = list(Game.background_color)

            # Background Color Detection
            Game.background_color[0] = background_R.run_detect(event)
            Game.background_color[1] = background_G.run_detect(event)
            Game.background_color[2] = background_B.run_detect(event)

            # Details Color Detection
            Game.details_color[0] = details_R.run_detect(event)
            Game.details_color[1] = details_G.run_detect(event)
            Game.details_color[2] = details_B.run_detect(event)

            # Details Color Detection
            Game.font_color[0] = font_R.run_detect(event)
            Game.font_color[1] = font_G.run_detect(event)
            Game.font_color[2] = font_B.run_detect(event)

            # Dynamically Changing
            Game.background_color = tuple(Game.background_color)
            Game.details_color = tuple(Game.details_color)
            Game.font_color = tuple(Game.font_color)

        # Updating Display
        pygame.display.update()


# Options Menu
def which_options_menu():
    # Runtime Loop
    running = True
    while running:
        # Filling Background
        Game.screen.fill(Game.background_color)

        # Getting Rects & Blitting Options
        rects = options_blit_all()

        # Setting Selection Position
        options_set_y_pos()

        # Drawing Circles for Selection
        draw_circle(Game.screen, Game.options_menu_x, Game.options_menu_y, Game.circle_radius, Game.player_one_rgb)
        draw_circle(Game.screen, 2 * Game.options_menu_x, Game.options_menu_y, Game.circle_radius, Game.player_two_rgb)

        # Drawing Backward Arrow
        arrow_rect = arrow_polygon_draw((Game.width / 15, Game.height / 15), Game.details_color, flipped=True)

        # Total Victories
        blit_total_points((Game.options_menu_x, Game.options_menu_y), Game.player_one_victories, Game.player_one_rgb)
        blit_total_points((2 * Game.options_menu_x, Game.options_menu_y), Game.player_two_victories,
                          Game.player_two_rgb)

        # Checking for Events
        for event in pygame.event.get():
            # Quit Option
            if event.type == pygame.QUIT:
                return False

            # Checking for Mouse Clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Click Player Options
                if rects[0].collidepoint(event.pos):
                    Game.menu_enter.play()
                    if player_options_menu() is False:
                        return False

                # Click Gameplay Options
                elif rects[1].collidepoint(event.pos):
                    Game.menu_enter.play()
                    if gameplay_options_menu() is False:
                        return False

                # Click Style Options
                elif rects[2].collidepoint(event.pos):
                    Game.menu_enter.play()
                    if style_options_menu() is False:
                        return False

                # Click Backward Arrow
                elif arrow_rect.collidepoint(event.pos):
                    if pygame.mixer.get_busy() == 0:
                        Game.menu_back.play()
                        return None

            # Checking for Mouse Hovers
            if event.type == pygame.MOUSEMOTION:
                # Mouse Hovers Player Options
                if rects[0].collidepoint(event.pos):
                    if pygame.mixer.get_busy() == 0 and Game.options_menu_selected != 0:
                        Game.menu_change.play()
                    Game.options_menu_selected = 0

                # Mouse Hovers Gameplay Options
                elif rects[1].collidepoint(event.pos):
                    if pygame.mixer.get_busy() == 0 and Game.options_menu_selected != 1:
                        Game.menu_change.play()
                    Game.options_menu_selected = 1

                # Mouse Hovers Style Options
                elif rects[2].collidepoint(event.pos):
                    if pygame.mixer.get_busy() == 0 and Game.options_menu_selected != 2:
                        Game.menu_change.play()
                    Game.options_menu_selected = 2

            # Checking for Key Inputs
            if event.type == pygame.KEYDOWN:
                # Go Back
                if key_menu_back(event):
                    Game.menu_back.play()
                    return None

                # Move Selection Down
                if key_menu_down(event):
                    if Game.options_menu_selected >= Game.options_n_options - 1:
                        pass
                    else:
                        Game.options_menu_selected += 1
                        Game.menu_change.play()

                # Move Selection Up
                elif key_menu_up(event):
                    if Game.options_menu_selected <= 0:
                        pass
                    else:
                        Game.options_menu_selected -= 1
                        Game.menu_change.play()

                # Go Forward
                elif key_menu_forward(event):
                    # Enter Player Options
                    if Game.options_menu_selected == 0:
                        Game.menu_enter.play()
                        if player_options_menu() is False:
                            return False

                    # Enter Gameplay Options
                    elif Game.options_menu_selected == 1:
                        Game.menu_enter.play()
                        if gameplay_options_menu() is False:
                            return False

                    # Enter Style Options
                    elif Game.options_menu_selected == 2:
                        Game.menu_enter.play()
                        if style_options_menu() is False:
                            return False

        # Display Update
        pygame.display.update()


# Main Menu
def main_menu():
    # Runtime Loop
    running = True
    while running:
        # Setting Selection Position
        menu_set_y_pos()

        # Blitting all Options and Retrieving all Rects
        rects = menu_blit_all()

        # Drawing Circles For Selection
        draw_circle(Game.screen, Game.main_menu_x, Game.main_menu_y, Game.circle_radius, Game.player_one_rgb)
        draw_circle(Game.screen, 2 * Game.main_menu_x, Game.main_menu_y, Game.circle_radius, Game.player_two_rgb)

        # Total Victories
        blit_total_points((Game.main_menu_x, Game.main_menu_y), Game.player_one_victories, Game.player_one_rgb)
        blit_total_points((2 * Game.main_menu_x, Game.main_menu_y), Game.player_two_victories, Game.player_two_rgb)

        # Checking for Events
        for event in pygame.event.get():
            # Quit Option
            if event.type == pygame.QUIT:
                return False

            # Checking For Mouse Clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Start Game
                if rects[0].collidepoint(event.pos):
                    Game.menu_enter.play()
                    return None

                # Go to Options Menu
                elif rects[1].collidepoint(event.pos):
                    Game.menu_enter.play()
                    if which_options_menu() is False:
                        return False

                # Go to Credits Page
                elif rects[2].collidepoint(event.pos):
                    Game.menu_enter.play()
                    if credits_menu() is False:
                        return False

                # Quit
                elif rects[3].collidepoint(event.pos):
                    Game.menu_enter.play()
                    return False

            # Checking For Mouse Hovers
            if event.type == pygame.MOUSEMOTION:
                # Mouse Hovers Player Start Game
                if rects[0].collidepoint(event.pos):
                    if pygame.mixer.get_busy() == 0 and Game.main_menu_selected != 0:
                        Game.menu_change.play()
                    Game.main_menu_selected = 0

                # Mouse Hovers Options Menu
                elif rects[1].collidepoint(event.pos):
                    if pygame.mixer.get_busy() == 0 and Game.main_menu_selected != 1:
                        Game.menu_change.play()
                    Game.main_menu_selected = 1

                # Mouse Hovers Credits Page
                elif rects[2].collidepoint(event.pos):
                    if pygame.mixer.get_busy() == 0 and Game.main_menu_selected != 2:
                        Game.menu_change.play()
                    Game.main_menu_selected = 2

                # Mouse Hovers Quit
                elif rects[3].collidepoint(event.pos):
                    if pygame.mixer.get_busy() == 0 and Game.main_menu_selected != 3:
                        Game.menu_change.play()
                    Game.main_menu_selected = 3

            # Checking for Key Inputs
            if event.type == pygame.KEYDOWN:
                # Move Selection Down
                if key_menu_down(event):
                    if Game.main_menu_selected >= Game.menu_n_options - 1:
                        pass
                    else:
                        Game.main_menu_selected += 1
                        Game.menu_change.play()

                # Move Selection Up
                elif key_menu_up(event):
                    if Game.main_menu_selected <= 0:
                        pass
                    else:
                        Game.main_menu_selected -= 1
                        Game.menu_change.play()

                # Go Forward
                elif key_menu_forward(event):
                    # Start Game
                    Game.menu_enter.play()
                    if Game.main_menu_selected == 0:
                        return None

                    # Launch Options Menu
                    elif Game.main_menu_selected == 1:
                        if which_options_menu() is False:
                            return False

                    # Launch Credits Page
                    elif Game.main_menu_selected == 2:
                        if credits_menu() is False:
                            return False

                    # Quit
                    elif Game.main_menu_selected == 3:
                        return False

        # Update Display
        pygame.display.update()
