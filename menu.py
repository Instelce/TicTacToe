import pygame
import sys
import json

from settings import *
from support import get_font, print_matrix
from tiles import Case

pygame.font.init()


class Menu:
    def __init__(self, surface, title, component_list, background_image=None):
        """
        Constructor
        Args:
            surface (pygame.Surface)
            title (str)
            buttons_list (list): All buttons
            background_image (str): Path of the background image
        """
        self.title = title
        self.display_surface = surface

        # Buttons
        self.component_gap = 60
        self.component_list = component_list
        self.last_time = pygame.time.get_ticks()

        # Background
        self.background_surface = pygame.Surface(
            (screen_width, screen_height))

        if background_image != None:
            self.background = pygame.image.load(background_image)
        else:
            self.background = pygame.Surface((screen_width, screen_height))
            self.background.fill('#FFFFFF')

    def draw_title(self):
        title_font = get_font(80)
        title_surf = title_font.render(self.title, True, "#000000")
        title_rect = title_surf.get_rect(
            center=(screen_width / 2, screen_height / 2 - 200))
        self.display_surface.blit(title_surf, title_rect)

    def position_buttons(self):
        is_repositioned = False
        if not is_repositioned:
            temp_pos = self.component_list[0].pos
            for i in range(len(self.component_list)):
                button = self.component_list[i]
                button_pos = list(button.pos)
                button_pos[1] = temp_pos[1] + self.component_gap * i
                button.pos = tuple(button_pos)
                is_repositioned = True

    def draw_buttons(self):
        for button in self.component_list:
            button.draw()

    def run(self):
        now = pygame.time.get_ticks()

        self.display_surface.blit(
            self.background_surface, self.background_surface.get_rect(topleft=(0, 0)))

        if self.background != None:
            self.display_surface.blit(self.background, (0, 0))

        if now - self.last_time >= 100:
            self.draw_title()
            self.position_buttons()
            self.draw_buttons()


class MatrixMenu(Menu):
    def __init__(self, surface, title, games_data, component_list, background_image=None):
        super().__init__(surface, title, component_list, background_image)
        self.games_data = games_data
        self.game_data = games_data[f"game_data_{len(games_data)-1}"][0]
        self.matrix = self.game_data['matrix']
        self.index = self.game_data['index']
        self.tile_size = 100
        self.round_image = pygame.image.load(
            'graphics/round.png').convert_alpha()
        self.cross_image = pygame.image.load(
            'graphics/cross.png').convert_alpha()
        self.grid_tiles = []
        self.case_group = pygame.sprite.Group()

        self.component_list[0].pos = ((screen_width / 2), (screen_height / 2) + 200)

        # Arrows
        self.right_arrow = Button(self.display_surface, self.increase_game_index, "+", 50, 50, 
        ((screen_width/2) + 200, (screen_height/2) - 20), 'graphics/button/arrow/button_normal.png', 'graphics/button/arrow/button_hover.png')
        self.left_arrow = Button(self.display_surface, self.decrease_game_index, "-", 50, 50, 
        ((screen_width/2) - 240, (screen_height/2) - 20), 'graphics/button/arrow/left/button_normal.png', 'graphics/button/arrow/left/button_hover.png')

        self.create_grid()
    
    def draw_arrows(self):
        if len(self.games_data) != self.index + 1:
            self.right_arrow.draw()
        if self.index > 0:
            self.left_arrow.draw()
    
    def increase_game_index(self):
        self.index += 1
        # Update data
        self.game_data = self.games_data[f"game_data_{self.index}"][0]
        self.matrix = self.game_data['matrix']
        print_matrix(self.matrix)
        self.case_group = pygame.sprite.Group()
        self.draw_grid()
    
    def decrease_game_index(self):
        self.index -= 1
        # Update data
        self.game_data = self.games_data[f"game_data_{self.index}"][0]
        self.matrix = self.game_data['matrix']
        print_matrix(self.matrix)
        self.case_group = pygame.sprite.Group()
        self.draw_grid()
    
    def create_grid(self):
        for i in range(0, 3):
            row = []
            for j in range(0, 3):
                tile = pygame.Rect((screen_width / 2) - 150 + j * self.tile_size,
                                   (screen_height / 2) - 150 + i * self.tile_size, self.tile_size, self.tile_size)
                row.append(tile)
            self.grid_tiles.append(row)
    
    def draw_grid(self):
        for row in self.grid_tiles:
            for tile in row:
                pygame.draw.rect(self.display_surface,
                                "black", tile, 2)
                    
        for row_index, matrix_row in enumerate(self.matrix):
            for col_index, val in enumerate(matrix_row):
                if val == 'X':
                    tile = Case(80, self.grid_tiles[row_index][col_index].x + 10,
                            self.grid_tiles[row_index][col_index].y + 10, self.cross_image)
                    self.case_group.add(tile)
                if val == 'O':
                    tile = Case(80, self.grid_tiles[row_index][col_index].x + 10,
                            self.grid_tiles[row_index][col_index].y + 10, self.round_image)
                    self.case_group.add(tile)

    def run(self):
        now = pygame.time.get_ticks()

        print("Index :", self.index)

        self.draw_title()
        self.draw_grid()
        self.draw_arrows()
        self.case_group.draw(self.display_surface)

        if now - self.last_time >= 100:
            self.position_buttons()
            self.draw_buttons()        

class Button:
    def __init__(self, surface, callback, text, width, height, pos=None, normal_image='graphics/button/button_normal.png', hover_image='graphics/button/button_hover.png'):
        super().__init__()
        self.width = width
        self.height = height
        self.display_surface = surface
        self.text = text
        self.callback = callback
        self.normal_image = normal_image
        self.hover_image = hover_image
        self.is_click = False
        self.last_time = pygame.time.get_ticks()

        # Font and image
        self.font = get_font(30)
        self.image = pygame.image.load(self.normal_image).convert_alpha()

        # If the button is on a menu or not
        if pos != None:
            self.pos = pos
        else:
            self.pos = ((screen_width / 2) - int(width /
                                                 2), (screen_height / 2) - int(height / 2) - 100)

        self.rect = self.image.get_rect(topleft=self.pos)

        # Text
        self.text_surf = self.font.render(text, True, "#000000")
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        now = pygame.time.get_ticks()
        if self.rect.collidepoint(mouse_pos):
            # Change color of button on hover
            self.image = pygame.image.load(self.hover_image).convert_alpha()
            self.display_surface.blit(self.image, self.rect)
            self.display_surface.blit(self.text_surf, self.text_rect)
        
            if pygame.mouse.get_pressed()[0] and not self.is_click:
                print('CLICK', self.text)
                if self.callback != None:
                    self.callback()
                    self.is_click = True
        else:
            self.is_click = False
            self.image = pygame.image.load(self.normal_image).convert_alpha()
            self.display_surface.blit(self.image, self.rect)
            self.display_surface.blit(self.text_surf, self.text_rect)

    def alignement(self, y_alignement):
        if y_alignement == 'top':
            y = 50 + self.text_surf.get_size()[1]
        elif y_alignement == 'middle':
            y = screen_height / 2
        elif y_alignement == 'bottom':
            y = (screen_height - 80) - self.text_surf.get_size()[1]
        
        self.pos = (self.pos[0], y)

    def reverse(self):
        self.image = pygame.image.load(self.normal_image).convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180)

    def draw(self):
        # Update rect end text
        self.rect = self.image.get_rect(topleft=self.pos)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

        # Draw rext and text
        self.display_surface.blit(self.image, self.rect)
        self.display_surface.blit(self.text_surf, self.text_rect)

        self.check_click()


class Text:
    def __init__(self, text, pos=None, size=40, color="#000000", font_path="graphics/ui/Gamer.ttf"):
        self.text = text
        self.size = size
        self.color = color
        self.pos = pos

        # If the button is on a menu or not
        if pos != None:
            self.pos = pos
        else:
            self.pos = ((screen_width / 2), (screen_height / 2) - 100)

        self.font = pygame.font.Font(font_path, self.size)
        self.surf =  self.font.render(self.text, True, self.color)
        self.rect = self.surf.get_rect(center=self.pos)
        self.display_surface = pygame.display.get_surface()

    def draw(self):
        self.surf =  self.font.render(self.text, True, self.color)
        self.rect = self.surf.get_rect(center=self.pos)
        self.display_surface.blit(self.surf, self.rect)