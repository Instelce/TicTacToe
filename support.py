from numpy import matrix
import pygame
from settings import *


def get_font(size):
    return pygame.font.Font('graphics/ui/Gamer.ttf', size)


def draw_text(surface, text, size, color, pos):
    font = get_font(size)
    surf = font.render(text, True, color)
    rect = surf.get_rect(
        center=pos)
    surface.blit(surf, rect)
def create_matrix(width, height):
    matrix = []
    for i in range(height):
        line = []
        for j in range(width):
            line.append('')
        matrix.append(line)
    return matrix

def print_matrix(matrix):
    for row in matrix:
        print(row)