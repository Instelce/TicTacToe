import pygame
import sys

from settings import *
from support import get_font

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


class Button:
    def __init__(self, surface, callback, text, width, height, mouse, pos=None, normal_image='graphics/button/button_normal.png', hover_image='graphics/button/button_hover.png'):
        super().__init__()
        self.width = width
        self.height = height
        self.display_surface = surface
        self.text = text
        self.mouse = mouse
        self.callback = callback
        self.normal_image = normal_image
        self.hover_image = hover_image

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
        if self.rect.collidepoint(mouse_pos):
            # Change color of button on hover
            self.mouse.change_status('hover')
            self.image = pygame.image.load(self.hover_image).convert_alpha()
            self.display_surface.blit(self.image, self.rect)
            self.display_surface.blit(self.text_surf, self.text_rect)

            if pygame.mouse.get_pressed()[0]:
                print('CLICK', self.text)
                if self.callback != None:
                    self.callback()
        else:
            self.mouse.change_status('normal')
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