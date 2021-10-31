import pygame.time

from menu import *


# Main Game Function
def main():
    # Runtime Loop
    game_running = True
    while game_running:
        # Run & get Info From Main Menu, Check for Quit Option
        menu_out = main_menu()
        if menu_out is False:
            return False

        # Setting Up Player One
        player_one = Player(Game.player_one_name, Game.width / 3, Game.height / 2, Game.player_one_rgb,
                            pygame.K_a,
                            pygame.K_d,
                            pygame.K_w,
                            pygame.K_s)

        # Setting Up Player Two
        player_two = Player(Game.player_two_name, Game.width / 3 * 2, Game.height / 2, Game.player_two_rgb,
                            pygame.K_j,
                            pygame.K_l,
                            pygame.K_i,
                            pygame.K_k)

        # Defining Powers Parameters
        speed = Speed_power('images/power_speed.png', player_one, player_two,
                            1 / 10000 if Game.power_speed_activation is True else 0, 5, 0.2)
        size = Size_power('images/power_size.png', player_one, player_two,
                          1 / 10000 if Game.power_size_activation is True else 0, 5, 0.5)
        infinity = Infinity_power('images/power_infinity.png', player_one, player_two,
                                  1 / 10000 if Game.power_infinity_activation is True else 0, 2, 0.5)
        invisibility = Invisibility_power('images/power_invisibility.png', player_one, player_two,
                                          1 / 10000 if Game.power_invisibility_activation is True else 0, 1, 0.5)

        # Initializing Runtime Variables
        keep_playing = True
        running = True
        current_round = True

        # Main Loop
        while running:

            # Game Victory Handling
            if player_two.points >= Game.max_points:
                blit_point_bar(player_one, player_two)
                centered_message(f'{Game.last_round_winner} Wins the Game!')
                pygame.display.update()
                t.sleep(Game.sleep_time)
                centered_message(f'Press SPACEBAR to Exit the Game', y_displacement=Game.height / 6)
                pygame.display.update()
                Game.player_two_victories += 1
                space_bar_initiation()
                break
            elif player_one.points >= Game.max_points:
                blit_point_bar(player_one, player_two)
                centered_message(f'{Game.last_round_winner} Wins the Game!')
                pygame.display.update()
                t.sleep(Game.sleep_time)
                centered_message(f'Press SPACEBAR to Exit the Game', y_displacement=Game.height / 6)
                pygame.display.update()
                Game.player_one_victories += 1
                space_bar_initiation()
                break

            # Blitting Round Winner & New Round Starting
            if Game.last_round_winner != '':
                centered_message(f'{Game.last_round_winner} Wins the Round!')
                blit_point_bar(player_one, player_two)
                pygame.display.update()
                t.sleep(Game.sleep_time)
                centered_message(f'Press SPACEBAR to Continue', y_displacement=Game.height / 6)
                pygame.display.update()
                pygame.event.clear()
                keep_playing = space_bar_initiation()

            # Initializing New Round
            if keep_playing is True:
                Game.current_score = 0
                Game.current_turn += 1
                player_two.reset()
                player_one.reset()
                blit_arena()
                blit_stat_bar()
                blit_point_bar(player_one, player_two)
                blit_score_bar()
                blit_time_bar(Game.max_time)
                player_two.draw_player()
                player_one.draw_player()
                blit_score_player(player_one, player_two)
                who_text_blit(player_one, player_two)
                centered_message(f'Round {Game.current_turn}!')
                pygame.display.update()
                t.sleep(Game.sleep_time)
                centered_message(f'Press SPACEBAR to Start the Round', y_displacement=Game.height / 6)
                pygame.display.update()
                pygame.event.clear()
                keep_playing = space_bar_initiation()

                # Checking For Exit & Main Menu
                if keep_playing is True:
                    Game.ini_time_start = t.time()
                elif keep_playing == 'main_menu':
                    Game.menu_back.play()
                    running = False
                    current_round = False
                else:
                    return None

            # Checking For Exit & Main Menu
            elif keep_playing == 'main_menu':
                Game.menu_back.play()
                running = False
                current_round = False
            else:
                return None

            # Initializing Runtime Variables
            loop_time = 0

            # Round Loop
            while current_round:
                # Starting Time
                loop_start_time = pygame.time.get_ticks()

                # Giving Game Exit option
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return None
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            Game.menu_back.play()
                            running = False
                            current_round = False

                # Filling Arena
                blit_arena()

                # Running Powers
                speed.run_power(loop_time)
                size.run_power(loop_time)
                infinity.run_power(loop_time)
                invisibility.run_power(loop_time)

                # Detecting Keys & Moving Player
                pressed = call_keys()
                player_two.move(pressed, loop_time)
                player_one.move(pressed, loop_time)

                # Player Physics
                player_two.player_physics()
                player_one.player_physics()

                # Awarding points
                if distance(player_two.get_position(), player_one.get_position()) < (
                        player_two.circle_radius + player_one.circle_radius):
                    increase_score(loop_time)
                    # Playing Sound
                    if pygame.mixer.get_busy() == 0:
                        Game.sound_touch.play()

                # Blitting Players & Moving Score
                if Game.current_turn % 2 == 0:
                    player_one.draw_player()
                    player_two.draw_player()
                    blit_score_player(player_one, player_two)
                else:
                    player_two.draw_player()
                    player_one.draw_player()
                    blit_score_player(player_one, player_two)

                # Blitting Status
                blit_stat_bar()
                power_cool_cycle(player_one, [size, speed, infinity, invisibility], Game.power_status_p1_start,
                                 Game.status_bar_height_half)
                power_cool_cycle(player_two, [size, speed, infinity, invisibility], Game.power_status_p2_start,
                                 Game.status_bar_height_half)
                who_text_blit(player_one, player_two)

                # Display Time & Score
                blit_point_bar(player_one, player_two)
                blit_score_bar()
                blit_time_bar(round(Game.max_time + Game.ini_time_start - t.time(), 2))

                # Updating Display
                pygame.display.update()

                # Checking for Round Victory by Score
                if Game.current_score >= Game.max_score:
                    if Game.current_turn % 2 != 0:
                        player_one.give_point()
                        Game.last_round_winner = player_one.name
                    else:
                        player_two.give_point()
                        Game.last_round_winner = player_two.name
                    break
                # Checking for Round Victory by Time
                elif (Game.max_time + Game.ini_time_start - t.time()) <= 0:
                    if Game.current_turn % 2 != 0:
                        player_two.give_point()
                        Game.last_round_winner = player_two.name
                    else:
                        player_one.give_point()
                        Game.last_round_winner = player_one.name
                    break

                # Calculating Loop Time
                loop_time = pygame.time.get_ticks() - loop_start_time

        # Resetting General Settings
        Game.current_score = 0
        Game.current_turn = 0
        Game.last_round_winner = ''


# Execute Main function when called
if __name__ == '__main__':
    main()
