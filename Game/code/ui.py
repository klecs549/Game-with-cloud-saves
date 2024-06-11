import pygame
from code.settings import *


class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        health = pygame.image.load("NinjaAdventure/HUD/Heart.png").convert_alpha()
        self.window = SCREEN.copy
        self.health = [0, 1, 2]
        for pos in range(len(self.health)):
            self.health[pos] = pygame.Surface([16, 16])
            self.health[pos].blit(health, (0, 0), (pos * 2 * 16, 0, 16, 16))
            self.health[pos] = pygame.transform.scale(self.health[pos], (TILESIZE, TILESIZE))
            self.health[pos].set_colorkey((0, 0, 0))
        self.health_rect = [self.health[i].get_rect() for i in range(len(self.health))]
        self.image = self.health[0]
        self.rect = self.image.get_rect()

    def display(self, player):

        max_hp = player.max_hp
        hp = player.health
        index = 0
        while max_hp > 0:
            if hp > 1:
                SCREEN.blit(self.health[0], (index*(TILESIZE+5)+10, 5))
            elif hp == 1:
                SCREEN.blit(self.health[1], (index*(TILESIZE+5)+10, 5))
            else:
                SCREEN.blit(self.health[2], (index*(TILESIZE+5)+10, 5))
            max_hp -= 2
            hp -= 2
            index += 1

        font = pygame.font.Font(None, 30)
        display_surface = pygame.display.get_surface()
        debug_surf = font.render(str(player.current_regen), True, 'White')
        debug_rect = debug_surf.get_rect(topleft=(30, 60))
        pygame.draw.rect(display_surface, 'Black', debug_rect)
        display_surface.blit(debug_surf, debug_rect)
