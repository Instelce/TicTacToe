import pygame
import sys

from settings import *
from level import Level
from menu import Menu, Button


class Game:
    def __init__(self):
        self.status = 'menu'
        self.level = Level(screen)
        self.start_menu = Menu(screen,
                               "Tic Tac Toe",
                               [
                                    Button(screen,
                                          self.create_level, "Jouer contre ordinateur simple", 400, 50),
                                    Button(screen,
                                          self.create_level, "Jouer contre ordinateur expert", 400, 50),
                                    Button(screen,
                                          self.create_level, "Joueur contre joueur", 400, 50),
                                    Button(screen,
                                          self.create_level, "Stats", 400, 50),
                                    Button(screen,
                                          self.create_level, "Dernière partie", 400, 50),
                                   Button(screen,
                                          self.quit_game, "Quitter", 400, 50)
                               ])

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def create_menu(self):
        self.start_menu = Menu(screen,
                               "Tic Tac Toe",
                               [
                                   Button(screen,
                                          self.create_level, "Jouer ", 200, 50),
                                   Button(screen,
                                          self.create_level, "Settings", 200, 50),
                                   Button(screen,
                                          self.quit_game, "Quit", 200, 50)
                               ],
                               "graphics/ui/start_menu_banner.png",)
        self.status = 'menu'

    def create_level(self):
        self.level = Level(screen)
        self.status = 'level'

    def run(self):
        if self.status == 'menu':
            self.start_menu.run()
        else:
            self.level.run()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tic Tac toe")
clock = pygame.time.Clock()
game = Game()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('white')
    game.run()

    pygame.display.update()
    clock.tick(60)