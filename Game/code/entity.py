import pygame
from code.settings import *
from math import sin


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.1
        self.direction = pygame.math.Vector2()

    def move(self):
        if abs(self.direction.magnitude()) > 2:
            pass
        elif self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * self.speed
        self.collision(0)
        self.hitbox.y += self.direction.y * self.speed
        self.collision(2)
        self.rect.center = self.hitbox.center

    def choose_border(self):
        if self.rect.y < 3900:
            self.border_pos = 0
        elif self.rect.y > 7050:
            self.border_pos = 2
        else:
            self.border_pos = 1
    def collision(self, direction):
        if direction == 0:
            for sprite in self.borders[self.border_pos]:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 2:
            for sprite in self.borders[self.border_pos]:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    @staticmethod
    def wave_val():
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
