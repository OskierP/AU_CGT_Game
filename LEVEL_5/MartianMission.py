import os
import pygame
from pygame import mixer
import random
import csv
import LEVEL_5.button as button
from PIL import Image
from pygame.locals import *

def main():
    mixer.init()
    pygame.init()

    clock = pygame.time.Clock()
    fps = 50

    screen_width = 1100
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Martian Mission')

    #define game vars
    GRAV = .45
    SCROLL_THRESH = 200
    ROWS = 15
    COLS = 150
    TILE_SIZE = int(screen_height // ROWS)
    TILE_TYPES = 11
    MAX_LEVELS = 2
    screen_scroll = 0
    bg_scroll = 0
    level = 0
    start_game = False
    start_intro = False

    #player action variables
    movl = False
    movr = False
    shoot = False
    laser = False
    laser_thrown = False

    #load music and sounds
    pygame.mixer.music.load('LEVEL_5/music/audio_space1.mp3')
    pygame.mixer.music.set_volume(.3)
    pygame.mixer.music.play(-1, 0.0, 5000)

    jump_fx = pygame.mixer.Sound('LEVEL_5/music/audio_jump.wav')
    jump_fx.set_volume(.5)
    shot_fx = pygame.mixer.Sound('LEVEL_5/music/audio_shot.wav')
    shot_fx.set_volume(.5)
    bomb_fx = pygame.mixer.Sound('LEVEL_5/music/audio_grenade.wav')
    bomb_fx.set_volume(.5)



    #load images
    #background image
    bg_img = pygame.image.load('LEVEL_5/img/pixelMars.png').convert_alpha()
    bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

    #button images
    start_btn = pygame.image.load('LEVEL_5/img/start_btn.png')
    restart_btn = pygame.image.load('LEVEL_5/img/restart_btn.png')
    exit_btn = pygame.image.load('LEVEL_5/img/exit_btn.png')

    #store tile images in list
    img_list = []
    for x in range(TILE_TYPES):
        img = pygame.image.load(f'LEVEL_5/img/Tiles/tile{x}.png')
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        img_list.append(img)
    #energy ball
    ebullet_img = pygame.image.load('LEVEL_5/img/hsLaser.png').convert_alpha()
    ebullet_img = pygame.transform.scale(ebullet_img, (40, 40))
    #Alien bomb
    laser_img = pygame.image.load('LEVEL_5/img/yelball.png').convert_alpha()
    laser_img = pygame.transform.scale(laser_img, (30, 30))
    #Item drops
    health_drop_img = pygame.image.load('LEVEL_5/img/drops/health_drop.png').convert_alpha()
    health_drop_img = pygame.transform.scale(health_drop_img, (80, 80))
    energy_ammo_img = pygame.image.load('LEVEL_5/img/drops/energy_ammo.png').convert_alpha()
    energy_ammo_img = pygame.transform.scale(energy_ammo_img, (30, 22))
    special_ammo_img = pygame.image.load('LEVEL_5/img/drops/special_ammo.png').convert_alpha()
    special_ammo_img = pygame.transform.scale(special_ammo_img, (30, 27))
    item_drops = {'Health'  : health_drop_img,
                  'Ammo'    : energy_ammo_img,
                  'Special' : special_ammo_img
                  }

    #define colors
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PINK = (235, 65, 54)

    #define font
    font = pygame.font.SysFont('Futura', 25)

    def draw_text(text, font, text_color, x, y):
        img = font.render(text, True, text_color)
        screen.blit(img, (x, y))

    def draw_bg():
        screen.fill(BLUE)
        width = bg_img.get_width()
        for x in range(5):
            screen.blit(bg_img, ((x * width) - bg_scroll * .5, 0))
        #draw line for floor
        #pygame.draw.line(screen, GREEN, (0, 550), (screen_width, 550))

    def restart_lvl():
        enemy_group.empty()
        ebullet_group.empty()
        laser_group.empty()
        exp_group.empty()
        item_drop_group.empty()
        water_group.empty()
        exit_group.empty()

        #create empty tile list
        w_data = []
        for row in range(ROWS):
            r = [-1] * COLS
            w_data.append(r)
        return w_data

    class Dog(pygame.sprite.Sprite):
        def __init__(self, char_type, x, y, scale, speed, ammo, laser):
            pygame.sprite.Sprite.__init__(self)
            self.alive = True
            self.char_type = char_type
            self.x = x
            self.y = y
            self.scale = scale
            self.speed = speed
            self.ammo = ammo
            self.start_ammo = ammo
            self.shoot_cooldown = 0
            self.laser = laser
            self.health = 100
            self.max_health = self.health
            self.direction = 1
            self.vel_y = 0
            self.jump = False
            self.in_air = True
            self.flip = False
            self.dog_list = []
            self.frame_index = 0
            self.action = 0
            self.update_time = pygame.time.get_ticks()
            # ai variables
            self.move_counter = 0
            self.idling = False
            self.idling_counter = 0
            self.vision = pygame.Rect(0, 0, 200, 30)
            self.wall = False

            #load player images
            animation_types = ['Idle', 'Run', 'Jump', 'Death']
            for animation in animation_types:
                #reset temporary list of images
                temp_list = []
                #count number of files in the folder
                num_of_frames = len(os.listdir(f'LEVEL_5/img/{self.char_type}/{animation}'))
                for i in range(num_of_frames):
                    img = pygame.image.load(f'LEVEL_5/img/{self.char_type}/{animation}/char{i}.png').convert_alpha()
                    img = pygame.transform.scale(img, (int(45 * scale), int(50 * scale)))
                    temp_list.append(img)
                    self.dog_list.append(temp_list)

            self.image = self.dog_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.width = self.image.get_width()
            self.height = self.image.get_height()


        def update(self):
            self.update_animation()
            self.check_alive()
            if self.shoot_cooldown > 0:

                self.shoot_cooldown -= 1


        def move(self, movl, movr):
            #reset movement vars
            screen_scroll = 0
            dx = 0
            dy = 0

            #assign movement vars if moving left or right
            if movl:
                dx = -self.speed
                self.flip = True
                self.direction = -1
            if movr:
                dx = self.speed
                self.flip = False
                self.direction = 1

            #jump
            if self.jump == True and self.in_air == False:
               self.vel_y = -11
               self.jump = False
               self.in_air = True

            #apply gravity
            self.vel_y += GRAV
            if self.vel_y > 10:
                self.vel_y
            dy += self.vel_y

            #check collision
            for tile in world.obstacle_list:
                #collisions in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                    # turn around ai if it hits a wall
                    if self.char_type == 'enemy':
                        self.direction *= -1
                        self.move_counter = 0

                #collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check above or below ground
                    if self.vel_y < 0:
                        self.vel_y = 0
                        dy = tile[1].bottom - self.rect.top
                    elif self.vel_y >= 0:
                        self.vel_y = 0
                        self.in_air = False
                        dy = tile[1].top - self.rect.bottom

            #collision in x direction
            # if self.rect.bottom + dy > 550:
            #     dy = 550 - self.rect.bottom
            #     self.in_air = False

            #check for collision with water
            if pygame.sprite.spritecollide(self, water_group, False):
                self.health = 0

            #check for collision with exit
            level_complete = False
            if pygame.sprite.spritecollide(self, exit_group, False):
                level_complete = True

            #check if fallen off the map
            if self.rect.bottom > screen_height:
                self.health = 0
                print(self.health)

            #check is going off screen edges
            if self.char_type == 'dog':
                if self.rect.left + dx < 0 or self.rect.right + dx > screen_width:
                    dx = 0

            #update rect pos
            self.rect.x += dx
            self.rect.y += dy

            #update scroll based on player pos
            if self.char_type == 'dog':
                if (self.rect.right >= screen_width - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - screen_width)\
                        or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                    self.rect.x -= dx
                    screen_scroll = -dx
            return screen_scroll, level_complete

        def shoot(self):
            if self.shoot_cooldown == 0 and self.ammo > 0:
                self.shoot_cooldown = 20
                ebullet = Bullet(self.rect.centerx + (0.96 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
                ebullet_group.add(ebullet)
                #reduce ammo
                self.ammo -= 1
                shot_fx.play()

        def ai(self):
            if self.alive and player.alive:
                if self.idling == False and random.randint(1, 500) == 1:
                    self.update_action(0)# idle
                    self.idling = True
                    self.idling_counter = 50
                #check if ai is near the player
                if self.vision.colliderect(player.rect):
                    # for tile in world.obstacle_list:
                    #     if self.vision.colliderect(tile[1]):
                    #         self.wall = True
                    # if self.wall == False:
                    #stop running and face player
                    self.update_action(0)# idle
                    #shoot
                    self.shoot()
                else:
                    if self.idling == False:
                        if self.direction == 1:
                            ai_mov_right = True
                        else:
                            ai_mov_right = False
                        ai_mov_left = not ai_mov_right
                        self.move(ai_mov_left, ai_mov_right)
                        self.update_action(1)# run
                        self.move_counter += 1
                        #update ai vision while enemy moves
                        self.vision.center = (self.rect.centerx + 100 * self.direction, self.rect.centery)
                        #Show enemy vision
                        #pygame.draw.rect(screen, RED, self.vision)

                        if self.move_counter > TILE_SIZE:
                            self.direction *= -1
                            self.move_counter *= -1
                    else:
                        self.idling_counter -= 1
                        if self.idling_counter <= 0:
                            self.idling = False
            #scroll
            self.rect.x += screen_scroll


        def update_animation(self):
            #update animation
            ANIMATION_COOLDOWN = 100
            #update image depending on current frame
            self.image = self.dog_list[self.action][self.frame_index]
            #check if enough time has passed since the last update
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            #if the animation has run out the reset back to the start
            if self.frame_index >= len(self.dog_list[self.action]):
                if self.action == 3:
                    self.frame_index = len(self.dog_list[self.action]) - 1
                else:
                    self.frame_index = 0

        def update_action(self, new_action):
            #check if the new action is different to the previous one
            if new_action != self.action:
                self.action = new_action
                #update the animation settings
                self.frame_index = 0
                self.update_time = pygame.time.get_ticks()

        def check_alive(self):
            if self.health <= 0:
                self.health = 0
                self.speed = 0
                self.alive = False
                self.update_action(3)
                if player.health <= 0:
                    pygame.mixer.music.rewind()
            # if self.char_type == 'enemy' and self.alive == False:


        def draw(self):
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    class World():
        def __init__(self):
            self.obstacle_list = []

        def process_data(self, data):
            self.level_length = len(data[0])
            #iterate through in value in level data
            for y, row in enumerate(data):
                for x, tile in enumerate(row):
                    if tile >= 0:
                        img = img_list[tile]
                        img_rect = img.get_rect()
                        img_rect.x = x * TILE_SIZE
                        img_rect.y = y * TILE_SIZE
                        tile_data = (img, img_rect)
                        if tile == 0:
                            self.obstacle_list.append(tile_data)
                        elif tile == 8:
                            self.obstacle_list.append(tile_data)
                        elif tile == 9:
                            self.obstacle_list.append(tile_data)
                        elif tile >= 6 and tile <= 7:
                            water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                            water_group.add(water)
                        elif tile == 10:#change level
                            exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                            exit_group.add(exit)
                        elif tile == 4:#players
                            player = Dog('dog', x * TILE_SIZE, y * TILE_SIZE, 1, 5, 20, 4)
                            health_bar = HealthBar(10, 10, player.health, player.health)
                        elif tile == 5:#enemies
                            enemy = Dog('enemy', x * TILE_SIZE, y * TILE_SIZE, 1, 2, 20, 0)
                            enemy_group.add(enemy)
                        elif tile == 1:#health drop
                            item_drop = ItemDrop('Health', x * TILE_SIZE, y * TILE_SIZE)
                            item_drop_group.add(item_drop)
                        elif tile == 2:#ammo drop
                            item_drop = ItemDrop('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                            item_drop_group.add(item_drop)
                        elif tile == 3:#special ammo drop
                            item_drop = ItemDrop('Special', x * TILE_SIZE, y * TILE_SIZE)
                            item_drop_group.add(item_drop)


            return player, health_bar

        def draw(self):
            for tile in self.obstacle_list:
                tile[1][0] += screen_scroll
                screen.blit(tile[0], tile[1])

    class Water(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

        def update(self):
            self.rect.x += screen_scroll

    class Exit(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

        def update(self):
            self.rect.x += screen_scroll


    class ItemDrop(pygame.sprite.Sprite):
        def __init__(self, item_type, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.item_type = item_type
            self.image = item_drops[self.item_type]
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

        def update(self):
            # scroll
            self.rect.x += screen_scroll
            #check if player pick up item drop
            if pygame.sprite.collide_rect(self, player):
                #check item drop type
                if self.item_type == 'Health':
                    player.health += 25
                    if player.health > player.max_health:
                        player.health = player.max_health
                elif self.item_type == 'Ammo':
                    player.ammo += 15
                elif self.item_type == 'Special':
                    player.laser += 3
                #delete drops
                self.kill()


    class HealthBar():
        def __init__(self, x, y, health, max_health):
            self.x = x
            self.y = y
            self.health = health
            self.max_health = max_health

        def draw(self, health):
            #update with new health
            self.health = health
            #calculate health ratio
            ratio = self.health / self.max_health
            pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
            pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
            pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))


    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, direction):
            pygame.sprite.Sprite.__init__(self)
            self.speed = 10
            self.direction = direction
            if self.direction == 1:
                self.image = ebullet_img
            elif self.direction == -1:
                self.image = pygame.transform.flip(ebullet_img, True, False)
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)


        def update(self):
            #move bullet
            self.rect.x += (self.direction * self.speed) + screen_scroll
            #check if bullet has gone off screen
            if self.rect.right < 0 or self.rect.left > screen_width:
                self.kill()

            #check collision with characters
            if pygame.sprite.spritecollide(player, ebullet_group, False):
                if player.alive:
                    player.health -= 10
                    self.kill()
            for enemy in enemy_group:
                if pygame.sprite.spritecollide(enemy, ebullet_group, False):
                    if enemy.alive:
                        enemy.health -= 25
                        self.kill()
            #check for collision with tiles
            for tile in world.obstacle_list:
                if tile[1].colliderect(self.rect):
                    self.kill()

    class Laser(pygame.sprite.Sprite):
        def __init__(self, x, y, direction):
            pygame.sprite.Sprite.__init__(self)
            self.timer = 100
            self.vel_y = -11
            self.speed = 7
            self.image = laser_img
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.direction = direction
            self.width = self.image.get_width ()
            self.height = self.image.get_height ()

        def update(self):
            self.vel_y += GRAV + .1
            dx = self.direction * self.speed
            dy = self.vel_y

            for tile in world.obstacle_list:
                #check collsion with walls
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    self.direction *= -1
                    dx = self.direction * self.speed
                 #collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    self.speed = 0
                    #check if thrown up
                    if self.vel_y < 0:
                        self.vel_y = 0
                        dy = tile[1].bottom - self.rect.top
                    #check if falling
                    elif self.vel_y >= 0:
                        self.vel_y = 0
                        dy = tile[1].top - self.rect.bottom


            #update laser pos
            self.rect.x += dx + screen_scroll
            self.rect.y += dy

            #exp countdown timer
            self.timer -= 1
            if self.timer <= 0:
                self.kill()
                bomb_fx.play()
                exp = Explosion(self.rect.x, self.rect.y, 0.4)
                exp_group.add(exp)
                #do damage to players in radius
                if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                   abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                    player.health -= 50
                    #print(player.health)
                for enemy in enemy_group:
                    if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                       abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                        enemy.health -= 50



    class Explosion(pygame.sprite.Sprite):
        def __init__(self, x, y, scale):
            pygame.sprite.Sprite.__init__(self)
            self.images = []
            for num in range(0,6):
                img = pygame.image.load(f'LEVEL_5/img/explosions/explosion{num}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), (int(img.get_height() * scale))))
                self.images.append(img)
            self.frame_index = 0
            self.image = self.images[self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.counter = 0

        def update(self):
            # scroll
            self.rect.x += screen_scroll
            exp_speed = 4
            #update exp animation
            self.counter += 1

            if self.counter >= exp_speed:
                self.counter = 0
                self.frame_index += 1
                #if animation if complete delete explosion
                if self.frame_index >= len(self.images):
                    self.kill()
                else:
                    self.image = self.images[self.frame_index]



    class ScreenFade():
        def __init__(self, direction, colour, speed):
            self.direction = direction
            self.colour = colour
            self.speed = speed
            self.fade_counter = 0

        def fade(self):
            fade_complete = False
            self.fade_counter += self.speed
            if self.direction == 1:#whole screen fade
                pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, screen_width // 2, screen_height))
                pygame.draw.rect(screen, self.colour, (screen_width // 2 + self.fade_counter, 0, screen_width, screen_height))
                pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, screen_width, screen_height // 2))
                pygame.draw.rect(screen, self.colour, (0, screen_height // 2 +self.fade_counter, screen_width, screen_height))
            if self.direction == 2:#vertical screen fade down
                pygame.draw.rect(screen, self.colour, (0, 0, screen_width, 0 + self.fade_counter))
            if self.fade_counter >= screen_width:
                fade_complete = True

            return fade_complete


    #create screen fades
    intro_fade = ScreenFade(1, BLACK, 4)
    death_fade = ScreenFade(2, PINK, 6)

    #create buttons
    start_button = button.Button(screen_width // 2 - 130, screen_height // 2 - 150, start_btn, 1)
    exit_button = button.Button(screen_width // 2 - 110, screen_height // 2 + 50, exit_btn, 1)
    restart_button = button.Button(screen_width // 2 - 100, screen_height // 2 - 50, restart_btn, 2)

    #create sprite groups
    enemy_group = pygame.sprite.Group()
    ebullet_group = pygame.sprite.Group()
    laser_group = pygame.sprite.Group()
    exp_group = pygame.sprite.Group()
    item_drop_group = pygame.sprite.Group()
    water_group = pygame.sprite.Group()
    exit_group = pygame.sprite.Group()

    #create empty tile list for world
    world_data = []
    for row in range(ROWS):
        r = [-1] * COLS
        world_data.append(r)
        #print(r)
    #load in level data and create world
    with open(f'LEVEL_5/LevelEditor/level{level}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)
    world = World()
    player, health_bar = world.process_data(world_data)



    run = True
    while run:

        clock.tick(fps)

        if start_game == False:
            #level 4/draw menu
            screen.fill(BLACK)
            if start_button.draw(screen):
                start_game = True
                start_intro = True
            if exit_button.draw(screen):
                run = False
        else:
            #update background
            draw_bg()
            #draw map
            world.draw()
            #show player health
            health_bar.draw(player.health)
            #show ammo
            #draw_text(f'AMMO: {player.ammo}', font, WHITE, 10, 35)
            draw_text('AMMO: ', font, WHITE, 10, 40)
            for x in range(player.ammo):
                screen.blit(ebullet_img, (80 + (x * 10), 25))
            #draw_text(f'Special: {player.laser}', font, WHITE, 10, 60)
            draw_text('Special: ' , font , WHITE , 10 , 65)
            for x in range(player.laser):
                screen.blit(laser_img, (85 + (x * 15), 60))

            player.update()
            player.draw()

            for enemy in enemy_group:
                enemy.ai()
                enemy.update()
                enemy.draw()

            #update and draw groups
            ebullet_group.update()
            laser_group.update()
            exp_group.update()
            exit_group.update()
            item_drop_group.update()
            water_group.update()
            ebullet_group.draw(screen)
            laser_group.draw(screen)
            exp_group.draw(screen)
            item_drop_group.draw(screen)
            water_group.draw(screen)
            exit_group.draw(screen)

            #show intro
            if start_intro == True:
                if intro_fade.fade():
                    start_intro = False
                    intro_fade.fade_counter = 0

            #update player actions
            if player.alive:
                #shoot bullets
                if shoot:
                    player.shoot()
                elif laser and laser_thrown == False and player.laser > 0:
                    laser = Laser(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction), \
                                  player.rect.top, player.direction)
                    laser_group.add(laser)
                    #reduce laser
                    player.laser -= 1
                    laser_thrown = True
                if player.in_air:
                    player.update_action(2)#2: jump
                elif movl or movr:
                    player.update_action(1)#1: run
                else:
                    player.update_action(0)#0: idle
                screen_scroll, level_complete = player.move(movl, movr)
                bg_scroll -= screen_scroll
                if level_complete:
                    level += 1
                    bg_scroll = 0
                    world_data = restart_lvl()
                    if level <= MAX_LEVELS:
                        # load in level data and create world
                        with open ( f'LEVEL_5/LevelEditor/level{level}_data.csv' , newline = '' ) as csvfile:
                            reader = csv.reader ( csvfile , delimiter = ',' )
                            for x , row in enumerate ( reader ):
                                for y , tile in enumerate ( row ):
                                    world_data[x][y] = int ( tile )
                        world = World ()
                        player, health_bar = world.process_data (world_data)
            else:
                screen_scroll = 0
                if death_fade.fade():
                    if restart_button.draw(screen):
                        death_fade.fade_counter = 0
                        start_intro = True
                        bg_scroll = 0
                        world_data = restart_lvl()
                        #load in level data and create world
                        with open(f'LEVEL_5/LevelEditor/level{level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter = ',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        player, health_bar = world.process_data(world_data)

        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                run = False
            #keyboard presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    movl = True
                if event.key == pygame.K_RIGHT:
                    movr = True
                if event.key == pygame.K_LCTRL:
                    shoot = True
                if event.key == pygame.K_LALT:
                    laser = True
                if event.key == pygame.K_SPACE and player.alive:
                    player.jump = True
                    #stop sound from playing when player is in air
                    if player.in_air == False:
                        jump_fx.play()
                if event.key == pygame.K_ESCAPE:
                    run = False

            # keyboard releases
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    movl = False
                if event.key == pygame.K_RIGHT:
                    movr = False
                if event.key == pygame.K_LCTRL:
                    shoot = False
                if event.key == pygame.K_LALT:
                    laser = False
                    laser_thrown = False
                if event.key == pygame.K_SPACE:
                    player.jump = False

        pygame.display.update()

    pygame.quit()
