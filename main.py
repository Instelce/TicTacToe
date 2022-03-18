import pygame
import sys
import json

from support import *
from settings import *
from tictactoe import TicTacToe
from menu import *
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
                                        self.create_old_games_screen, "Dernière partie", 400, 50, self.mouse),
                                Button(screen,
                                        self.quit_game, "Quitter", 400, 50, self.mouse)
                            ])
        self.status = 'menu'
    
    def create_stats_screen(self):
        with open("data/stats.json", "r") as stats_file:
            data = json.load(stats_file)
    
        print("data", data)

        self.stats_screen = Menu(screen,
							   "Statistics",
							   [
								   Text(f"Victory over the simple computer : {data['victory_over_simple_computer']}"),
								   Text(f"Victory over the expert computer : {data['victory_over_expert_computer']}"),
								   Text(f"Number of games played : {data['game_played']}"),
								   Text(f"Games won by player X : {data['won_by_X']}"),
								   Text(f"Games won by player O : {data['won_by_O']}"),
								   Button(screen,
										  self.reset_stats_data, "Reset Data", 400, 50, self.mouse),
                                Button(screen,
										  self.create_menu, "Back", 400, 50, self.mouse)
							   ])
        self.status = 'stats_screen'

    def create_old_games_screen(self):
        with open("data/games.json", "r") as stats_file:
            data = json.load(stats_file)

        self.old_games_screen = Matrix(screen,
        "Old Games",
        data[f"game_data_{len(data)-1}"],
        [
            Button(screen,
                    self.create_menu, "Back", 400, 50, self.mouse)
        ]
        )
        self.status = 'old_games_screen'

    def create_jcj_tictactoe(self):
        self.tictactoe = TicTacToe(screen, 'jcj', self.mouse, self.create_menu)
        self.status = 'game'

    def create_simple_computer_tictactoe(self):
        self.tictactoe = TicTacToe(screen, 'computer simple', self.mouse, self.create_menu)
        self.status = 'game'

    def create_expert_computer_tictactoe(self):
        self.tictactoe = TicTacToe(screen, 'computer expert', self.mouse, self.create_menu)
        self.status = 'game'

    def reset_stats_data(self):
        with open("data/stats.json", "r") as stats_file:
            data = json.load(stats_file)
        
        for row in data:
            print(data[row])
            data[row] = 0

        with open("data/stats.json", "w") as outfile:
            json.dump(data, outfile)

        self.create_stats_screen()

    def run(self):
        if self.status == 'menu':
            self.start_menu.run()
        elif self.status == 'stats_screen':
            self.stats_screen.run()
        elif self.status == 'old_games_screen':
            self.old_games_screen.run()
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
