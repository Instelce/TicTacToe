import pygame
from settings import *
from os import walk

def get_font(size):
    return pygame.font.Font('graphics/ui/Gamer.ttf', size)

sound_is_play = False

if sound_is_play:
    sound_is_play = False

def play_sound(sound):
    global sound_is_play
    
    sounds = {
        'clap': 'sounds/clap.wav',
        'computer_turn': 'sounds/computer_turn.wav',
        'player_turn': 'sounds/player_turn.wav',
        'cross_player_turn': 'sounds/cross_player_turn.wav',
        'round_player_turn': 'sounds/round_player_turn.wav',
        'you_lose': 'sounds/you_lose.wav',
        'you_win': 'sounds/you_win.wav',
    }

    if not sound_is_play:
        pygame.mixer.Sound(sounds[sound]).play()
        sound_is_play = True


def import_folder(path, tile_size=64):
    surface_list = []

    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.transform.scale(
                pygame.image.load(full_path).convert_alpha(), (tile_size, tile_size))
            surface_list.append(image_surf)

    return surface_list


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