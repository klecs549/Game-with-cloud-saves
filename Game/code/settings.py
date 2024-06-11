import pygame

WIDTH = 1280
HEIGHT = WIDTH * 9 / 16
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
TILESIZE = HEIGHT / 15

enemies = {
    '0Slime3': {'hp': 10, 'speed': 3, 'attack_damage': 1, 'type': 'claw', 'attack_radius': 36, 'resistance': 0,
                'attack_cooldown': 1500, 'pushing': 5},
    'Caveman': {'hp': 15, 'speed': 4, 'attack_damage': 1, 'type': 'range', 'attack_radius': 400, 'resistance': 0,
                'attack_cooldown': 2000, 'pushing': 2},
    'GiantFrog': {'hp': 60, 'speed': 4, 'attack_damage': 1, 'type': 'range', 'attack_radius': 300, 'resistance': 0,
                  'attack_cooldown': 300, 'pushing': 2},
    '0Mollusc': {'hp': 10, 'speed': 2, 'attack_damage': 1, 'type': 'claw', 'attack_radius': 36, 'resistance': 5,
                 'attack_cooldown': 1500, 'pushing': 2},
    'RedDemon': {'hp': 15, 'speed': 4, 'attack_damage': 1, 'type': 'range', 'attack_radius': 400, 'resistance': 5,
                 'attack_cooldown': 1000, 'pushing': 2},
    'GiantRacoon': {'hp': 75, 'speed': 4, 'attack_damage': 1, 'type': 'claw', 'attack_radius': 150, 'resistance': 5,
                    'attack_cooldown': 400, 'pushing': 2},
    '0Spirit': {'hp': 15, 'speed': 4, 'attack_damage': 1, 'type': 'range', 'attack_radius': 400, 'resistance': 0,
                'attack_cooldown': 400, 'pushing': 2},
    'BlueSamurai': {'hp': 20, 'speed': 6, 'attack_damage': 1, 'type': 'claw', 'attack_radius': 50, 'resistance': 0,
                    'attack_cooldown': 2000, 'pushing': 1},
    'GiantRacoonGold': {'hp': 150, 'speed': 4, 'attack_damage': 1, 'type': 'claw', 'attack_radius': 150, 'resistance': 0,
                        'attack_cooldown': 600, 'pushing': 0},
    'GoldKnight': {'hp': 200, 'speed': 4, 'attack_damage': 1, 'type': 'claw', 'attack_radius': 100, 'resistance': 0,
                   'attack_cooldown': 400, 'pushing': 2}
}
boss_animations = {
    'GiantFrog': {0: 5, 1: 6, 2: 10},
    'GiantRacoon': {0: 6, 1: 5, 2: 8},
    'GiantRacoonGold': {0: 6, 1: 5, 2: 6}
}

weapon_data = {
    'Katana': {'cooldown': 300, 'damage': 5, 'graphic': '../NinjaAdventure/Items/Weapons/Katana/Sprite.png'},
    'Sword': {'cooldown': 300, 'damage': 5, 'graphic': '../NinjaAdventure/Items/Weapons/Sword/Sprite.png'},
    'Hammer': {'cooldown': 700, 'damage': 10, 'graphic': '../NinjaAdventure/Items/Weapons/Hammer/Sprite.png'},
    'Bow': {'cooldown': 300, 'damage': 3, 'graphic': '../NinjaAdventure/Items/Weapons/Bow/Sprite.png'},
}
