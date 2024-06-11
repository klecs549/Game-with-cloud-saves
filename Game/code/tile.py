import pygame
from code.settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE)), name=None, active=False):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.name = name
        self.active = active
        self.image.set_colorkey((0, 0, 0))
        # self.image = pygame.transform.scale(self.image, (48, 48))
        # self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-5, -20)
