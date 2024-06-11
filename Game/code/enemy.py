import pygame
from code.entity import Entity
from code.settings import *


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, borders, damage, create_attack, destroy, alive):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.name = monster_name
        monster_info = enemies[self.name]
        self.info = monster_info
        self.health = monster_info['hp']
        self.speed = self.info['speed']
        self.attack_radius = monster_info['attack_radius']
        self.resistance = monster_info['resistance']
        self.pushing = monster_info['pushing']
        self.damage = monster_info['attack_damage']
        self.attack_type = monster_info['type']
        self.active = False
        self.alive = alive

        self.sprites = pygame.image.load(f'NinjaAdventure/Actor/Enemies/{monster_name}/SpriteSheet.png')
        self.status = 'down_idle'
        if 'Giant' in self.name:
            self.status = "attack"

        self.animations = self.import_animations()
        self.image = self.animations[self.status][0]

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.borders = borders
        self.border_pos = 1

        # interactions
        self.can_attack = True
        self.attacking = False
        self.attack_time = None
        self.attack_cooldown = monster_info['attack_cooldown']
        self.damage_player = damage

        self.punching = False
        self.punching_cooldown = 300
        self.punching_time = 0

        # ranged_attacks
        self.create_attack = create_attack
        self.destroy_attack = destroy
        self.weapon_pos = 1
        self.completed = False
        self.projectile = None

        self.vulnerable = True
        self.hit_time = None
        self.invincible_duration = 200

        # sounds
        if 'Giant' in self.name:
            self.death_sound = pygame.mixer.Sound('NinjaAdventure/Sounds/Game/Fire2.wav')
            self.death_sound.set_volume(0.2)
        else:
            self.death_sound = pygame.mixer.Sound('NinjaAdventure/Sounds/Game/Kill.wav')
            self.death_sound.set_volume(0.5)
        if self.attack_type == 'range':
            self.attack_sound = pygame.mixer.Sound('NinjaAdventure/Sounds/Game/Fireball.wav')
            self.attack_sound.set_volume(0.2)

    def import_animations(self):
        if 'Giant' in self.name:
            animations = {'idle': [], 'jump': [], 'attack': []}
            for x_pos in range(3):
                count = boss_animations[self.name][x_pos]
                name = list(animations.keys())[x_pos]
                for y_pos in range(count):
                    if 'Frog' in self.name:
                        size = 40
                    else:
                        size = 60

                    sprite = pygame.Surface((size, size)).convert_alpha()
                    sprite.blit(self.sprites, (0, 0), (y_pos * size, x_pos * size, size, size))
                    sprite = pygame.transform.scale_by(sprite, 3)
                    sprite.set_colorkey((0, 0, 0))
                    animations[name].append(sprite)
            return animations

        else:
            animations = {'down': [], 'up': [], 'left': [], 'right': [],
                          'down_idle': [], 'up_idle': [], 'left_idle': [], 'right_idle': [],
                          'down_dash': [], 'up_dash': [], 'left_dash': [], 'right_dash': [],
                          'down_attack': [], 'up_attack': [], 'left_attack': [], 'right_attack': [], }
        for y_pos in range(0, 4):
            for x_pos in range(0, 6):
                name = list(animations.keys())[y_pos]
                if x_pos > 3 and '0' in self.name:
                    break
                elif x_pos == 4:
                    name += '_attack'
                elif x_pos == 5:
                    name += '_dash'
                sprite = pygame.Surface((16, 16)).convert_alpha()
                sprite.blit(self.sprites, (0, 0), (y_pos * 16, x_pos * 16, 16, 16))
                sprite = pygame.transform.scale(sprite, (48, 48))
                sprite.set_colorkey((0, 0, 0))
                animations[name].append(sprite)
                if '0' in self.name:
                    animations[name + '_idle'].append(sprite)
                    animations[name + '_attack'].append(sprite)
                elif x_pos == 0:
                    animations[name + '_idle'].append(sprite)

        return animations

    def get_distance(self, player):
        enemy_vector = pygame.Vector2(self.rect.center)
        player_vector = pygame.Vector2(player.rect.center)
        distance = (player_vector - enemy_vector).magnitude()
        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.Vector2()
        return distance, direction

    def get_status(self, player):
        distance = self.get_distance(player)[0]
        if not self.attacking:
            if distance <= self.attack_radius and self.can_attack:
                if not 'attack' in self.status:
                    self.frame_index = 0
                    self.attacking = True
                if 'Giant' in self.name:
                    self.status = 'attack'
                elif not 'attack' in self.status:
                    if abs(self.direction.y) > abs(self.direction.x):
                        if self.direction.y < 0:
                            self.status = 'up'
                        elif self.direction.y > 0:
                            self.status = 'down'
                    else:
                        if self.direction.x < 0:
                            self.status = 'left'
                        else:
                            self.status = 'right'
                    self.status += '_attack'
            else:
                if self.attack_type == 'range':
                    self.speed = 0
                if 'Giant' in self.name:
                    self.status = 'jump'
                else:
                    self.status = 'down'
            if distance > self.attack_radius:
                self.speed = self.info['speed']

    def actions(self, player):
        if 'attack' in self.status:
            self.attack_time = pygame.time.get_ticks()
            if 'Giant' in self.name:
                self.speed = 0
            if self.attack_type == 'range' and not self.completed:
                self.speed = 0
                self.destroy_attack(self)
                self.create_attack(self)
                self.completed = True
            # elif self.attack_type != 'range':
            # self.damage_player(self.damage, self.attack_type)
            if '0' in self.name and self.can_attack:
                self.direction = self.get_distance(player)[1]
            elif self.attack_type != 'range':
                self.direction = pygame.Vector2(0, 0)
        elif not 'attack' in self.status:
            self.completed = False
            if self.attack_type == 'range':
                self.destroy_attack(self)
            if not self.attack_time == 'range':
                self.direction = self.get_distance(player)[1]
        elif not self.attack_time == 'range':
            self.direction = pygame.Vector2()

    def animate(self):
        self.frame_index += self.animation_speed
        if self.attack_type != 'range' and self.can_attack and self.attacking:
            if (('Giant' in self.name and int(self.frame_index) == (len(self.animations[self.status]) - 4))
                    or (not 'Giant' in self.name and int(self.frame_index) == len(self.animations[self.status]) and not self.punching)):
                self.damage_player(self, self.damage, self.attack_type)
                if not 'Giant' in self.name:
                    self.punching = True
                    self.punching_time = pygame.time.get_ticks()
                    print(self.punching_time)
        if int(self.frame_index) >= len(self.animations[self.status]):
            if 'attack' in self.status:
                # if self.can_attack:
                self.can_attack = False
                self.attacking = False
                if self.attack_type == 'range' and self.weapon_pos != 0:
                    self.attack_sound.play()
                    self.destroy_attack(self, 1)
                    self.create_attack(self, 1)
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]
        if not self.vulnerable:
            alpha = self.wave_val()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
                # if self.attack_type == 'range' and self.weapon_pos != 0:
                #     self.destroy_attack(self, 1)
                self.destroy_attack(self)
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincible_duration:
                self.vulnerable = True
        if self.punching:
            if current_time - self.punching_time >= self.punching_cooldown:
                self.punching = False

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_distance(player)[1]
            if attack_type == 'weapon':
                damage = weapon_data[player.weapons[player.weapon_index]]['damage']
                if damage - self.resistance > 0:
                    self.health -= (damage - self.resistance)
                    self.vulnerable = False
                    self.hit_time = pygame.time.get_ticks()
                if player.weapon_index == 2:
                    self.invincible_duration = 600
                else:
                    player.current_regen += 1
                    self.invincible_duration = 200

    def hit_reaction(self, player):
        self.direction = self.get_distance(player)[1]
        self.direction *= -self.pushing

    def check_death(self):
        if self.health <= 0:
            self.death_sound.play()
            if self.attack_type == 'range':
                self.destroy_attack(self)
                self.destroy_attack(self, 1)
            if 'Giant' in self.name:
                self.alive[self.name] = 1

            self.kill()

    def update(self):
        self.animate()
        self.move()

    def enemy_update(self, player):
        self.choose_border()
        self.cooldown()
        self.get_status(player)
        self.actions(player)
        self.check_death()
        # print(self.punching)
        self.hit_reaction(player)
        if self.vulnerable:
            self.direction = self.get_distance(player)[1]
