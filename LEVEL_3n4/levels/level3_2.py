import time

import pygame

import LEVEL_3n4.collisions as collisions
import LEVEL_3n4.display_game as DisplayGame
import LEVEL_3n4.sprite as sprite
import flags as flags
from LEVEL_3n4.movable_objects import Player, Box

next_level = False


def run_level(run):
    ################################# LOAD UP A BASIC WINDOW AND CLOCK #################################
    pygame.init()
    display_width = 1100  # 1100
    display_height = 600  # 600
    was_pressed = False

    pygame.mixer.music.load('LEVEL_3n4/assets/sound/deep_space_music.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    button_click = pygame.mixer.Sound('LEVEL_3n4/assets/sound/button_click_effect.wav')
    jump_sound = pygame.mixer.Sound('LEVEL_3n4/assets/sound/audio_jump.wav')

    running = run
    clock = pygame.time.Clock()
    target_fps = 60

    gravity = 0
    friction = 0

    font = pygame.font.Font('freesansbold.ttf', 22)
    text = font.render('Press B to press the button', True, (0, 0, 0))
    text_box = text.get_rect()
    text_box.center = (display_width // 2, display_height // 2 - 150)
    ################################# LOAD PLAYER AND SPRITE SHEET###################################
    game_display = DisplayGame.GameDisplay(display_width, display_height).display_game()
    level_4_2_background = sprite.Sprite('LEVEL_3n4/assets/sprites/background/level4_2.png').load_image()

    dog = Player('LEVEL_3n4/assets/sprites/player/dog_anim_left.png', 5, gravity, friction)
    scale = 2.25

    box = Box('LEVEL_3n4/assets/sprites/movable_obj/box.png', gravity, friction)
    box2 = Box('LEVEL_3n4/assets/sprites/movable_obj/box.png', gravity, friction)

    move_arr = [dog, box, box2]

    ################################# OBSTACLES ####################################
    ceiling = sprite.Obstacles(1100, 20, 0, 0)

    floor = sprite.Obstacles(1200, 20, 0, 570)  # spikes

    top = sprite.Platform(990, 50, 150)
    arr = []
    for i in range(10):
        arr.append(sprite.Platform(980, 50 + 20 * i, 20))
    arr_wall = sprite.Obstacles(20, 100, 980, 50)

    wall_right = sprite.Obstacles(20, 900, 1090, 0)
    wall_left = sprite.Obstacles(10, 900, 30, 0)

    platform = sprite.Platform(0, 230, 340)
    platform1 = sprite.Platform(850, 450, 300)
    platform2 = sprite.Platform(450, 350, 300)

    limitor1_1 = sprite.Platform(850, 430, 20)
    limitor2_1 = sprite.Platform(450, 340, 20)
    limitor2_2 = sprite.Platform(730, 340, 20)
    limitor3_1 = sprite.Platform(320, 210, 20)

    platform_arr = [platform, platform1, platform2]
    limitor_arr = [limitor1_1, limitor2_1, limitor2_2, limitor3_1]

    ##BUTTONS##

    press_gravity = sprite.ActionPlace('LEVEL_3n4/assets/sprites/action_place/button.png', 1010, 100, 40, 40)
    keyboard = sprite.ActionPlace('LEVEL_3n4/assets/sprites/action_place/keyboard.png', 50, 150, 40, 40)
    spikes = sprite.ActionPlace_2(1200, 20, 0, 550)

    ########## COLLISIONS ##################

    collision_objects_player = [spikes, floor, wall_right, wall_left, box, box2, ceiling, platform, platform1,
                                platform2, limitor1_1, limitor2_1, limitor2_2, limitor3_1, top, arr_wall]

    collision_objects_box = [floor, wall_right, wall_left, platform1, platform2, limitor1_1, limitor2_1, limitor2_2]
    #################################### LOAD THE LEVEL #######################################
    dog.position.x, dog.position.y = 1000, 100

    box.position.x, box.position.y = 600, 200
    box.width, box.height = 20, 20

    box2.position.x, box2.position.y = 900, 200
    box2.width, box2.height = 20, 20

    ################################# GAME LOOP ##########################
    flag = True

    while running:
        dt = clock.tick(60) * .001 * target_fps
        game_display.blit(level_4_2_background, (0, 0))

        ################################# CHECK PLAYER INPUT #################################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                flags.next_lvl_3_2.set_flag(True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dog.LEFT_KEY = True
                elif event.key == pygame.K_RIGHT:
                    dog.RIGHT_KEY = True
                elif event.key == pygame.K_UP:
                    dog.jump()
                    jump_sound.play()
                    jump_sound.set_volume(0.5)
                elif event.key == pygame.K_UP and not gravity and not friction:
                    dog.acceleration.y -= .5
                # elif event.key == pygame.K_j:  # to delete
                #     if flag:
                #         gravity = 0.21
                #         friction = -.12
                #         flag = False
                #         # was_pressed = True to change
                #     else:
                #         gravity = 0
                #         friction = 0
                #         flag = True
                #     for obj in move_arr:
                #         obj.gravity = gravity
                #         obj.friction = friction

                elif event.key == pygame.K_b and press_gravity.flag and not was_pressed:
                    button_click.play()
                    button_click.set_volume(0.5)
                    gravity = 0.21
                    friction = -.12
                    was_pressed = True
                    for obj in move_arr:
                        obj.gravity = gravity
                        obj.friction = friction
                elif event.key == pygame.K_b and keyboard.flag:
                    button_click.play()
                    button_click.set_volume(0.5)
                    time.sleep(1)
                    running = False
                    flags.next_lvl_3_2.set_flag(True)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    dog.LEFT_KEY = False
                    dog.frame = 0
                elif event.key == pygame.K_RIGHT:
                    dog.RIGHT_KEY = False
                    dog.frame = 0
                elif event.key == pygame.K_UP:
                    if dog.is_jumping:
                        dog.velocity.y *= .25
                        dog.is_jumping = False

        ################################# UPDATE WINDOW AND DISPLAY #################################

        dog.collisions = collisions.collision_test(dog.rect, collision_objects_player)
        dog.collision_with_box = collisions.collision_test(dog.rect, [box, box2])
        box.collisions = collisions.collision_test(box.rect, collision_objects_box)
        box2.collisions = collisions.collision_test(box2.rect, collision_objects_box)

        game_display.blit(top.get_frame(top.width, top.height, 1), (top.x, top.y))

        for x in arr:
            game_display.blit(x.get_frame(x.width, x.height, 1), (x.x, x.y))

        for plat in platform_arr:
            game_display.blit(plat.get_frame(plat.width, plat.height, 1), (plat.x, plat.y))

        for plat in limitor_arr:
            game_display.blit(plat.get_frame(plat.width, plat.height, 1), (plat.x, plat.y))

        press_gravity.collision = collisions.collision_test(press_gravity.rect, [dog])
        press_gravity.update()
        keyboard.collision = collisions.collision_test(keyboard.rect, [dog])
        keyboard.update()
        spikes.collision = collisions.collision_test(spikes.rect, [dog])
        spikes.update()

        if spikes.flag:
            running = False
            flags.lvl3_dog_dead_flag.set_flag(True)

        game_display.blit(press_gravity.get_frame(40, 40, scale), (press_gravity.x, press_gravity.y))
        game_display.blit(keyboard.get_frame(40, 20, scale), (keyboard.x, keyboard.y))

        game_display.blit(dog.get_frame(40, 30, scale), (dog.position.x, dog.position.y))
        game_display.blit(box.get_frame(20, 20, scale), (box.position.x, box.position.y))
        game_display.blit(box2.get_frame(20, 20, scale), (box2.position.x, box2.position.y))

        dog.update(dt)
        box.update(dt)
        box2.update(dt)

        if keyboard.flag or press_gravity.flag:
            game_display.blit(text, text_box)

        pygame.display.update()
