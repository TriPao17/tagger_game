import time as t

import numpy as np
import pygame
from pygame import gfxdraw


class Game:
    # Initialising Pygame
    pygame.init()

    # Loading Settings
    width = 1200  # Original 1200
    height = round(width * (700 / 1200))  # Original 700
    movement_size = round(width / 1500, 2)
    circle_radius = round(width / 48)
    circle_diameter = circle_radius * 2
    touch_distance = circle_diameter
    sleep_time = 1

    # Colors
    dark_fact = 4
    background_color = (248, 237, 227)  # Original (214, 211, 243)
    details_color = (162, 178, 159)  # Original (100, 100, 100)
    font_color = (
        round(details_color[0] / dark_fact), round(details_color[1] / dark_fact), round(details_color[2] / dark_fact))
    bar_separator_color = background_color
    icon_alpha = 100
    player_one_rgb = (2, 106, 255)
    player_two_rgb = (255, 21, 64)

    # Initializing Scores & Turns
    current_score = 0
    current_turn = 0
    last_round_winner = ''

    # Game Time & Score settings
    max_time = 30
    max_score = 100
    max_points = 3
    ini_time_start = 0

    # Status Bar
    status_bar_height = circle_diameter
    status_bar_height_half = round(status_bar_height / 2)
    stat_bar = pygame.Surface((width, status_bar_height))
    stat_bar.fill(details_color)

    # Points Bar
    point_bar = pygame.Surface((width, status_bar_height))
    point_bar.fill(details_color)

    # Points Bar Paddings-H
    pad_size = int(status_bar_height / 8)
    point_bar_pad_h = pygame.Surface((width, pad_size))
    point_bar_pad_h.fill(details_color)

    # Points Bar Paddings-V
    point_bar_pad_v = pygame.Surface((pad_size, status_bar_height))
    point_bar_pad_v.fill(details_color)
    point_bar_pad_v_size = point_bar_pad_v.get_size()

    # Defining Arena
    arena = pygame.Surface((width, height - 2 * status_bar_height))
    arena.fill(background_color)

    # Setting up screen & Standard Font
    screen = pygame.display.set_mode((width, height))
    font = pygame.font.Font('JetBrains_Mono_Static/JetBrainsMono-SemiBold.ttf', 32)
    font_score_player = pygame.font.Font('JetBrains_Mono_Static/JetBrainsMono-SemiBold.ttf', 24)

    # Setting Up Name & Logo
    logo = pygame.transform.scale(pygame.image.load('images/game_icon.png'), (32, 32))
    logo.convert_alpha()
    pygame.display.set_icon(logo)
    pygame.display.set_caption('Tagger')

    # Sound
    pygame.mixer.init()
    sound_touch = pygame.mixer.Sound('sounds/sound_game_touch.mp3')
    sound_power = pygame.mixer.Sound('sounds/sound_game_power.mp3')
    menu_change = pygame.mixer.Sound('sounds/sound_menu_select.mp3')
    menu_enter = pygame.mixer.Sound('sounds/sound_menu_enter.mp3')
    menu_back = pygame.mixer.Sound('sounds/sound_menu_back.mp3')

    # Powers
    power_despawn_time = 3
    power_status_pad = round(circle_diameter * 1.1)
    power_status_radius = round(circle_radius * 0.6)
    power_status_size = 3 * power_status_pad + 2 * power_status_radius
    power_status_p1_start = round(width / 4) - power_status_size / 2
    power_status_p2_start = 3 * round(width / 4) - power_status_size / 2

    # Powers-Active
    power_speed_activation = True
    power_size_activation = True
    power_infinity_activation = True
    power_invisibility_activation = True

    # Names
    player_one_name = 'Blue'
    player_two_name = 'Red'

    # Total Victories
    player_one_victories = 0
    player_two_victories = 0

    # Menu-Title
    title_font = pygame.font.Font('JetBrains_Mono_Static/JetBrainsMono-SemiBold.ttf', 80)

    title_main_menu_surface = title_font.render('TAGGER', True, font_color)
    title_main_menu_surface_pads = title_main_menu_surface.get_size()
    title_main_menu_x = width / 2 - title_main_menu_surface_pads[0] / 2
    title_main_menu_y = height / 3 - title_main_menu_surface_pads[1] / 2

    title_options_menu_surface = title_font.render('OPTIONS', True, font_color)
    title_options_menu_surface_pads = title_options_menu_surface.get_size()
    title_options_menu_x = width / 2 - title_options_menu_surface_pads[0] / 2
    title_options_menu_y = height / 3 - title_options_menu_surface_pads[1] / 2

    # Menu-Options
    offset = round(height / 8)
    start_game_y = 0
    options_y = offset
    credits_y = 2 * offset
    quit_y = 3 * offset
    menu_n_options = 4

    # Options-Options
    offset = round(height / 8)
    players_y = 0
    gameplay_y = offset
    style_y = 2 * offset
    options_n_options = 3

    # Selected
    main_menu_selected = 0
    options_menu_selected = 1

    # Cursor Position in Main Menu
    main_menu_x = width / 3
    main_menu_y = height / 2 + main_menu_selected * offset

    # Cursor Position in Options Menu
    options_menu_x = width / 3
    options_menu_y = height / 2 + main_menu_selected * offset


# Function that draws an Anti-aliased Filled Circle
def draw_circle(surface, x, y, radius, color):
    gfxdraw.aacircle(surface, round(x), round(y), radius, color)
    gfxdraw.filled_circle(surface, round(x), round(y), radius, color)


# Defining function that Gets the key which are currently pressed
def call_keys():
    return pygame.key.get_pressed()


# Function that increases the score
def increase_score(dt):
    Game.current_score += (dt / 5)


# Function that calculates a poisson probability
def poisson_prob(lam, T, k):
    return 1 - (np.math.pow(lam * T, k) / np.math.factorial(k)) * np.math.exp(- lam * T)


# Defining Player Class (inherits from game)
class Player(Game):
    # Initialising
    def __init__(self, name, start_x, start_y, rgb, left_key, right_key, up_key, down_key):
        # Name & Text to Blit
        self.name = name
        self.name_text = Game.font.render(self.name, True, Game.font_color)
        self.name_text_pad_h = (Game.status_bar_height - self.name_text.get_size()[1]) / 2
        self.name_text_pad_w_one = (Game.width - Game.width / 10) / 2 - self.name_text.get_size()[0]
        self.name_text_pad_w_two = (Game.width - Game.width / 10) / 2 + Game.width / 10

        # Coordinates
        self.start_x = round(start_x)
        self.start_y = round(start_y)
        self.x = self.start_x
        self.y = self.start_y

        # Colors
        self.rgb = rgb
        self.rgb_darkened = tuple([x / Game.dark_fact for x in list(self.rgb)])
        self.rgb_alpha = self.rgb + (self.icon_alpha,)

        # Points
        self.points = 0

        # Keys
        self.LEFT = left_key
        self.RIGHT = right_key
        self.UP = up_key
        self.DOWN = down_key

        # Powers
        self.player_powers = {
            'speed': {'active': False, 'time': 0},
            'size': {'active': False, 'time': 0},
            'infinity': {'active': False, 'time': 0},
            'invisibility': {'active': False, 'time': 0}}

    # Get Player Coordinates
    def get_position(self):
        return [self.x, self.y]

    # Move Player Horizontally
    def move_horizontal(self, direction, time_step):
        self.x += direction * self.movement_size * time_step

    # Move Player Vertically
    def move_vertical(self, direction, time_step):
        self.y += direction * self.movement_size * time_step

    # Move Player Diagonally-Left
    def move_diagonal_left(self, direction, time_step):
        self.x -= self.movement_size * time_step / np.sqrt(2)
        self.y += direction * (self.movement_size * time_step / np.sqrt(2))

    # Move Player Diagonally-Right
    def move_diagonal_right(self, direction, time_step):
        self.x += self.movement_size * time_step / np.sqrt(2)
        self.y += direction * (self.movement_size * time_step / np.sqrt(2))

    # Reset Player Attributes
    def reset(self):
        # Positions
        self.x = self.start_x
        self.y = self.start_y

        # Size & Speed
        self.circle_radius = Game.circle_radius
        self.movement_size = Game.movement_size

        # Powers
        self.player_powers = {
            'speed': {'active': False, 'time': 0},
            'size': {'active': False, 'time': 0},
            'infinity': {'active': False, 'time': 0},
            'invisibility': {'active': False, 'time': 0}}

    # Drawing Player to Screen
    def draw_player(self):
        # Checking If invisibility Power is Active
        if self.player_powers['invisibility']['active'] is False:
            # Drawing
            draw_circle(self.screen, self.x, self.y, self.circle_radius, self.rgb)

    # Awarding Points
    def give_point(self):
        self.points += 1

    # Defining Continuous Playground Physics
    def continuous_playground(self):
        if self.x > self.width:
            self.x = 0
        elif self.x < 0:
            self.x = self.width
        if self.y > self.height - self.status_bar_height:
            self.y = self.status_bar_height
        elif self.y < self.status_bar_height:
            self.y = self.height - self.status_bar_height

    # Defining Fixed Playground Physics
    def fixed_playground(self):
        if self.x > self.width - 1 - self.circle_radius:
            self.x = self.width - 1 - self.circle_radius
        elif self.x < self.circle_radius:
            self.x = self.circle_radius
        if self.y > self.height - self.circle_radius - 1 - self.status_bar_height:
            self.y = self.height - self.circle_radius - 1 - self.status_bar_height
        elif self.y < self.status_bar_height + self.circle_radius:
            self.y = self.status_bar_height + self.circle_radius

    # Choosing Player Physics to Execute
    def player_physics(self):
        # Checking If Infinity Power is In-Active
        if self.player_powers['infinity']['active'] is False:
            self.fixed_playground()
        else:
            self.continuous_playground()

    # Capturing Pressed Keys Moving Player
    def move(self, pressed, time_step):
        # LEFT & Other
        if pressed[self.LEFT]:
            if pressed[self.UP]:
                self.move_diagonal_left(-1, time_step)
            elif pressed[self.DOWN]:
                self.move_diagonal_left(1, time_step)
            else:
                self.move_horizontal(-1, time_step)

        # RIGHT & Other
        elif pressed[self.RIGHT]:
            if pressed[self.UP]:
                self.move_diagonal_right(-1, time_step)
            elif pressed[self.DOWN]:
                self.move_diagonal_right(1, time_step)
            else:
                self.move_horizontal(1, time_step)

        # UP & Other
        elif pressed[self.UP]:
            if pressed[self.LEFT]:
                self.move_diagonal_left(-1, time_step)
            elif pressed[self.RIGHT]:
                self.move_diagonal_right(1, time_step)
            else:
                self.move_vertical(-1, time_step)

        # DOWN & Other
        elif pressed[self.DOWN]:
            if pressed[self.LEFT]:
                self.move_diagonal_left(1, time_step)
            elif pressed[self.RIGHT]:
                self.move_diagonal_right(-1, time_step)
            else:
                self.move_vertical(1, time_step)


# Distance Calculation
def distance(object_one, object_two):
    return ((object_one[0] - object_two[0]) ** 2 + (object_one[1] - object_two[1]) ** 2) ** 0.5


# Defining Power Class (inherits from game)
class Powers(Game):
    # Initialising
    def __init__(self, image, player_one, player_two, probability, duration, enhancement_factor):
        # Images & Icon
        self.image_raw = pygame.image.load(image).convert()
        self.image = pygame.transform.scale(self.image_raw,
                                            (int(self.circle_diameter * 0.6), int(self.circle_diameter * 0.6)))
        self.image.set_colorkey((255, 255, 255))
        self.image_small = pygame.transform.scale(self.image_raw,
                                                  (int(self.circle_diameter * 0.3), int(self.circle_diameter * 0.3)))
        self.image_small.set_colorkey((255, 255, 255))
        self.icon_size = self.image.get_size()
        self.icon_size_small = self.image_small.get_size()

        # Power Settings
        self.probability = probability
        self.duration = duration
        self.enhancement_factor = enhancement_factor

        # Players
        self.player_one = player_one
        self.player_two = player_two

        # Declaring Position (Initial/None)
        self.x = None
        self.y = None

        # Declaring Runtime Variables
        self.displayed = False
        self.start_time = None
        self.target_power = None

    # Generating Random Spawn Position
    def generate_position(self):
        self.x = round(np.random.uniform(self.circle_radius + self.status_bar_height,
                                         self.width - self.circle_radius - self.status_bar_height))
        self.y = round(np.random.uniform(self.circle_radius + self.status_bar_height,
                                         self.height - self.circle_radius - self.status_bar_height))

    # Get The Generated Spawned Position
    def get_position(self):
        return [self.x, self.y]

    # Blitting Spawned Power to Screen
    def blit_power(self):
        self.screen.blit(self.image, (self.x - self.icon_size[0] / 2, self.y - self.icon_size[1] / 2))
        gfxdraw.aacircle(Game.screen, self.x, self.y, self.circle_radius, (0, 0, 0))

    # Starting Timer for de-Spawning
    def start_timer(self):
        self.start_time = t.time()

    # Power Activation Sequence (TBD in SubClass)
    def activate_power(self, player_spec):
        pass

    # Power de-Activation Sequence (TBD in SubClass)
    def de_activate_power(self, player_spec):
        pass

    # Executing Power
    def run_power(self, dt):
        # If Power is not currently Spawned
        if self.displayed is False:
            if np.random.uniform(0, 1) <= poisson_prob(self.probability, dt, 0):
                self.generate_position()
                self.blit_power()
                self.start_timer()
                self.displayed = True

        # If Power is currently Spawned
        else:
            # Blit Spawned Power to Screen
            self.blit_power()

            # Handling Player One Getting the Spawned Power
            if distance(self.player_one.get_position(), self.get_position()) < (
                    self.player_one.circle_radius + self.player_two.circle_radius):
                self.sound_power.play()
                self.displayed = False
                self.player_one.player_powers[self.target_power]['active'] = True
                self.player_one.player_powers[self.target_power]['time'] = t.time()
                self.activate_power(self.player_one)

            # Handling Player Two Getting the Spawned Power
            elif distance(self.player_two.get_position(), self.get_position()) < (
                    self.player_one.circle_radius + self.player_two.circle_radius):
                self.sound_power.play()
                self.displayed = False
                self.player_two.player_powers[self.target_power]['active'] = True
                self.player_two.player_powers[self.target_power]['time'] = t.time()
                self.activate_power(self.player_two)

            # Checking If it is time to de-Spawn Spawned Power
            elif t.time() - self.start_time > Game.power_despawn_time:
                self.displayed = False

        # Checking for Deactivation for Player One
        if self.player_one.player_powers[self.target_power]['active'] is True:
            if t.time() - self.player_one.player_powers[self.target_power]['time'] > self.duration:
                self.player_one.player_powers[self.target_power]['active'] = False
                self.player_one.player_powers[self.target_power]['time'] = 0
                self.de_activate_power(self.player_one)

        # Checking for Deactivation for Player Two
        elif self.player_two.player_powers[self.target_power]['active'] is True:
            if t.time() - self.player_two.player_powers[self.target_power]['time'] > self.duration:
                self.player_two.player_powers[self.target_power]['active'] = False
                self.player_two.player_powers[self.target_power]['time'] = 0
                self.de_activate_power(self.player_two)


# Defining Speed Power SubClass (inherits from Power & Game)
class Speed_power(Powers):
    # Initializing
    def __init__(self, image, player_one, player_two, probability, duration, enhancement_factor):
        # Initializing SuperClass Powers
        super().__init__(image, player_one, player_two, probability, duration, enhancement_factor)

        # Overwriting Target Power
        self.target_power = 'speed'

    # Overwriting Activation
    def activate_power(self, player_spec):
        player_spec.movement_size += self.enhancement_factor * Game.movement_size

    # Overwriting de-Activation
    def de_activate_power(self, player_spec):
        player_spec.movement_size = Game.movement_size


class Size_power(Powers):
    # Initializing
    def __init__(self, image, player_one, player_two, probability, duration, enhancement_factor):
        # Initializing SuperClass Powers
        super().__init__(image, player_one, player_two, probability, duration, enhancement_factor)

        # Overwriting Target Power
        self.target_power = 'size'

    # Overwriting Activation
    def activate_power(self, player_spec):
        player_spec.circle_radius += round(self.enhancement_factor * Game.circle_radius)

    # Overwriting de-Activation
    def de_activate_power(self, player_spec):
        player_spec.circle_radius = Game.circle_radius


class Infinity_power(Powers):
    # Initializing
    def __init__(self, image, player_one, player_two, probability, duration, enhancement_factor):
        # Initializing SuperClass Powers
        super().__init__(image, player_one, player_two, probability, duration, enhancement_factor)

        # Overwriting Target Power
        self.target_power = 'infinity'


class Invisibility_power(Powers):
    # Initializing
    def __init__(self, image, player_one, player_two, probability, duration, enhancement_factor):
        # Initializing SuperClass Powers
        super().__init__(image, player_one, player_two, probability, duration, enhancement_factor)

        # Overwriting Target Power
        self.target_power = 'invisibility'


# Function that detects key SPACEBAR presses
def space_bar_initiation():
    # Infinite Loop
    while True:
        # Retrieving Key Presses
        for event in pygame.event.get():
            # SPACEBAR KEY
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True
            # QUIT BUTTON
            elif event.type == pygame.QUIT:
                return False
            # ESCAPE BUTTON
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 'main_menu'


# Blitting to Screen a Centered & Padded Message (Possible Vertical Displacement)
def centered_message(string_in, x_displacement=0, y_displacement=0):
    # Creating Message
    message = Game.font.render(string_in, True, Game.font_color)
    message_size = message.get_size()

    # Creating Message Padding
    message_padding = pygame.Surface((message_size[0] + 0.8 * message_size[1], message_size[1] + 0.8 * message_size[1]))
    message_padding.fill(Game.details_color)
    message_padding.set_alpha(200)
    message_padding_size = message_padding.get_size()

    # Rect
    message_padding_rect = pygame.Rect(((Game.width - message_padding_size[0]) / 2 + x_displacement,
                                        (Game.height - message_padding_size[1]) / 2 + y_displacement,
                                        message_size[0] + 0.8 * message_size[1],
                                        message_size[1] + 0.8 * message_size[1]))

    # Blitting Message & Padding
    Game.screen.blit(message_padding, ((Game.width - message_padding_size[0]) / 2 + x_displacement,
                                       (Game.height - message_padding_size[1]) / 2 + y_displacement))
    Game.screen.blit(message, (
        (Game.width - message_size[0]) / 2 + x_displacement, (Game.height - message_size[1]) / 2 + y_displacement))

    return message_padding_rect


# Blitting Status Bar
def blit_stat_bar():
    Game.stat_bar.fill(Game.details_color)
    Game.screen.blit(Game.stat_bar, (0, 0))


# Blitting Arena
def blit_arena():
    Game.arena.fill(Game.background_color)
    Game.screen.blit(Game.arena, (0, Game.status_bar_height))


# Defining a function which draws an Anti-Aliased filled Arrow
def arrow_polygon_draw(position, color, flipped=False):
    # Arrow Shape Parameters
    body_len = Game.status_bar_height
    start_width = position[0]
    back_draw = 0.2
    thickness = body_len / 10
    start_arrow = position[1]
    start_height = start_arrow + abs(- body_len * back_draw - thickness / (2 ** 0.5))

    # Calculating Resulting Width and Height
    rect_width = abs(start_width - (start_width + body_len + thickness * (2 ** 0.5) + thickness / 2))
    rect_height = abs(
        2 * (start_height + thickness / 2) - (start_height - body_len * back_draw - thickness / (2 ** 0.5)) - (
                start_height - body_len * back_draw - thickness / (2 ** 0.5)))

    # Setting Arrow Direction
    if flipped is True:
        flip = -1
    else:
        flip = 1

    # Calculating Adjusted Starting Width & Height
    start_width = start_width - flip * 0.5 * rect_width
    start_height = start_height - 0.5 * rect_height

    # Calculating All Polygon Point
    a = (start_width, start_height)
    b = (start_width + flip * body_len, start_height)
    c = (start_width + flip * (body_len - body_len * back_draw), start_height - body_len * back_draw)
    d = (start_width + flip * (body_len - body_len * back_draw + thickness / (2 ** 0.5)),
         start_height - body_len * back_draw - thickness / (2 ** 0.5))
    e = (start_width + flip * (body_len + thickness * (2 ** 0.5) + thickness / 2), start_height + thickness / 2)
    f = (start_width + flip * (body_len - body_len * back_draw + thickness / (2 ** 0.5)),
         2 * (start_height + thickness / 2) - (start_height - body_len * back_draw - thickness / (2 ** 0.5)))
    g = (start_width + flip * (body_len - body_len * back_draw),
         2 * (start_height + thickness / 2) - (start_height - body_len * back_draw))
    h = (start_width + flip * body_len, 2 * (start_height + thickness / 2) - start_height)
    i = (start_width, start_height + thickness)

    # Making a list out of Calculated Points
    points = [a, b, c, d, e, f, g, h, i]

    # Drawing the Anti-Aliased Filled Arrow
    gfxdraw.aapolygon(Game.screen, points, color)
    gfxdraw.filled_polygon(Game.screen, points, color)

    # Creating Rect Object
    arrow_rect = pygame.Rect((position[0] - rect_width / 2, position[1] - rect_height / 2, rect_width, rect_height))

    return arrow_rect


# Drawing Active Power Cool-off
def power_cool_cycle(player_sp, power, start_center_x, start_center_y):
    i = 0
    for po in power:
        if player_sp.player_powers[po.target_power]['active'] is True:
            # Center and radius of pie chart
            center_x = start_center_x + Game.power_status_radius + (i * Game.power_status_pad)
            center_y = start_center_y

            # Angle Formed by Remaining Time
            curr_angle = round(
                360 - ((t.time() - player_sp.player_powers[po.target_power]['time']) / po.duration) * 360)

            # Points List - Appending Center
            points_list = [(center_x, center_y)]

            # Points List - Appending Vertices
            for n in range(0, curr_angle):
                n = 360 - n + 90
                x = center_x - int(Game.power_status_radius * np.cos(n * np.pi / 180))
                y = center_y - int(Game.power_status_radius * np.sin(n * np.pi / 180))
                points_list.append((x, y))

            # Points List - Appending Center
            points_list.append((center_x, center_y))

            # Drawing Pie Segment & Power Symbol
            if len(points_list) > 2:
                gfxdraw.filled_polygon(Game.screen, points_list, player_sp.rgb_alpha)
                Game.screen.blit(po.image_small,
                                 (center_x - po.icon_size_small[0] / 2, center_y - po.icon_size_small[1] / 2))
                gfxdraw.aacircle(Game.screen, int(center_x), int(center_y), Game.power_status_radius, (0, 0, 0))
        i += 1


# Blitting Score On Status Bar
def blit_score_bar():
    # Generating Text
    points = Game.font.render('Score: ' + str('%0.0f' % min(Game.current_score, Game.max_score)), True,
                              Game.font_color)

    # Generating Padding
    score_pad = (Game.status_bar_height - (points.get_size())[1]) / 2

    # Blitting to Screen
    Game.screen.blit(points, (score_pad, score_pad))


# Blitting Time On Status Bar
def blit_time_bar(time_left):
    # Generating Text
    time_str = Game.font.render(str('%0.2f' % abs(time_left)), True, Game.font_color)

    # Generating Paddings
    time_pad_h = (Game.status_bar_height - (time_str.get_size())[1]) / 2
    time_pad_w = Game.width - time_str.get_size()[0] - time_pad_h

    # Blitting to Screen
    Game.screen.blit(time_str, (time_pad_w, time_pad_h))


# Blitting Who Chases Who on Status Bar
def who_text_blit(player_one, player_two):
    # Blitting Player Names
    Game.screen.blit(player_one.name_text, (player_one.name_text_pad_w_one, player_one.name_text_pad_h))
    Game.screen.blit(player_two.name_text, (player_two.name_text_pad_w_two, player_two.name_text_pad_h))

    # Blitting Filled Arrow
    if Game.current_turn % 2 == 0:
        arrow_polygon_draw((Game.width / 2, Game.status_bar_height / 2), player_two.rgb, flipped=True)
    else:
        arrow_polygon_draw((Game.width / 2, Game.status_bar_height / 2), player_one.rgb)


# Blitting Time On Status Bar
def blit_score_player(player_one, player_two):
    # Generating Text
    score_to_blit = str('%0.0f' % min(Game.current_score, Game.max_score))

    # Generating Font Color For Each Player
    points_disp_p1 = Game.font_score_player.render(score_to_blit, True, player_one.rgb_darkened)
    points_disp_p2 = Game.font_score_player.render(score_to_blit, True, player_two.rgb_darkened)

    # Generating Paddings
    score_pad_w = (0 - (points_disp_p2.get_size())[0]) / 2
    score_pad_h = (0 - (points_disp_p2.get_size())[1]) / 2

    # Blitting Score On Player which is Chasing & Checking if Invisibility is Active
    if Game.current_turn % 2 == 0 and player_two.player_powers['invisibility']['active'] is False:
        Game.screen.blit(points_disp_p2,
                         (player_two.get_position()[0] + score_pad_w, player_two.get_position()[1] + score_pad_h))
    elif Game.current_turn % 2 != 0 and player_one.player_powers['invisibility']['active'] is False:
        Game.screen.blit(points_disp_p1,
                         (player_one.get_position()[0] + score_pad_w, player_one.get_position()[1] + score_pad_h))


def blit_total_points(loc, player_victories, rgb):
    # Generating Text
    score_to_blit = str('%0.0f' % player_victories)

    # Generating Font Color For Each Player
    victory_disp = Game.font_score_player.render(score_to_blit, True, (
        rgb[0] / Game.dark_fact, rgb[1] / Game.dark_fact, rgb[2] / Game.dark_fact))

    # Generating Paddings
    score_pad_w = (0 - (victory_disp.get_size())[0]) / 2
    score_pad_h = (0 - (victory_disp.get_size())[1]) / 2

    # Blitting Victories on Each Player
    Game.screen.blit(victory_disp, (loc[0] + score_pad_w, loc[1] + score_pad_h))


# Blitting Point Bar
def blit_point_bar(player_one, player_two):
    # Blitting Background
    Game.point_bar.fill(Game.details_color)
    Game.screen.blit(Game.point_bar, (0, Game.height - Game.status_bar_height))

    # Blitting Blue Score
    points_bar_p1 = pygame.Surface(((Game.width / (2 * Game.max_points)) * player_one.points,
                                    Game.status_bar_height))
    points_bar_p1.fill(player_one.rgb)
    Game.screen.blit(points_bar_p1, (0, Game.height - Game.status_bar_height))

    # Blitting Red Score
    points_bar_p2 = pygame.Surface(((Game.width / (2 * Game.max_points)) * player_two.points,
                                    Game.status_bar_height))
    points_bar_p2.fill(player_two.rgb)
    Game.screen.blit(points_bar_p2, (
        Game.width - (Game.width / (2 * Game.max_points)) * player_two.points, Game.height - Game.status_bar_height))

    # Blitting H-Pads
    Game.point_bar_pad_h.fill(Game.details_color)
    Game.screen.blit(Game.point_bar_pad_h, (0, Game.height - Game.status_bar_height))
    Game.screen.blit(Game.point_bar_pad_h, (0, Game.height - Game.pad_size))

    # Blit V-Pads-Blue
    Game.point_bar_pad_v.fill(Game.details_color)
    for i in range(Game.max_points + 1):
        Game.screen.blit(Game.point_bar_pad_v, (
            ((Game.width - 2 * Game.point_bar_pad_v_size[0]) / (2 * Game.max_points)) * i,
            Game.height - Game.status_bar_height))

    # Blit V-Pads-Red
    for i in range(Game.max_points + 1):
        Game.screen.blit(Game.point_bar_pad_v, (
            Game.width / 2 + ((Game.width - 2 * Game.point_bar_pad_v_size[0]) / (2 * Game.max_points)) * i,
            Game.height - Game.status_bar_height))

    # Drawing Vertical Separator
    pygame.draw.line(Game.screen, Game.bar_separator_color, (Game.width / 2, Game.height - Game.status_bar_height),
                     (Game.width / 2, Game.height), 1)


# Blit all Options of Main Menu
def menu_blit_all():
    # Blitting
    Game.screen.fill(Game.background_color)
    Game.screen.blit(Game.title_main_menu_surface, (Game.title_main_menu_x, Game.title_main_menu_y))
    start_game_rect = centered_message('Start Game', y_displacement=Game.start_game_y)
    options_rect = centered_message('Options', y_displacement=Game.options_y)
    credits_rect = centered_message('Credits', y_displacement=Game.credits_y)
    quit_rect = centered_message('Quit', y_displacement=Game.quit_y)

    # Retrieving Rects
    return start_game_rect, options_rect, credits_rect, quit_rect


# Cursor Position in Main Menu
def menu_set_y_pos():
    Game.main_menu_y = Game.height / 2 + Game.main_menu_selected * Game.offset


# Blit all Options of Options Menu
def options_blit_all():
    # Blitting
    Game.screen.fill(Game.background_color)
    Game.screen.blit(Game.title_options_menu_surface, (Game.title_options_menu_x, Game.title_options_menu_y))
    players_rect = centered_message('Players', y_displacement=Game.players_y)
    gameplay_rect = centered_message('Gameplay', y_displacement=Game.gameplay_y)
    style_rect = centered_message('Style', y_displacement=Game.style_y)

    # Retrieving Rects
    return players_rect, gameplay_rect, style_rect


# Cursor Position in Options Menu
def options_set_y_pos():
    Game.options_menu_y = Game.height / 2 + Game.options_menu_selected * Game.offset


# Move Selection Up
def key_menu_up(event):
    if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_i:
        return True


# Move Selection Down
def key_menu_down(event):
    if event.key == pygame.K_DOWN or event.key == pygame.K_s or event.key == pygame.K_k:
        return True


# Move Selection Forward
def key_menu_forward(event):
    if event.key == pygame.K_RIGHT or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
        return True


# Move Selection Backwards
def key_menu_back(event):
    if event.key == pygame.K_LEFT or event.key == pygame.K_ESCAPE:
        return True


# Class for Text Input
class input_text(Game):
    # Initialising
    def __init__(self, field_name, default_input, x_field_left, y_field_left, x_box_right_offset, max_char=4,
                 rtype='str'):
        # Field Name, Sizes & Positions
        self.field_name_one = self.font.render(field_name, True, Game.font_color)
        self.field_name_one_size = self.field_name_one.get_size()
        self.in_rect_width = 100
        self.in_rect_height = self.status_bar_height
        self.total_size_x = self.field_name_one_size[0] + self.in_rect_width
        self.total_size_y = self.field_name_one_size[1] + self.in_rect_height
        self.x_field_left = x_field_left
        self.y_field_left = y_field_left - self.field_name_one_size[1]
        self.x = x_field_left - self.total_size_x / 2
        self.y = y_field_left - self.total_size_y / 2

        # Input Box Shape, Activation, & Color
        self.in_rect = pygame.Rect((self.x_field_left + x_box_right_offset - self.in_rect_width, self.y,
                                    self.in_rect_width, self.in_rect_height))
        self.in_rect_active = False
        self.in_rect_color = None

        # Inputs, Default Input, Return Type of Input & Maximum Characters of Input
        self.default_input = str(default_input)
        self.input = str(default_input)
        self.max_char = max_char
        self.rtype = rtype

    # Checking for Inputs & Activation
    def run_detect(self, event):
        # Checking for Key Inputs
        if event.type == pygame.KEYDOWN:
            if self.in_rect_active is True:
                if event.key == pygame.K_BACKSPACE:
                    self.input = self.input[:-1]
                elif len(self.input) < self.max_char:
                    self.input += event.unicode

        # Checking for Mouse Clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.in_rect.collidepoint(event.pos):
                Game.menu_change.play()
                self.in_rect_active = True
            else:
                self.in_rect_active = False

        # Returning Int Values
        if self.rtype == 'int':
            try:
                return abs(int(self.input))
            except ValueError:
                return int(self.default_input)

        if self.rtype == 'rgb':
            try:
                return min(abs(int(self.input)), 255)
            except ValueError:
                return int(self.default_input)

        # Returning Float Values
        elif self.rtype == 'float':
            try:
                return abs(float(self.input))
            except ValueError:
                return float(self.default_input)

        # Returning String Values
        else:
            return str(self.input)

    # Blitting
    def blit(self):
        # Choosing Color
        if self.in_rect_active is True:
            self.in_rect_color = (255, 255, 255)
        else:
            self.in_rect_color = (200, 200, 200)

        # Blitting Input Box
        pygame.draw.rect(self.screen, self.in_rect_color, self.in_rect)

        # Rendering Font & Calculating Paddings
        text_surface = self.font.render(self.input[0:self.max_char], True, Game.font_color)
        text_pad_size_w = (self.in_rect.width - text_surface.get_size()[0]) / 2
        text_pad_size_h = (self.in_rect.height - text_surface.get_size()[1]) / 2

        # Blitting Text & Field Name
        Game.screen.blit(self.field_name_one, (self.x_field_left, self.y_field_left))
        Game.screen.blit(text_surface, (self.in_rect.x + text_pad_size_w, self.in_rect.y + text_pad_size_h))


# Class for Bool Input
class input_bool(Game):
    # Initialising
    def __init__(self, field_name, x_field_left, y_field_left, x_box_right_offset, default_input='On'):
        # Field Name, Sizes & Positions
        self.field_name_one = self.font.render(field_name, True, Game.font_color)
        self.field_name_one_size = self.field_name_one.get_size()
        self.in_rect_width = 100
        self.in_rect_height = self.status_bar_height
        self.total_size_x = self.field_name_one_size[0] + self.in_rect_width
        self.total_size_y = self.field_name_one_size[1] + self.in_rect_height
        self.x_field_left = x_field_left
        self.y_field_left = y_field_left - self.field_name_one_size[1]
        self.x = x_field_left - self.total_size_x / 2
        self.y = y_field_left - self.total_size_y / 2

        # Input Box Shape, Default Value, Activation, & Color
        self.in_rect = pygame.Rect((self.x_field_left + x_box_right_offset - self.in_rect_width, self.y,
                                    self.in_rect_width, self.in_rect_height))
        self.in_rect_active = False
        self.in_rect_color = None
        self.default_input = str(default_input)

    # Checking for Inputs & Activation
    def run_detect(self, event):
        # Checking for Mouse Clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.in_rect.collidepoint(event.pos):
                Game.menu_change.play()
                self.in_rect_active = True
                if self.default_input == 'On':
                    self.default_input = 'Off'
                else:
                    self.default_input = 'On'
            else:
                self.in_rect_active = False

        # Returning Values
        if self.default_input == 'On':
            return True
        else:
            return False

    # Blitting
    def blit(self):
        # Choosing Color
        if self.in_rect_active is True:
            self.in_rect_color = (255, 255, 255)
        else:
            self.in_rect_color = (200, 200, 200)

        # Blitting Input Box
        pygame.draw.rect(self.screen, self.in_rect_color, self.in_rect)

        # Rendering Font & Calculating Paddings
        text_surface = self.font.render(self.default_input, True, Game.font_color)
        text_pad_size_w = (self.in_rect.width - text_surface.get_size()[0]) / 2
        text_pad_size_h = (self.in_rect.height - text_surface.get_size()[1]) / 2

        # Blitting Text & Field Name
        Game.screen.blit(self.field_name_one, (self.x_field_left, self.y_field_left))
        Game.screen.blit(text_surface, (self.in_rect.x + text_pad_size_w, self.in_rect.y + text_pad_size_h))
