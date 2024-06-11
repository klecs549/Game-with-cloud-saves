import pygame.sprite

from code.settings import *
from code.tile import Tile
from code.player import Player
from code.work_with_csv import *
from code.weapons import Weapons
from code.ui import UI
from code.debug import debug
from code.enemy import Enemy


class Level:
    def __init__(self, save=None):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.stone_obstacles_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()
        self.air_obstacle_sprites = pygame.sprite.Group()
        self.abilities_sprites = pygame.sprite.Group()
        self.teleports_sprites = pygame.sprite.Group()
        self.campfires_sprites = pygame.sprite.Group()
        self.layouts = {
            "Border": import_csv("Layers/layer._Border.csv"),
            "entities": import_csv("Layers/layer._Entities.csv"),
            'abilities': import_csv("Layers/layer._Abilities.csv"),
            'teleports': import_csv("Layers/layer._Teleports.csv"),
            'campfires': import_csv("Layers/layer._Campfires.csv")
        }

        self.save = save
        # attack sprite
        self.current_attack = list(range(12))
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.ranged_attack = pygame.sprite.Group()

        self.player = None
        if save is not None:
            position = [save[0][0], save[0][1]]
            self.player = Player((position[1] * TILESIZE, position[0] * TILESIZE),
                                 [self.visible_sprites],
                                 [self.obstacles_sprites,
                                 self.ranged_attack,
                                 self.abilities_sprites,
                                 self.teleports_sprites,
                                 self.campfires_sprites],
                                 [self.stone_obstacles_sprites, self.obstacles_sprites, self.air_obstacle_sprites],
                                 self.create_attack,
                                 self.destroy_attack,
                                 save[2],
                                 self.save_game,
                                 self.check_death
                                 )
        self.create_map()
        self.ui = UI()

    def create_map(self):
        graphics = {
            "Tiles": import_folder("NinjaAdventure/Backgrounds/Tilesets")

        }
        for style, layout in self.layouts.items():
            for row_index, row in enumerate(layout):
                for column_index, col in enumerate(row):
                    if col != '-1':
                        x = column_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "Border":
                            if y < 3900:
                                Tile((x, y),
                                     [self.stone_obstacles_sprites],
                                     "Border",
                                     )
                            elif y > 7050:
                                Tile((x, y),
                                     [self.air_obstacle_sprites],
                                     "Border",
                                     )
                            else:
                                Tile((x, y),
                                     [self.obstacles_sprites],
                                     "Border",
                                     )
                        elif style == 'entities':
                            name = list(enemies.keys())[int(col)]
                            if 'Giant' in name and self.save[3][name]:
                                break
                            Enemy(
                                name,
                                (x, y),
                                [self.visible_sprites, self.attackable_sprites],
                                [self.stone_obstacles_sprites, self.obstacles_sprites, self.air_obstacle_sprites],
                                self.damage_player,
                                self.create_attack,
                                self.destroy_attack,
                                self.save[3]
                            )
                        elif style == 'abilities':

                            if (x, y) == (1488.0, 1776.0):
                                name = 'Hammer'
                            elif (x, y) == (3264.0, 5568.0):
                                name = 'Sword'
                            else:
                                name = 'Dash'
                            if name in self.save[2] and self.save[2][name]:
                                break
                            sprite = pygame.image.load(f"NinjaAdventure/Items/Weapons/{name}/Sprite.png")
                            sprite = pygame.transform.scale(sprite, (sprite.get_width() * 3, sprite.get_height() * 3))
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.abilities_sprites],
                                'Abilities',
                                sprite,
                                name
                            )
                        elif style == 'teleports':
                            sprite = pygame.image.load("NinjaAdventure/Backgrounds/Teleport.png")
                            sprite = pygame.transform.scale(sprite, (sprite.get_width() * 3, sprite.get_height() * 3))
                            if self.save[1][str(int(y))]:

                                active = True
                            else:
                                active = False
                            Tile((x, y),
                                 [self.visible_sprites, self.teleports_sprites],
                                 "Teleport",
                                 sprite,
                                 active=active or (y > 5000)
                                 )
                        elif style == 'campfires':
                            sprite = pygame.image.load("NinjaAdventure/Backgrounds/Campfire.png")
                            sprite = pygame.transform.scale(sprite, (sprite.get_width() * 3, sprite.get_height() * 3))
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.campfires_sprites, self.obstacles_sprites],
                                'Campfire',
                                sprite)

    def create_attack(self, entity, ranged=0):
        if entity.sprite_type == 'player':
            self.current_attack[0] = Weapons(entity, [self.visible_sprites, self.attack_sprites])
        else:
            if ranged:
                self.current_attack[entity.weapon_pos + 5] = (
                     Weapons(
                        entity,
                        [self.visible_sprites, self.ranged_attack],
                        1))
            else:
                if entity.name == 'Caveman':
                    self.current_attack[entity.weapon_pos] = Weapons(entity, [self.visible_sprites])
                else:
                    self.current_attack[entity.weapon_pos] = Weapons(entity, [])

    def destroy_attack(self, entity, ranged=0):
        if entity.sprite_type == 'player':
            if self.current_attack[0]:
                self.current_attack[0].kill()
            self.current_attack[0] = None
        elif entity.sprite_type == 'enemy':
            if ranged:
                if isinstance(self.current_attack[entity.weapon_pos + 5], Weapons):
                    self.current_attack[entity.weapon_pos + 5].kill()
                self.current_attack[entity.weapon_pos + 5] = 0
            elif isinstance(self.current_attack[entity.weapon_pos], Weapons):
                self.current_attack[entity.weapon_pos].kill()
            #self.current_attack[entity.weapon_pos] = 0

    def respawn_enemies(self):
        for entity in self.attackable_sprites:
            entity.kill()
        for row_index, row in enumerate(self.layouts['entities']):
            for column_index, col in enumerate(row):
                if col != '-1':
                    x = column_index * TILESIZE
                    y = row_index * TILESIZE
                    name = list(enemies.keys())[int(col)]
                    if 'Giant' in name and self.save[3][name]:
                        break
                    Enemy(
                        name,
                        (x, y),
                        [self.visible_sprites, self.attackable_sprites],
                        [self.stone_obstacles_sprites, self.obstacles_sprites, self.air_obstacle_sprites],
                        self.damage_player,
                        self.create_attack,
                        self.destroy_attack,
                        self.save[3]
                    )

    def check_death(self):
        if self.player.health <= 0:
            self.player.death_sound.play()
            self.player.kill()
            self.player = Player((self.save[0][1] * TILESIZE, self.save[0][0] * TILESIZE),
                                 [self.visible_sprites],
                                 [self.obstacles_sprites,
                                 self.ranged_attack,
                                 self.abilities_sprites,
                                 self.teleports_sprites,
                                 self.campfires_sprites],
                                 [self.stone_obstacles_sprites, self.obstacles_sprites, self.air_obstacle_sprites],
                                 self.create_attack,
                                 self.destroy_attack,
                                 self.save[2],
                                 self.save_game,
                                 self.check_death
                                 )
            self.respawn_enemies()

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'rock':
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def save_game(self):
        self.respawn_enemies()
        self.player.health = self.player.max_hp
        try:
            self.save[0] = [self.player.rect.y / TILESIZE, self.player.rect.x / TILESIZE]
        except AttributeError:
            self.save[0] = [0, 0]
        for teleport in self.teleports_sprites:
            if teleport.active:
                self.save[1][str(int(teleport.rect.y))] = 1
            # else:
            #     self.save[0][teleport.rect.y] = 0
        if self.player is not None:
            if self.player.l_available:
                self.save[2]['Sword'] = 1
            if self.player.h_available:
                self.save[2]['Hammer'] = 1
            if self.player.dash_available:
                self.save[2]['Dash'] = 1

    def damage_player(self, entity, amount, attack_type):
        if self.player.parry:
            self.player.parry_sound.play()
        elif self.player.vulnerable and entity.get_distance(self.player)[0] < entity.attack_radius + 100:
            self.player.hit_sound.play()
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    def run(self):
        self.visible_sprites.costume_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)
        # debug(self.visible_sprites.offset)
        # debug(self.player.rect.center, y=70)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2(0, 0)

        # background image
        self.floor_surface = pygame.image.load("NinjaAdventure/Field/Field.png").convert_alpha()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def costume_draw(self, player):
        self.offset.x = 0
        self.offset.y = 0
        for y in range(12):
            if (11 + y * 20) * TILESIZE < player.rect.centery < (24 + y * 20) * TILESIZE:
                for x in range(6):
                    if ((18.333 + x * 33) * TILESIZE) < player.rect.centerx < ((44.333 + x * 32.666) * TILESIZE):
                        self.offset.x = (18.33 + x * 33) * TILESIZE
                        self.offset.y = (10 + y * 20) * TILESIZE
                        break

        if self.offset == (0, 0):
            self.offset.x = player.rect.centerx - self.half_width
            self.offset.y = player.rect.centery - self.half_height
        # else:
        # self.offset.x = 18*TILESIZE
        # self.offset.y = 89*TILESIZE
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = []
        weapon_position = 1
        for sprite in self.sprites():
            if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy':
                if (self.offset.x < sprite.rect.centerx < self.offset.x + WIDTH
                        and self.offset.y < sprite.rect.centery < self.offset.y + HEIGHT
                        and not int(self.offset.x / TILESIZE - 18.33) % 33
                        and not (self.offset.y / TILESIZE - 10) % 20):
                    if not sprite.active and sprite.attack_type == 'range':
                        sprite.weapon_pos = weapon_position
                        sprite.active = True
                        weapon_position += 1
                    enemy_sprites.append(sprite)
                else:
                    sprite.active = False
                    sprite.can_attack = True
                    sprite.attacking = False
                    sprite.attack_time = None
                    sprite.direction = pygame.math.Vector2()
                    if 'Giant' in sprite.name:
                        sprite.status = 'idle'
                    elif '0' in sprite.name:
                        sprite.status = 'down'
                    else:
                        sprite.status = 'down_idle'
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
            # print(enemy.status)
