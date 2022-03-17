import pygame
import sys

from settings import *
from tictactoe import TicTacToe
from menu import Menu, Button, Text
from mouse import Mouse


class Game:
    def __init__(self):
        self.mouse = Mouse(screen)
        self.last_time = pygame.time.get_ticks()

        self.status = 'menu'
        self.tictactoe = TicTacToe(screen, 'computer simple', self.mouse, self.create_menu)
        self.start_menu = Menu(screen,
							   "Tic Tac Toe",
							   [
								   Button(screen,
										  self.create_simple_computer_tictactoe, "Jouer contre ordinateur simple", 400, 50, self.mouse),
								   Button(screen,
										  self.create_expert_computer_tictactoe, "Jouer contre ordinateur expert", 400, 50, self.mouse),
								   Button(screen,
										  self.create_jcj_tictactoe, "Joueur contre joueur", 400, 50, self.mouse),
								   Button(screen,
										  self.create_menu, "Stats", 400, 50, self.mouse),
								   Button(screen,
										  self.create_menu, "Dernière partie", 400, 50, self.mouse),
								   Button(screen,
										  self.quit_game, "Quitter", 400, 50, self.mouse)
							   ])

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def create_menu(self):
        self.start_menu = Menu(screen,
                            "Tic Tac Toe",
                            [
                                Button(screen,
                                        self.create_simple_computer_tictactoe, "Jouer contre ordinateur simple", 400, 50, self.mouse),
                                Button(screen,
                                        self.create_expert_computer_tictactoe, "Jouer contre ordinateur expert", 400, 50, self.mouse),
                                Button(screen,
                                        self.create_jcj_tictactoe, "Joueur contre joueur", 400, 50, self.mouse),
                                Button(screen,
                                        self.create_stats_screen, "Stats", 400, 50, self.mouse),
                                Button(screen,
                                        self.create_menu, "Dernière partie", 400, 50, self.mouse),
                                Button(screen,
                                        self.quit_game, "Quitter", 400, 50, self.mouse)
                            ])
        self.status = 'menu'
    
    def create_stats_screen(self):
        self.stats_screen = Menu(screen,
							   "Statistics",
							   [
								   Text("Victory over the simple computer"),
								   Text("Victory over the expert computer"),
								   Text("Number of games played"),
								   Text("Games won by player X"),
								   Text("Games won by player O"),
								   Button(screen,
										  self.create_menu, "Back", 400, 50, self.mouse)
							   ])
        self.status = 'stats_screen'

    def create_jcj_tictactoe(self):
        self.tictactoe = TicTacToe(screen, 'jcj', self.mouse, self.create_menu)
        self.status = 'game'

    def create_simple_computer_tictactoe(self):
        self.tictactoe = TicTacToe(screen, 'computer simple', self.mouse, self.create_menu)
        self.status = 'game'

    def create_expert_computer_tictactoe(self):
        self.tictactoe = TicTacToe(screen, 'computer expert', self.mouse, self.create_menu)
        self.status = 'game'

    def run(self):
        if self.status == 'menu':
            self.start_menu.run()
        elif self.status == 'stats_screen':
            self.stats_screen.run()
        else:
            self.tictactoe.run()
            
        self.mouse.draw()


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tic Tac toe")
pygame.mouse.set_visible(False)
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
