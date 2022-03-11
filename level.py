import pygame
from random import randint

from settings import *


class Level:
    def __init__(self, surface):
        super(Level, self).__init__()
        self.display_surface = surface

        self.matrix = [['', '', ''],
                       ['', '', ''],
                       ['', '', '']]

        self.tile_size = 100
        self.grid_tiles = []
        for i in range(0, 3):
            row = []
            for j in range(0, 3):
                tile = pygame.Rect((screen_width / 2) - 150 + j * self.tile_size,
                                   (screen_height / 2) - 150 + i * self.tile_size, self.tile_size, self.tile_size)
                row.append(tile)
            self.grid_tiles.append(row)

        print(self.grid_tiles)

    def draw_grid(self):
        for row in self.grid_tiles:
            for tile in row:
                pygame.draw.rect(self.display_surface,
                             "black", tile, 2)

    def check_grid(self):
        mouse_pos = pygame.mouse.get_pos()
        for row_index, row in enumerate(self.grid_tiles):
            for tile_index, tile in enumerate(row):
                if tile.collidepoint(mouse_pos):
                    pygame.draw.rect(self.display_surface,
                             "gray", tile, 2)
                    if pygame.mouse.get_pressed()[0]:
                        pygame.draw.rect(self.display_surface,
                             "blue", tile, 2)
    def draw_title(self):
        title_font = get_font(80)
        title_surf = title_font.render("Tic Tac Toe", True, "#000000")
        title_rect = title_surf.get_rect(
            center=(screen_width / 2, 100))
        self.display_surface.blit(title_surf, title_rect)

    def run(self):
        self.draw_title()
        self.draw_grid()
        self.check_grid()
