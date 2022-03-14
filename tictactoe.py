from re import S
import pygame
from random import randint

from settings import *
from tiles import Case
from support import *
from menu import Button


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
        self.case_group = pygame.sprite.Group()
        self.already_set = False
        self.winner = None

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

        for row_index, row in enumerate(self.grid_tiles):
            for tile_index, tile in enumerate(row):

                # Hover
                if tile.collidepoint(mouse_pos):
                    pygame.draw.rect(self.display_surface,
                                     "gray", tile, 2)

                    if len(self.case_group) >= 1:
                        for case in self.case_group:
                            if case.zone.collidepoint((tile.x + 10, tile.y + 10)):
                                self.already_set = True
                                self.draw_tiles.append(tile)
                            else:
                                self.already_set = False

                    # Click
                    if pygame.mouse.get_pressed()[0]:
                        if not self.already_set and tile not in self.draw_tiles:
                            pygame.draw.rect(self.display_surface,
                                             "blue", tile, 2)

                            if self.player == 'X':
                                tile = Case(80, tile.x + 10,
                                            tile.y + 10, self.cross_image)
                                self.tictactoe_matrix[row_index][tile_index] = 'X'
                            elif self.player == 'O':
                                tile = Case(80, tile.x + 10,
                                            tile.y + 10, self.round_image)
                                self.tictactoe_matrix[row_index][tile_index] = 'O'

                            self.case_group.add(tile)
                            self.change_player()
                        else:
                            pygame.draw.rect(self.display_surface,
                                             "red", tile, 2)

                        print_matrix(self.tictactoe_matrix)

    def check_win(self):
        x_col_count = {}
        o_col_count = {}

        for row_index, row in enumerate(self.tictactoe_matrix):
            for col_index, val in enumerate(row):
                x_col_count[col_index] = 0
                o_col_count[col_index] = 0

        for row_index, row in enumerate(self.tictactoe_matrix):
            # Row check
            if row == ['X', 'X', 'X'] or row == ['O', 'O', 'O']:
                if row[0] == 'X':
                    self.winner = 'X'
                elif row[0] == 'O':
                    self.winner = 'O'
            for col_index, val in enumerate(row):
                if val == 'X':
                    x_col_count[col_index] += 1
                elif val == 'O':
                    o_col_count[col_index] += 1

        # Column check
        for col in x_col_count:
            if x_col_count[col] == 3:
                self.winner = 'X'
        for col in o_col_count:
            if o_col_count[col] == 3:
                self.winner = 'O'

        # Diagonal check
        x_diagonal_right = 0
        o_diagonal_right = 0
        x_diagonal_left = 0
        o_diagonal_left = 0

        for row_index, row in enumerate(self.tictactoe_matrix):
            for col_index, val in enumerate(row):
                if col_index == row_index and val == 'X':
                    x_diagonal_right += 1
                elif col_index == row_index and val == 'O':
                    o_diagonal_right += 1

        # Reverse the matrix for left check
        tictactoe_matrix_reverse = []
        for row_index, row in enumerate(self.tictactoe_matrix):
            line = self.tictactoe_matrix[row_index][::-1]
            tictactoe_matrix_reverse.append(line)

        for row_index, row in enumerate(tictactoe_matrix_reverse):
            for col_index, val in enumerate(row):
                if col_index == row_index and val == 'X':
                    x_diagonal_left += 1
                elif col_index == row_index and val == 'O':
                    o_diagonal_left += 1

        if x_diagonal_right == 3 or x_diagonal_left == 3:
            self.winner = 'X'
        elif o_diagonal_right == 3 or o_diagonal_left == 3:
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
        back_button.draw(back_button.pos)

    def run(self):
        now = pygame.time.get_ticks()
        grid_is_draw = False

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
        self.draw_back_button()

        if now -self.last_time >= 300 and not grid_is_draw:
            self.draw_grid()
            grid_is_draw = True

        if grid_is_draw:
            self.check_grid()

        self.check_win()

        self.case_group.draw(self.display_surface)
