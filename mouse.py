import pygame
from support import import_folder

class Mouse:
    def __init__(self, surface):
        self.import_mouse_assets()

        self.display_surface = surface
        self.status = 'normal'

        self.image = self.animations[self.status]

        # Animation
        self.frame_index = 0
        self.animation_speed = 0.2
    
    def change_status(self, status):
        self.status = status

    def import_mouse_assets(self):
        mouse_path = 'graphics/mouse/'
        self.animations = {'normal': [], 'hover': [], 'rainbow': [], 'demon': [], 'equality': []}

        for animation in self.animations.keys():
            full_path = mouse_path + animation
            self.animations[animation] = import_folder(full_path, 40)

    def animate(self):
        animation = self.animations[self.status]

        # Loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
    
    def draw(self):
        self.animate()
        self.display_surface.blit(self.image, pygame.mouse.get_pos())