import pygame
import random
import string

pygame.init()
screen = pygame.display.set_mode((800,1000))
screen.fill((20, 150, 255))
pygame.display.set_caption("Tower of Babel")
clock = pygame.time.Clock()
game_title_font = pygame.font.SysFont("Comic Sans MS", 50)
game_small_font = pygame.font.SysFont("Comic Sans MS", 30)
bricks_placed = 0
bricks = 0
clay = 0

'''
all of my decrative and gameplay sprites
'''
# a sprite for the ground
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r".\Graphics\Ground.png").convert_alpha()
        self.rect = self.image.get_rect(bottomleft=(0, 1000))

# a sprite for the tower, which changes its image as more bricks are placed
class Tower(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        Tower_Full = pygame.image.load(r".\Graphics\Tower\Tower_Full.png").convert_alpha()
        Tower_LV6 = pygame.image.load(r".\Graphics\Tower\Tower_LV6.png").convert_alpha()
        Tower_LV5 = pygame.image.load(r".\Graphics\Tower\Tower_LV5.png").convert_alpha()
        Tower_LV4 = pygame.image.load(r".\Graphics\Tower\Tower_LV4.png").convert_alpha()
        Tower_LV3 = pygame.image.load(r".\Graphics\Tower\Tower_LV3.png").convert_alpha()
        Tower_LV2 = pygame.image.load(r".\Graphics\Tower\Tower_LV2.png").convert_alpha()
        Tower_LV1 = pygame.image.load(r".\Graphics\Tower\Tower_LV1.png").convert_alpha()
        Tower_Gone = pygame.image.load(r".\Graphics\Tower\Tower_Gone.png").convert_alpha()
        self.tower_index = 0
        self.tower_states = [Tower_Gone, Tower_LV1, Tower_LV2, Tower_LV3, Tower_LV4, Tower_LV5, Tower_LV6, Tower_Full]
        self.image = self.tower_states[self.tower_index]
        self.rect = self.image.get_rect(bottomleft=(200, 900))
        self.growth_veriable = 0
    
    def place_brick(self):
        global bricks
        global bricks_placed
        if bricks > 0:
            bricks -= 1
            bricks_placed += 1
    
    def update_tower(self):
        global bricks_placed
        if bricks_placed >= 3 ** self.growth_veriable and self.tower_index < 7:
            self.tower_index += 1
            self.image = self.tower_states[self.tower_index]
            self.growth_veriable += 1

# a sprite for the clay pile, which the player can click to gather clay
class Clay_Pile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r".\Graphics\Clay_Pile.png").convert_alpha()
        self.rect = self.image.get_rect(bottomleft=(50, 925))
        self.change_clay = 1
    
    def gather_clay(self):
        global clay
        clay += self.change_clay
    
    def upgrade_clay_amount(self):
        global clay
        if clay >= 10 ** self.change_clay: # the cost of the upgrade increases exponentially based on how many times the player has upgraded the clay amount
            clay -= 10 ** self.change_clay
            self.change_clay += 1

# a sprite for the brick pile, which changes its image as more bricks are made and can be clicked to make bricks from clay
class Brick_Pile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        Bricks_0 = pygame.image.load(r".\Graphics\Brick_Pile\Brick_Pile_0.png").convert_alpha()
        Bricks_1 = pygame.image.load(r".\Graphics\Brick_Pile\Brick_Pile_1.png").convert_alpha()
        Bricks_2 = pygame.image.load(r".\Graphics\Brick_Pile\Brick_Pile_2.png").convert_alpha()
        Bricks_3 = pygame.image.load(r".\Graphics\Brick_Pile\Brick_Pile_3.png").convert_alpha()
        Bricks_4 = pygame.image.load(r".\Graphics\Brick_Pile\Brick_Pile_4.png").convert_alpha()
        Bricks_5 = pygame.image.load(r".\Graphics\Brick_Pile\Brick_Pile_5.png").convert_alpha()
        Bricks_6 = pygame.image.load(r".\Graphics\Brick_Pile\Brick_Pile_6.png").convert_alpha()
        Bricks_7 = pygame.image.load(r".\Graphics\Brick_Pile\Brick_Pile_7.png").convert_alpha()
        Bricks_8 = pygame.image.load(r".\Graphics\Brick_Pile\Brick_Pile_8.png").convert_alpha()
        self.brick_pile_index = 0
        self.brick_pile_states = [Bricks_0, Bricks_1, Bricks_2, Bricks_3, Bricks_4, Bricks_5, Bricks_6, Bricks_7, Bricks_8]
        self.image = self.brick_pile_states[self.brick_pile_index]
        self.rect = self.image.get_rect(bottomleft=(650,925))
        self.pending_actions = []
        self.delay = 30000  # delay in milliseconds
        self.drying_time_level = 1
    
    def make_brick(self):
        global clay
        global bricks
        if clay > 0 and self.brick_pile_index < 8:
            clay -= 1
            if self.brick_pile_index < 8:
                self.brick_pile_index += 1
                self.image = self.brick_pile_states[self.brick_pile_index]
        self.pending_actions.append(pygame.time.get_ticks())
    
    def give_brick(self):
        global bricks
        if self.brick_pile_index > 0:
            bricks += 1
            self.brick_pile_index -= 1
            self.image = self.brick_pile_states[self.brick_pile_index]
    
    def reduce_brick_drying_time(self):
            global clay
            global bricks
            brick_cost = 10 * (2 ** (self.drying_time_level - 1))  # exponential cost increase for each level
            clay_cost = brick_cost * 3 # clay cost is 3 times the brick cost
            reduction_amount = self.delay * 0.05  # reduce drying time by 5%
            if clay >= clay_cost and bricks >= brick_cost and self.delay - reduction_amount >= 1000:  # check if player can afford the upgrade and if it doesn't reduce the delay below 1 second
                clay -= clay_cost
                bricks -= brick_cost
                self.drying_time_level += 1
                self.delay =  self.delay - reduction_amount
'''
all of my button sprites
'''
# a sprite for the start button on the title screen
class Start_Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r".\Graphics\Buttons\Start_Button.png").convert_alpha()
        self.rect = self.image.get_rect(center=(400, 300))

# a sprite for the options button on the title screen
class Main_Options_Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r".\Graphics\Buttons\Options_Button.png").convert_alpha()
        self.rect = self.image.get_rect(center=(400, 400))

# a sprite for the credits button on the title screen
class Credits_Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r".\Graphics\Buttons\Credits_Button.png").convert_alpha()
        self.rect = self.image.get_rect(center=(400, 500))

# a sprite for the exit button on the options screen
class Exit_Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r".\Graphics\Buttons\Exit_Button.png").convert_alpha()
        self.rect = self.image.get_rect(center=(400, 300))

# a sprite for the back button on the options screen
class Options_Back_Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r".\Graphics\Buttons\Back_Button.png").convert_alpha()
        self.rect = self.image.get_rect(center=(400, 400))

# a sprite for the back button on the credits screen
class Credits_Back_Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r".\Graphics\Buttons\Back_Button.png").convert_alpha()
        self.rect = self.image.get_rect(center=(400, 400))

# a sprite for the pause button on the play screen
class Pause_Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r".\Graphics\Buttons\Pause_Button.png").convert_alpha()
        self.rect = self.image.get_rect(center=(40, 40))

# a sprite for the main menu button on the pause screen
class Main_Menu_Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r".\Graphics\Buttons\Main_Menu_Button.png").convert_alpha()
        self.rect = self.image.get_rect(center=(400, 300))

# a sprite for the options button on the pause screen
class Pause_Options_Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r".\Graphics\Buttons\Options_Button.png").convert_alpha()
        self.rect = self.image.get_rect(center=(400, 400))

# a sprite for the back button in the pause screen
class Pause_Back_Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r".\Graphics\Buttons\Back_Button.png").convert_alpha()
        self.rect = self.image.get_rect(center=(400, 500))

# a sprite for the button that brings the player to the upgrade screen
class Upgrade_Screen_Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r".\Graphics\Buttons\Upgrade_Screen_Button.png").convert_alpha()
        self.rect = self.image.get_rect(center=(760, 40))

# a sprite for the back button on the upgrade screen
class Upgrade_Screen_Back_Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r".\Graphics\Buttons\Back_Button.png").convert_alpha()
        self.rect = self.image.get_rect(center=(400, 800))

# a sprite for the clay amount upgrade button on the upgrade screen
class Upgrade_Clay_Amount_Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r".\Graphics\Buttons\Clay_Amount_Button.png").convert_alpha()
        self.rect = self.image.get_rect(center=(200, 300))

# a sprite for the brick drying time upgrade button on the upgrade screen
class Upgrade_Brick_Drying_Time_Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r".\Graphics\Buttons\Brick_Time_Button.png").convert_alpha()
        self.rect = self.image.get_rect(center=(600, 300))

'''
all of my text sprites
'''
# a sprite for the title text on the title screen
class Title(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = game_title_font.render("Tower of Babel", True, (255, 255, 255))
        self.rect = self.image.get_rect(center=(400, 100))

# a sprite for the title text on the options screen
class Options_Title(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = game_title_font.render("Options", True, (255, 255, 255))
        self.rect = self.image.get_rect(center=(400, 100))

# a sprite for the credits title on the credits screen
class Credits_Title(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = game_title_font.render("Credits", True, (255, 255, 255))
        self.rect = self.image.get_rect(center=(400, 100))

# a sprite for the credits text on the credits screen
class Credits_Text(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = game_title_font.render("Made by: Afton Jones", True, (255, 255, 255))
        self.rect = self.image.get_rect(center=(400, 300))

# a sprite for the bricks placed counter on the play screen
class Bricks_Placed_Counter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = game_small_font.render("Bricks placed: " + str(bricks_placed), True, (0, 0, 0))
        self.rect = self.image.get_rect(bottomleft=(10, 125))
    
    def update_bricks_placed(self):
        global bricks_placed
        self.image = game_small_font.render("Bricks placed: " + str(bricks_placed), True, (0, 0, 0))

# a sprite for the clay counter on the play screen
class Clay_Counter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = game_small_font.render("Clay: " + str(clay), True, (0, 0, 0))
        self.rect = self.image.get_rect(bottomleft=(10, 175))
    
    def update_clay(self):
        global clay
        self.image = game_small_font.render("Clay: " + str(clay), True, (0, 0, 0))

# a sprite for the bricks counter on the play screen
class Bricks_Counter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = game_small_font.render("Bricks: " + str(bricks), True, (0, 0, 0))
        self.rect = self.image.get_rect(bottomleft=(10, 225))
    
    def update_bricks(self):
        global bricks
        self.image = game_small_font.render("Bricks: " + str(bricks), True, (0, 0, 0))

def create_environment():
    environment = pygame.sprite.Group()
    environment.add(Ground())
    environment.add(Tower())
    return environment

def create_play_area():
    play_area = pygame.sprite.Group()
    tower = Tower()
    bricks_placed_counter = Bricks_Placed_Counter()
    bricks_counter = Bricks_Counter()
    clay_counter = Clay_Counter()
    clay_pile = Clay_Pile()
    brick_pile = Brick_Pile()
    pause_button = Pause_Button()
    upgrade_button = Upgrade_Screen_Button()
    play_area.add(pause_button)
    play_area.add(upgrade_button)
    play_area.add(tower)
    play_area.add(bricks_placed_counter)
    play_area.add(bricks_counter)
    play_area.add(clay_counter)
    play_area.add(clay_pile)
    play_area.add(brick_pile)
    return play_area, pause_button, upgrade_button, tower, bricks_placed_counter, clay_counter, bricks_counter, clay_pile, brick_pile
def create_start_screen():
    start_screen = pygame.sprite.Group()
    start_screen.add(Title())
    start_screen.add(Start_Button())
    start_screen.add(Main_Options_Button())
    start_screen.add(Credits_Button())
    return start_screen

def create_main_options_screen():
    options_screen = pygame.sprite.Group()
    options_screen.add(Options_Title())
    options_screen.add(Exit_Button())
    options_screen.add(Options_Back_Button())
    return options_screen

def create_credits_screen():
    credits_screen = pygame.sprite.Group()
    credits_screen.add(Credits_Title())
    credits_screen.add(Credits_Text())
    credits_screen.add(Credits_Back_Button())
    return credits_screen

def create_pause_screen():
    pause_screen = pygame.sprite.Group()
    pause_screen.add(Title())
    pause_screen.add(Main_Menu_Button())
    pause_screen.add(Pause_Options_Button())
    pause_screen.add(Pause_Back_Button())
    return pause_screen

def create_options_pause_screen():
    options_pause_screen = pygame.sprite.Group()
    options_pause_screen.add(Options_Title())
    options_pause_screen.add(Exit_Button())
    options_pause_screen.add(Options_Back_Button())
    return options_pause_screen

def create_upgrade_screen():
    upgrade_screen = pygame.sprite.Group()
    upgrade_back_button = Upgrade_Screen_Back_Button()
    upgrade_brick_counter = Bricks_Counter()
    upgrade_clay_counter = Clay_Counter()
    clay_amount_button = Upgrade_Clay_Amount_Button()
    brick_drying_time_button = Upgrade_Brick_Drying_Time_Button()
    upgrade_screen.add(upgrade_back_button)
    upgrade_screen.add(upgrade_brick_counter)
    upgrade_screen.add(upgrade_clay_counter)
    upgrade_screen.add(clay_amount_button)
    upgrade_screen.add(brick_drying_time_button)
    return upgrade_screen, upgrade_back_button, upgrade_brick_counter, upgrade_clay_counter, clay_amount_button, brick_drying_time_button

''' 
determins which screen to draw
1 = start screen
2 = play area
3 = options screen
4 = credits screen
5 = pause screen
6 = options pause screen
7 = upgrade screen
'''
mode = 1

# creates all the mode screens before the main game loop so that they dont have to be created every frame, only drawn
environment = create_environment()
play_area, pause_button, upgrade_button, tower, bricks_placed_counter, clay_counter, bricks_counter, clay_pile, brick_pile = create_play_area()
start_screen = create_start_screen()
options_screen = create_main_options_screen()
credits_screen = create_credits_screen()
pause_screen = create_pause_screen()
options_pause_screen = create_options_pause_screen()
upgrade_screen, upgrade_back_button, upgrade_brick_counter, upgrade_clay_counter, clay_amount_button, brick_drying_time_button = create_upgrade_screen()

# main game loop, draws a new frame every 1/60th of a second
while True:

    current_time = pygame.time.get_ticks()

    # draw start screen
    if mode == 1:
        screen.fill((20, 150, 255))
        environment.draw(screen)
        start_screen.draw(screen)
    # draw game play area
    elif mode == 2:
        screen.fill((20, 150, 255))
        environment.draw(screen)
        play_area.draw(screen)
    # draw options screen
    elif mode == 3:
        screen.fill((20, 150, 255))
        environment.draw(screen)
        options_screen.draw(screen)
    # draw credits screen
    elif mode == 4:
        screen.fill((20, 150, 255))
        environment.draw(screen)
        credits_screen.draw(screen)
    # draw pause screen
    elif mode == 5:
        screen.fill((20, 150, 255))
        environment.draw(screen)
        pause_screen.draw(screen)
    # draw options pause screen
    elif mode == 6:
        screen.fill((20, 150, 255))
        environment.draw(screen)
        options_pause_screen.draw(screen)
    elif mode == 7:
        screen.fill((20, 150, 255))
        environment.draw(screen)
        upgrade_screen.draw(screen)
    # check for player inputs relating to clicking the mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if mode == 1:
                if start_screen.sprites()[1].rect.collidepoint(mouse_pos):
                    mode = 2
                elif start_screen.sprites()[2].rect.collidepoint(mouse_pos):
                    mode = 3
                elif start_screen.sprites()[3].rect.collidepoint(mouse_pos):
                    mode = 4
            elif mode == 2:
                if pause_button.rect.collidepoint(mouse_pos):
                    mode = 5
                if upgrade_button.rect.collidepoint(mouse_pos):
                    mode = 7
                if clay_pile.rect.collidepoint(mouse_pos):
                    clay_pile.gather_clay()
                    clay_counter.update_clay()
                    upgrade_clay_counter.update_clay()
                if tower.rect.collidepoint(mouse_pos):
                    tower.place_brick()
                    bricks_counter.update_bricks()
                    upgrade_brick_counter.update_bricks()
                    bricks_placed_counter.update_bricks_placed()
                    tower.update_tower()
                if brick_pile.rect.collidepoint(mouse_pos):
                    brick_pile.make_brick()
                    clay_counter.update_clay()
                    upgrade_clay_counter.update_clay()
            elif mode == 3:
                if options_screen.sprites()[1].rect.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()
                elif options_screen.sprites()[2].rect.collidepoint(mouse_pos):
                    mode = 1
            elif mode == 4:
                if credits_screen.sprites()[2].rect.collidepoint(mouse_pos):
                    mode = 1
            elif mode == 5:
                if pause_screen.sprites()[1].rect.collidepoint(mouse_pos):
                    mode = 1
                elif pause_screen.sprites()[2].rect.collidepoint(mouse_pos):
                    mode = 6
                elif pause_screen.sprites()[3].rect.collidepoint(mouse_pos):
                    mode = 2
            elif mode == 6:
                if options_pause_screen.sprites()[1].rect.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()
                elif options_pause_screen.sprites()[2].rect.collidepoint(mouse_pos):
                    mode = 5
            elif mode == 7:
                if upgrade_back_button.rect.collidepoint(mouse_pos):
                    mode = 2
                elif clay_amount_button.rect.collidepoint(mouse_pos):
                    clay_pile.upgrade_clay_amount()
                    clay_counter.update_clay()
                    upgrade_clay_counter.update_clay()
                elif brick_drying_time_button.rect.collidepoint(mouse_pos):
                    brick_pile.reduce_brick_drying_time()
                    clay_counter.update_clay()
                    upgrade_clay_counter.update_clay()
                    bricks_counter.update_bricks()
                    upgrade_brick_counter.update_bricks()
    
    # check for pending actions in the brick pile and execute them if their delay has passed
    for action_time in brick_pile.pending_actions:
        if current_time - action_time >= brick_pile.delay:
            brick_pile.pending_actions.remove(action_time)
            brick_pile.give_brick()
            bricks_counter.update_bricks()
            upgrade_brick_counter.update_bricks()
    # update everything
    pygame.display.update()
    clock.tick(60)
