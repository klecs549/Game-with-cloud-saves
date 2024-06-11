import os
from csv import reader, writer
from os import walk
import pygame
from code.settings import *


def import_csv(path):
    terrain_map = []
    with open(path) as csvfile:
        layout = reader(csvfile, delimiter=',')
        for row in layout:
            terrain_map.append(row)
        return terrain_map


def import_folder(path):
    surface_list = []
    # print("Importing")
    for _, __, imgs in walk(path):
        # print(_, __, imgs)
        for image in imgs:
            full_path = path + '/' + image
            # full_path = full_path[3:]
            # print(full_path)
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def get_tile(num, type, graphic):
    if type == 'nature':
        length = 24
        position = 14
    else:
        length = 0
        position = 0
    y = int(num / length)
    x = int(num % length)
    image = pygame.Surface([16, 16])
    image.blit(graphic['Tiles'][position], (0, 0), (x * 16, y * 16, 16, 16))
    image = pygame.transform.scale(image, (48, 48))
    image.set_colorkey((0, 0, 0))
    return image


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1000, 200))
    pygame.display.set_caption("Test")
    print(import_folder('../NinjaAdventure/Backgrounds/Tilesets'))
