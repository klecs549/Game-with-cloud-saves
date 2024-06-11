import pygame
from code.settings import *
from code.entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, sprites, borders, create_attack, destroy_weapon, unlockable, save_game, check_death):
        super().__init__(groups)
        # load sprite
        self.sprite_type = 'player'
        self.sprites = pygame.image.load(
            "NinjaAdventure/Actor/Characters/BlackNinjaMage/SpriteSheet.png").convert_alpha()

        self.animations = self.import_animations()

        # set hitbox
        self.image = self.animations['up'][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-4, -1)
        self.obstacle_sprites = sprites[0]
        self.ranged_attack = sprites[1]
        self.abilities = sprites[2]
        self.teleports = sprites[3]
        self.campfires = sprites[4]
        self.borders = borders
        self.border_pos = 1

        # movement
        self.speed = 8
        self.status = 'down'

        # weapons
        self.create_attack = create_attack
        self.weapon_index = 0
        self.weapons = list(weapon_data.keys())
        self.destroy_weapon = destroy_weapon

        # l_attack
        self.l_available = unlockable['Sword']
        self.l_attacking = False
        self.l_attack_cooldown = 200
        self.l_attack_time = 0

        # h_attack
        self.h_available = unlockable['Hammer']
        self.h_attacking = False
        self.h_attack_cooldown = 600
        self.h_attack_time = 0

        # dash
        self.dash_available = unlockable['Dash']
        self.dashing = False
        self.dash_cooldown = 1000
        self.dash_time = 0

        #parry
        self.parry = False
        self.parry_cooldown = 500
        self.parry_time = 0

        # pick_up
        self.active = False
        self.pick_time = 0
        self.pick_cooldown = 400

        self.teleporting = False

        # save system
        self.save_game = save_game
        self.saving = True
        self.save_cd = 10000
        self.save_time = pygame.time.get_ticks()

        # stats
        self.max_hp = 6
        self.health = self.max_hp
        self.regen = 4
        self.current_regen = 0

        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        # self.timer_status = False
        # self.timer = 0
        # self.timer_cd = 1000

        #sound
        self.l_att_sound = pygame.mixer.Sound("NinjaAdventure/Sounds/Game/Sword.wav")
        self.l_att_sound.set_volume(0.2)
        self.h_att_sound = pygame.mixer.Sound("NinjaAdventure/Sounds/Game/Explosion.wav")
        self.h_att_sound.set_volume(0.3)
        self.dash_sound = pygame.mixer.Sound("NinjaAdventure/Sounds/Game/FX.wav")
        self.dash_sound.set_volume(0.3)
        self.hit_sound = pygame.mixer.Sound("NinjaAdventure/Sounds/Game/Hit.wav")
        self.hit_sound.set_volume(0.3)
        self.death_sound = pygame.mixer.Sound("NinjaAdventure/Sounds/Game/GameOver.wav")
        self.death_sound.set_volume(0.3)
        self.death = check_death
        self.pick_up_sound = pygame.mixer.Sound("NinjaAdventure/Sounds/Game/Success3.wav")
        self.pick_up_sound.set_volume(0.3)
        self.parry_sound = pygame.mixer.Sound("NinjaAdventure/Sounds/Game/Gold1.wav")

    def import_animations(self):
        animations = {'down': [], 'up': [], 'left': [], 'right': [],
                      'down_idle': [], 'up_idle': [], 'left_idle': [], 'right_idle': [],
                      'down_dash': [], 'up_dash': [], 'left_dash': [], 'right_dash': [],
                      'down_attack': [], 'up_attack': [], 'left_attack': [], 'right_attack': [],
                      'death': [], 'pick_up': []}

        for y_pos in range(0, 4):
            for x_pos in range(0, 7):
                name = list(animations.keys())[y_pos]
                if x_pos == 4:
                    name += '_attack'
                elif x_pos == 5:
                    name += '_dash'
                elif x_pos == 6 and y_pos == 0:
                    name = 'death'
                elif x_pos == 6 and y_pos == 1:
                    name = 'pick_up'
                if x_pos >= 6 and y_pos >= 2:
                    continue
                sprite = pygame.Surface((16, 16)).convert_alpha()
                sprite.blit(self.sprites, (0, 0), (y_pos * 16, x_pos * 16, 16, 16))
                sprite = pygame.transform.scale(sprite, (TILESIZE, TILESIZE))
                sprite.set_colorkey((0, 0, 0))
                animations[name].append(sprite)
                if x_pos == 0:
                    animations[name + '_idle'].append(sprite)
        return animations

    def input(self):
        if not self.dashing and not self.l_attacking and not self.h_attacking and not self.active and not self.parry:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_j] and not self.l_attacking:
                self.l_att_sound.play()
                self.l_attacking = True
                self.l_attack_time = pygame.time.get_ticks()
                if self.l_available:
                    self.weapon_index = 1
                else:
                    self.weapon_index = 0
                self.create_attack(self)
            elif keys[pygame.K_k] and not self.h_attacking and self.h_available:
                self.h_att_sound.play()
                self.h_attacking = True
                print(self.rect.y)
                self.h_attack_time = pygame.time.get_ticks()
                self.weapon_index = 2
                self.create_attack(self)

            if keys[pygame.K_l] and not self.dash_time and self.dash_available:
                self.dash_sound.play()
                self.dashing = True
                self.dash_time = pygame.time.get_ticks()
                self.speed = 20
                self.vulnerable = False
            elif not self.dashing:  # pygame.time.get_ticks() - self.dash_time > 200:
                self.speed = 6
            if keys[pygame.K_u] and not self.parry and not self.parry_time:
                self.parry = True
                self.parry_time = pygame.time.get_ticks()
                self.create_attack(self)

            if keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not '_' in self.status:
                self.status += '_idle'

        if self.l_attacking or self.h_attacking:
            if self.direction.x == 0 and self.direction.y == 0:
                if 'up' in self.status:
                    self.direction.y = -1
                elif 'down' in self.status:
                    self.direction.y = 1
                elif 'left' in self.status:
                    self.direction.x = -1
                else:
                    self.direction.x = 1
            if self.l_attacking:
                self.speed = 3
            if self.h_attacking:
                self.speed = 1
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('idle', 'attack')
                else:
                    self.status += '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')
        if self.dashing:
            if self.direction.x == 0 and self.direction.y == 0:
                if 'up' in self.status:
                    self.direction.y = -1
                elif 'down' in self.status:
                    self.direction.y = 1
                elif 'left' in self.status:
                    self.direction.x = -1
                else:
                    self.direction.x = 1

            if not 'dash' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('idle', 'dash')
                else:
                    self.status += '_dash'
        else:
            if 'dash' in self.status:
                self.status = self.status.replace('_dash', '')

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.l_attacking and current_time - self.l_attack_time >= self.l_attack_cooldown:
            self.l_attacking = False
            self.destroy_weapon(self)

        if self.h_attacking and current_time - self.h_attack_time >= self.h_attack_cooldown:
            self.h_attacking = False
            self.destroy_weapon(self)

        if self.dashing and current_time - self.dash_time >= 200:
            self.dashing = False
            self.vulnerable = True
        elif self.dash_time != 0 and current_time - self.dash_time >= self.dash_cooldown:
            self.dash_time = 0

        if current_time - self.parry_time >= 80 and self.parry:
            self.destroy_weapon(self)
            self.parry = False
        if current_time - self.parry_time >= self.parry_cooldown:
            self.parry_time = 0

        if self.active and current_time - self.pick_time >= self.pick_cooldown:
            self.active = False
            for sprite in self.abilities:
                if sprite.rect.colliderect(self.hitbox):
                    sprite.kill()
                    self.speed = 8

        if not self.vulnerable and not self.dashing:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True
        if self.saving and current_time - self.save_time >= self.save_cd:
            self.saving = False

    def animate(self):

        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        if not self.vulnerable and not self.dashing:
            alpha = self.wave_val()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def ranged_collision(self):
        for sprite in self.ranged_attack:
            if sprite.rect.colliderect(self.hitbox):
                if self.parry:
                    self.parry_sound.play()
                    sprite.kill()
                elif self.vulnerable:
                    self.hit_sound.play()
                    self.health -= 1
                    self.vulnerable = False
                    self.hurt_time = pygame.time.get_ticks()
                    sprite.kill()

    def abilities_collision(self):
        for sprite in self.abilities:
            if sprite.rect.colliderect(self.hitbox) and not self.active:
                self.pick_up_sound.play()
                self.speed = 0
                if sprite.name == 'Hammer':
                    self.h_available = True
                elif sprite.name == 'Dash':
                    self.dash_available = True
                else:
                    self.l_available = True
                self.active = True
                self.pick_time = pygame.time.get_ticks()
                self.status = "pick_up"
                sprite.rect = self.image.get_rect(center=self.rect.midbottom + pygame.math.Vector2(12, 0))

    def teleports_collision(self):
        for sprite in self.teleports:
            if sprite.rect.colliderect(self.hitbox):
                if not self.teleporting:
                    self.status = 'down_idle'
                    self.speed = 0
                    self.teleporting = True
                    sprite.active = True
                else:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_k]:
                        self.teleporting = False
                        self.hitbox = self.image.get_rect(center=sprite.rect.center + pygame.math.Vector2(60,0))
                        self.speed = 6
                        break
                    elif keys[pygame.K_s]:
                        direction = -2
                    elif keys[pygame.K_w]:
                        direction = 2
                    else:
                        direction = 0
                    start = sprite.rect.center
                    teleports = []
                    for teleport in self.teleports:
                        if teleport.rect.centery > sprite.rect.centery and teleport.active and direction == -2:
                            teleports.append(teleport)
                            self.hitbox = self.image.get_rect(center=teleport.rect.center + pygame.math.Vector2(60, 0))
                            self.teleporting = False
                            break
                        elif teleport.rect.centery < sprite.rect.centery and teleport.active and direction == 2:
                            teleports.append(teleport)
                            self.hitbox = self.image.get_rect(center=teleport.rect.center+ pygame.math.Vector2(60, 0))
                            self.teleporting = False
                            break

    def campfire_collision(self):
        for sprite in self.campfires:
            if sprite.rect.colliderect(self.hitbox):
                self.saving = True
                self.save_game()
                self.save_time = pygame.time.get_ticks()

    def regenerate(self):
        if self.l_available:
            if self.health == self.max_hp:
                self.current_regen = 0
            elif self.current_regen >= 4:
                if self.health < self.max_hp:
                    self.health += 1
                self.current_regen = 0
        else:
            self.current_regen = 0

    def update(self):
        if not self.teleporting:
            self.input()
        self.choose_border()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move()
        self.ranged_collision()
        self.regenerate()
        self.abilities_collision()
        self.teleports_collision()
        self.death()
        if not self.saving:
            self.campfire_collision()
