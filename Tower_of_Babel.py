import pygame
import random
import string

pygame.init()
screen = pygame.display.set_mode((800,1000))
screen.fill((20, 150, 255))
pygame.display.set_caption("Tower of Babel")
clock = pygame.time.Clock()
game_font = pygame.font.SysFont("Comic Sans MS", 50)

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r".\Graphics\Ground.png").convert_alpha()
        self.rect = self.image.get_rect(bottomleft=(0, 1000))

class Start_Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r".\Graphics\Start_Button.png").convert_alpha()
        self.rect = self.image.get_rect(center=(400, 300))

class Title(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = game_font.render("Tower of Babel", True, (255, 255, 255))
        self.rect = self.image.get_rect(center=(400, 100))

def create_environment():
    environment = pygame.sprite.Group()
    environment.add(Ground())
    environment.draw(screen)
    return environment

def create_start_screen():
    start_screen = pygame.sprite.Group()
    start_screen.add(Title())
    start_screen.add(Start_Button())
    start_screen.draw(screen)
    return start_screen

# main game loop, draws a new frame every 1/60th of a second
while True:
    # check for player input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # draw all elements
    environment = create_environment()
    start_screen = create_start_screen()
    # update everything
    pygame.display.update()
    clock.tick(60)
