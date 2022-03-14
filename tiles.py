import pygame


class Case(pygame.sprite.Sprite):
    def __init__(self, size, x, y, surface):
        super().__init__()
        self.size = size
        self.pos = (x, y)
        self.image = surface
        self.rect = self.image.get_rect(topleft=(x, y))
        self.zone = pygame.Rect(
            x, y, size, size)