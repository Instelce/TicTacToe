from random import randint
import time
import json

import pygame

from menu import Button
from settings import *
from support import *
from tiles import Case


class TicTacToe:
    def __init__(self, surface, game_type, create_start_menu):
        super(TicTacToe, self).__init__()
        self.display_surface = surface
        self.game_type = game_type
        self.create_start_menu = create_start_menu

        self.tictactoe_matrix = create_matrix(3, 3)

        self.tile_size = 100
        self.grid_tiles = []
        self.draw_tiles = []
        self.round_image = pygame.image.load(
            'graphics/round.png').convert_alpha()
        self.cross_image = pygame.image.load(
            'graphics/cross.png').convert_alpha()
        self.player = 'X'
        self.player_counter = 0
        self.case_group = pygame.sprite.Group()
        self.empty_case_count = 9
        self.already_set = False
        self.winner = None
        self.player_can_play = True
        self.data_is_update = False


        self.last_time = pygame.time.get_ticks()

        self.create_grid()

    def create_grid(self):
        for i in range(0, 3):
            row = []
            for j in range(0, 3):
                tile = pygame.Rect((screen_width / 2) - 150 + j * self.tile_size,
                                   (screen_height / 2) - 150 + i * self.tile_size, self.tile_size, self.tile_size)
                row.append(tile)
            self.grid_tiles.append(row)

    def draw_grid(self):
        now = pygame.time.get_ticks()

        if now - self.last_time >= 200:
            for row in self.grid_tiles:
                for tile in row:
                    pygame.draw.rect(self.display_surface,
                                     "black", tile, 2)

    def check_grid(self):
        mouse_pos = pygame.mouse.get_pos()
        hover_case = pygame.image.load("graphics/hover_case.png")

        for row_index, row in enumerate(self.grid_tiles):
            for tile_index, tile in enumerate(row):

                # Hover
                if tile.collidepoint(mouse_pos):
                    self.display_surface.blit(hover_case, (tile.x, tile.y))

                    if len(self.case_group) >= 1:
                        for case in self.case_group:
                            if case.zone.collidepoint((tile.x + 10, tile.y + 10)):
                                self.already_set = True
                                self.draw_tiles.append(tile)
                            else:
                                self.already_set = False

                    # Click
                    if pygame.mouse.get_pressed()[0] and self.player_can_play:
                        if not self.already_set and tile not in self.draw_tiles:
                            if self.player == 'X':
                                self.player_counter += 1
                                tile = Case(80, tile.x + 10,
                                            tile.y + 10, self.cross_image)
                                self.tictactoe_matrix[row_index][tile_index] = 'X'
                            elif self.player == 'O':
                                tile = Case(80, tile.x + 10,
                                            tile.y + 10, self.round_image)
                                self.tictactoe_matrix[row_index][tile_index] = 'O'

                            self.case_group.add(tile)
                            self.empty_case_count -= 1
                            if self.game_type == 'computer simple' or self.game_type == 'computer expert':
                                self.player_can_play = False
                            if self.game_type == 'jcj':
                                self.change_player()
                        else:
                            pass
    
    def get_random_case(self):
        good_case = False
        case = [randint(0, 2), randint(0, 2)]
        while not good_case:
            if self.tictactoe_matrix[case[0]][case[1]] != '':
                case = [randint(0, 2), randint(0, 2)]
            else:
                good_case = True

        if good_case:
            return case

    def fill_case(self, pos, image, symbol):
        tile = Case(80, self.grid_tiles[pos[0]][pos[1]].x + 10,
                            self.grid_tiles[pos[0]][pos[1]].y + 10, image)
        self.case_group.add(tile)
        self.tictactoe_matrix[pos[0]][pos[1]] = symbol

    def computer(self):
        can_row_block = False
        can_col_block = False
        can_diagonal_right_block = False
        can_diagonal_left_block = False
        can_block_count = 0

        if self.game_type == 'computer simple':
            if not self.player_can_play:
                for count in self.x_row_count:
                    if self.x_row_count[count] == 2:
                        # Block
                        for col_index, val in enumerate(self.tictactoe_matrix[count]):
                            if val == '':
                                print(f"Bloque Ligne {count+1} and check {col_index+1} case")
                                row_case_pos = [count, col_index]
                                can_block_count += 1
                                can_row_block = True
                for count in self.x_col_count:
                    if self.x_col_count[count] == 2:
                        # Block
                        for col_index, val in enumerate(self.tictactoe_col_matrix[count]):
                            if val == '':
                                print(f"Bloque Colonne {count+1} and check {col_index+1} case")
                                col_case_pos = [col_index, count]
                                can_block_count += 1
                                can_col_block = True
                if self.x_diagonal_right_count == 2:
                    for index, val in enumerate(self.x_diagonal_right):
                        if val == '':
                            print(f"Bloque Right Diagonal {index} ; {index}")
                            diagonal_right_pos = [index, index]
                            can_block_count += 1
                            can_diagonal_right_block = True
                if self.x_diagonal_left_count == 2:
                    print(self.x_diagonal_left)
                    for index, val in enumerate(self.x_diagonal_left):
                        if val == '':
                            print(f"Bloque Left Diagonal {index} ; {index}")
                            if index == 0:
                                diagonal_left_pos = [0, 2]
                            elif index == 2:
                                diagonal_left_pos = [2, 0]
                            else:
                                diagonal_left_pos = [index, index]

                            can_block_count += 1
                            can_diagonal_left_block = True

                if can_block_count > 1:
                    row_or_col_or_diagonal = randint(1, can_block_count)
                    print("Block Count :", can_block_count, "| Choice :", row_or_col_or_diagonal)

                    if row_or_col_or_diagonal == 1:
                        # Row block
                        self.fill_case(row_case_pos, self.round_image, 'O')
                    elif row_or_col_or_diagonal == 2:
                        # Col block
                        self.fill_case(col_case_pos, self.round_image, 'O')
                    elif row_or_col_or_diagonal == 3:
                        # Diagonal right block
                        self.fill_case(diagonal_right_pos, self.round_image, 'O')
                    elif row_or_col_or_diagonal == 4:
                        # Diagonal left block
                        self.fill_case(diagonal_left_pos, self.round_image, 'O')
                elif can_row_block:
                    # Row block
                    self.fill_case(row_case_pos, self.round_image, 'O')
                elif can_col_block:
                    # Col block
                                            self.fill_case(col_case_pos, self.round_image, 'O')

                elif can_diagonal_right_block:
                    # Diagonal right block
                    self.fill_case(diagonal_right_pos, self.round_image, 'O')
                elif can_diagonal_left_block:
                    # Diagonal left block
                    self.fill_case(diagonal_left_pos, self.round_image, 'O')
                else:
                    # Random case
                    case = self.get_random_case()
                    print(f"Case aléatoire {case}")
                    tile = Case(80, self.grid_tiles[case[0]][case[1]].x + 10,
                                        self.grid_tiles[case[0]][case[1]].y + 10, self.round_image)
                    self.case_group.add(tile)
                    self.tictactoe_matrix[case[0]][case[1]] = 'O'
                    pass
                
                # time.sleep(2)
                self.empty_case_count -= 1
                self.player_can_play = True 

    def check_win(self):
        self.tictactoe_col_matrix = create_matrix(3, 3)
        self.x_row_count = {}
        self.o_row_count = {}
        self.x_col_count = {}
        self.o_col_count = {}

        # Init value
        for row_index, row in enumerate(self.tictactoe_matrix):
            self.x_row_count[row_index] = 0
            self.o_row_count[row_index] = 0
            for col_index, val in enumerate(row):
                self.tictactoe_col_matrix[col_index][row_index] = val
                self.x_col_count[col_index] = 0
                self.o_col_count[col_index] = 0

        for row_index, row in enumerate(self.tictactoe_matrix):
            # Increse col and row value
            for col_index, val in enumerate(row):
                if val == 'X':
                    self.x_row_count[row_index] += 1
                    self.x_col_count[col_index] += 1
                elif val == 'O':
                    self.o_row_count[row_index] += 1
                    self.o_col_count[col_index] += 1

        print("col ", "X :", self.x_col_count, "O :", self.o_col_count)
        for val in self.x_row_count:
            print(self.x_row_count[val])
        print("row ", "X :", self.x_row_count, "O :", self.o_row_count)
        print("Player counter :", self.player_counter)
        print_matrix(self.tictactoe_matrix)

        # Row check
        for row in self.x_row_count:
            if self.x_row_count[row] == 3:
                self.winner = 'X'
        for row in self.o_row_count:
            if self.o_row_count[row] == 3:
                self.winner = 'O'

        # Column check
        for col in self.x_col_count:
            if self.x_col_count[col] == 3:
                self.winner = 'X'
        for col in self.o_col_count:
            if self.o_col_count[col] == 3:
                self.winner = 'O'

        # Diagonal check
        self.x_diagonal_right = []
        self.x_diagonal_left = []
        self.x_diagonal_right_count = 0
        o_diagonal_right_count = 0
        self.x_diagonal_left_count = 0
        o_diagonal_left_count = 0


        for row_index, row in enumerate(self.tictactoe_matrix):
            for col_index, val in enumerate(row):
                if col_index == row_index:
                    self.x_diagonal_right.append(val)

                if col_index == row_index and val == 'X':
                    self.x_diagonal_right_count += 1
                elif col_index == row_index and val == 'O':
                    o_diagonal_right_count += 1

        print("Diagonal Right : ", self.x_diagonal_right_count)
        
        # Reverse the matrix for left check
        tictactoe_matrix_reverse = []
        for row_index, row in enumerate(self.tictactoe_matrix):
            line = self.tictactoe_matrix[row_index][::-1]
            tictactoe_matrix_reverse.append(line)

        for row_index, row in enumerate(tictactoe_matrix_reverse):
            for col_index, val in enumerate(row):
                if col_index == row_index:
                    self.x_diagonal_left.append(val)

                if col_index == row_index and val == 'X':
                    self.x_diagonal_left_count += 1
                elif col_index == row_index and val == 'O':
                    o_diagonal_left_count += 1

        if self.x_diagonal_right_count == 3 or self.x_diagonal_left_count == 3:
            self.winner = 'X'
        elif o_diagonal_right_count == 3 or o_diagonal_left_count == 3:
            self.winner = 'O'

    def change_player(self):
        if self.player == 'X':
            self.player = 'O'
        elif self.player == 'O':
            self.player = 'X'

    def draw_back_button(self):
        back_button = Button(self.display_surface,
                             self.create_start_menu, "Back To Menu", 400, 50)
        back_button.alignement('bottom')
        back_button.draw()

    def display_text(self):
         # Title
        draw_text(self.display_surface,
                  "Tic Tac Toe",
                  80,
                  "#000000",
                  (screen_width / 2, 100))
        # Subtitle
        draw_text(self.display_surface,
                  self.game_type,
                  40,
                  "#000000",
                  (screen_width / 2, 140))
        # Win text
        if self.winner != None:
            draw_text(self.display_surface,
                  f"Winner is {self.winner} player",
                  40,
                  "#000000",
                  (screen_width / 2, screen_height - 160))
        elif self.winner == None and self.empty_case_count == 0:
            self.winner = 'Equality'
            draw_text(self.display_surface,
                  f"Equality",
                  40,
                  "#000000",
                  (screen_width / 2, screen_height - 160))

    def update_stats_data(self):
        file_data = "data/stats.json"
        
        # Get data
        with open(file_data, "r") as file:
            data = json.load(file)

        print(data)

        if self.game_type == 'computer simple' and self.winner == 'X':
            data['victory_over_simple_computer'] += 1
        if self.game_type == 'computer expert' and self.winner == 'X':
            data['victory_over_expert_computer'] += 1
        if self.winner == 'X':
            data['won_by_X'] += 1
        if self.winner == 'O':
            data['won_by_O'] += 1

        data['game_played'] += 1

        with open(file_data, 'w') as outfile:
            json.dump(data, outfile)

    def update_games_data(self):
        file_data = "data/games.json"

        with open(file_data, 'r') as games_file:
            data = json.load(games_file)

        if len(data) == 0:
            self.game_index = 0
        else:
            # Get the last game index
            self.game_index = data[f'game_data_{str(len(data) - 1)}'][0]['index'] + 1

        data[f'game_data_{self.game_index}'] = []
        data[f'game_data_{self.game_index}'].append({
            'index': self.game_index,
            'matrix': self.tictactoe_matrix,
            'winner': self.winner,
        })

        with open(file_data, 'w') as outfile:
            json.dump(data, outfile)

    def run(self):
        now = pygame.time.get_ticks()
        grid_is_draw = False

        self.display_text()
        self.draw_back_button()

        if now -self.last_time >= 300 and not grid_is_draw:
            self.draw_grid()
            grid_is_draw = True

        if grid_is_draw and self.winner == None and self.empty_case_count >= 1:
            self.check_grid()
            self.check_win()
                
        if self.winner != None and not self.data_is_update:
            self.update_stats_data()
            self.update_games_data()
            self.data_is_update = True

        if self.player_can_play and self.game_type != 'jcj' and self.winner == None:
            draw_text(self.display_surface,
                  "Player Turn",
                  40,
                  "#000000",
                  (screen_width / 2, screen_height - 160))
        elif not self.player_can_play and self.game_type != 'jcj' and self.winner == None and self.empty_case_count >= 1:
            draw_text(self.display_surface,
                "Computer Turn",
                40,
                "#000000",
                (screen_width / 2, screen_height - 160))

            if now - self.last_time >= 2000:
                self.last_time = now
                self.computer()            

        self.case_group.draw(self.display_surface)
