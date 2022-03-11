import pygame

tile_size = 64
vertical_tile_number = 18
horizontal_tile_number = 11

screen_width = vertical_tile_number * tile_size
screen_height = horizontal_tile_number * tile_size


def get_font(size):
    return pygame.font.Font('graphics/ui/Gamer.ttf', size)