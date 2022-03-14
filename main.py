import pygame
import sys

from settings import *
from tictactoe import TicTacToe
from menu import Menu, Button


class Game:
    def __init__(self):
        self.status = 'game'
        self.tictactoe = TicTacToe(screen, 'normal', self.create_menu)
        self.start_menu = Menu(screen,
							   "Tic Tac Toe",
							   [
								   Button(screen,
										  self.create_simple_computer_tictactoe, "Jouer contre ordinateur simple", 400, 50),
								   Button(screen,
										  self.create_expert_computer_tictactoe, "Jouer contre ordinateur expert", 400, 50),
								   Button(screen,
										  self.create_jcj_tictactoe, "Joueur contre joueur", 400, 50),
								   Button(screen,
										  self.create_menu, "Stats", 400, 50),
								   Button(screen,
										  self.create_menu, "Dernière partie", 400, 50),
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
                                          self.create_simple_computer_tictactoe, "Jouer contre ordinateur simple", 400, 50),
                                   Button(screen,
                                          self.create_expert_computer_tictactoe, "Jouer contre ordinateur expert", 400, 50),
                                   Button(screen,
                                          self.create_jcj_tictactoe, "Joueur contre joueur", 400, 50),
                                   Button(screen,
                                          self.create_menu, "Stats", 400, 50),
                                   Button(screen,
                                          self.create_menu, "Dernière partie", 400, 50),
                                   Button(screen,
                                          self.quit_game, "Quitter", 400, 50)
                               ])
        self.status = 'menu'

    def create_jcj_tictactoe(self):
        self.tictactoe = TicTacToe(screen, 'jcj', self.create_menu)
        self.status = 'game'

    def create_simple_computer_tictactoe(self):
        self.tictactoe = TicTacToe(screen, 'simple computer', self.create_menu)
        self.status = 'game'

    def create_expert_computer_tictactoe(self):
        self.tictactoe = TicTacToe(screen, 'expert computer', self.create_menu)
        self.status = 'game'

    def run(self):
        if self.status == 'menu':
            self.start_menu.run()
        else:
            self.tictactoe.run()


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
