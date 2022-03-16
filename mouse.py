import pygame


class Mouse:
    def __init__(self, surface):
        self.display_surface = surface
        self.status = 'normal'
        self.image_path = 'graphics/mouse/normal.png'
        self.image = pygame.image.load(self.image_path).convert_alpha()
    
    def change_status(self, status):
        self.status = status
    
    def draw(self):
        if self.status == 'normal':
            self.image_path = 'graphics/mouse/normal.png'
        elif self.status == 'hover':
            self.image_path = 'graphics/mouse/hover.png'
        elif self.status == 'rainbow':
            self.image_path = 'graphics/mouse/rainbow.png'
            
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.display_surface.blit(self.image, pygame.mouse.get_pos())