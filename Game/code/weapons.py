import pygame
import math
from code.settings import *


class Weapons(pygame.sprite.Sprite):
    def __init__(self, entity, groups, ranged=0):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        self.side = entity.status.split('_')[0]
        self.direction = entity.direction
        self.player = entity
        self.ranged = ranged
        self.name = None
        self.frame = 0
        if ranged:
            self.direction = entity.direction
        # graphic
        if entity.sprite_type == 'player':
            self.path = f'NinjaAdventure/Items/Weapons/{entity.weapons[entity.weapon_index]}/SpriteInHand.png'
            if entity.parry:
                self.path = f'NinjaAdventure/Items/Weapons/{entity.weapons[entity.weapon_index]}/Sprite.png'
        else:
            if entity.attack_type == 'range':
                if ranged:
                    if entity.name == 'GiantFrog':
                        self.path = 'NinjaAdventure/FX/Projectile/CanonBall.png'
                        self.sprite = pygame.image.load(self.path).convert_alpha()
                        self.sprites = []
                        self.name = 'Ball'
                    elif entity.name == '0Spirit':
                        self.path = 'NinjaAdventure/FX/Projectile/EnergyBall.png'
                        self.sprite = pygame.image.load(self.path).convert_alpha()
                        self.sprites = []
                        self.name = 'Energy'
                    else:
                        self.path = 'NinjaAdventure/Items/Weapons/Bow/Arrow.png'
                else:
                    self.path = 'NinjaAdventure/Items/Weapons/Bow/Sprite.png'

        self.image = pygame.image.load(self.path)
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*3, self.image.get_height()*3))
        if self.name == 'Ball':
            for i in range(5):
                sprite = pygame.Surface((16, 16)).convert_alpha()
                sprite.blit(self.sprite, (0, 0), (i*16, 0 * 16, 16, 16))
                sprite = pygame.transform.scale(sprite, (TILESIZE, TILESIZE))
                sprite.set_colorkey((0, 0, 0))
                self.sprites.append(sprite)
            self.image = self.sprites[0]
            self.rect = self.image.get_rect(center=entity.rect.center)
        elif self.name == 'Energy':
            for i in range(4):
                sprite = pygame.Surface((16, 16)).convert_alpha()
                sprite.blit(self.sprite, (0, 0), (i*16, 0 * 16, 16, 16))
                sprite = pygame.transform.scale(sprite, (TILESIZE, TILESIZE))
                sprite.set_colorkey((0, 0, 0))
                self.sprites.append(sprite)
            self.image = self.sprites[0]
            self.rect = self.image.get_rect(center=entity.rect.center)
        elif ranged:
            if self.direction.x != 0:
                self.image = pygame.transform.rotate(self.image, math.degrees(math.tan(-self.direction.y/self.direction.x)))
            if self.direction.x < 0:
                self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect(center=entity.rect.center)
        else:
            if self.side == 'up':
                self.image = pygame.transform.rotate(self.image, 180)
                self.rect = self.image.get_rect(midbottom=entity.rect.midtop + pygame.Vector2(-12, 0))
            elif self.side == 'down':
                self.rect = self.image.get_rect(midtop=entity.rect.midbottom + pygame.Vector2(-4, 0))
            elif self.side == 'left':
                self.image = pygame.transform.rotate(self.image, 270)
                self.rect = self.image.get_rect(midright=entity.rect.midleft + pygame.Vector2(0, 12))
            elif self.side == 'right':
                self.image = pygame.transform.rotate(self.image, 90)
                self.rect = self.image.get_rect(midleft=entity.rect.midright + pygame.Vector2(0, 12))
            if entity.sprite_type == 'player' and entity.parry:
                self.image = pygame.transform.rotate(self.image, 90)
                self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        if self.ranged:
            if self.name is not None:
                self.frame += 0.15
                if self.frame >= len(self.sprites):
                    self.frame = 0
                self.image = self.sprites[int(self.frame)]
            self.rect.x += self.direction.x * 6
            self.rect.y += self.direction.y * 6
        else:
            if self.side == 'up':
                # self.image = pygame.transform.rotate(self.image, self.rotation_speed)
                self.rect = self.image.get_rect(midbottom=self.player.rect.midtop + pygame.Vector2(-12, 0))
            elif self.side == 'down':
                self.rect = self.image.get_rect(midtop=self.player.rect.midbottom + pygame.Vector2(-4, 0))
            elif self.side == 'left':
                # self.image = pygame.transform.rotate(self.image, self.rotation_speed)
                self.rect = self.image.get_rect(midright=self.player.rect.midleft + pygame.Vector2(0, 12))
            elif self.side == 'right':
                # self.image = pygame.transform.rotate(self.image, self.rotation_speed)
                self.rect = self.image.get_rect(midleft=self.player.rect.midright + pygame.Vector2(0, 12))
