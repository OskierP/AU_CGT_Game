import time

import pygame

import LEVEL_3n4.collisions as collisions
import LEVEL_3n4.display_game as display_game
import LEVEL_3n4.sprite as sprite
import flags as flags
import progress.save_progress
from LEVEL_3n4.movable_objects import Player, Box


def run_level(run):
    ################################# LOAD UP A BASIC WINDOW AND CLOCK #################################
    pygame.init()
    display_width = 1100  # 1100
    display_height = 600  # 600

    pygame.mixer.init()
    pygame.mixer.music.load('LEVEL_3n4/assets/sound/deep_space_music.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    button_click = pygame.mixer.Sound('LEVEL_3n4/assets/sound/button_click_effect.wav')

    running = run
    clock = pygame.time.Clock()
    target_fps = 60
    delay_laser_odd = 0
    delay_laser_even = 0

    gravity = 0
    friction = 0

    font = pygame.font.SysFont('arial', 22)
        # Font('freesansbold.ttf', 22)
    text = font.render('Press SPACEBAR to press the button', True, (255, 255, 255))
    text_box = text.get_rect()
    text_box.center = (display_width // 2, display_height // 2)

    ################################# LOAD PLAYER AND SPRITE SHEET###################################
    game_display = display_game.GameDisplay(display_width, display_height).display_game()
    level_4_1_background = sprite.Sprite('LEVEL_3n4/assets/sprites/background/level4_1.png').load_image()
    dog = Player('LEVEL_3n4/assets/sprites/player/dog_anim_left.png', 5, gravity, friction)
    scale = 2.25

    box = Box('LEVEL_3n4/assets/sprites/movable_obj/box.png', gravity, friction)

    ################################# OBSTACLES ####################################
    ceiling = sprite.Obstacles(1100, 20, 0, 0)
    obj11 = sprite.Platform(0, 200, 100)
    obj12 = sprite.Platform(250, 200, 1100)
    obj21 = sprite.Platform(0, 400, 500)
    obj22 = sprite.Platform(650, 400, 500)
    floor = sprite.Obstacles(1200, 20, 0, 570)

    obj_list = [obj11, obj12, obj21, obj22]

    wall_left = sprite.Obstacles(20, 900, 1090, 0)
    wall_right = sprite.Obstacles(10, 900, 0, 0)

    laser1_1 = sprite.Laser(0, 200, 800, 0)
    laser2_1 = sprite.Laser(0, 200, 650, 0)
    laser3_1 = sprite.Laser(0, 200, 500, 0)
    laser4_1 = sprite.Laser(0, 200, 350, 0)
    laser1_2 = sprite.Laser(0, 180, 800, 220)
    laser2_2 = sprite.Laser(0, 180, 490, 220)
    laser3_2 = sprite.Laser(0, 180, 350, 220)
    laser1_3 = sprite.Laser(0, 180, 350, 420)
    laser_0 = sprite.Laser(0, 0, 0, 0)
    laser2_3 = sprite.Laser(0, 180, 700, 420)

    laser_list = [laser1_1, laser2_1, laser3_1, laser4_1, laser1_2, laser_0, laser2_2, laser3_2, laser1_3, laser_0,
                  laser2_3]

    laser1_1_indi = sprite.Laser(0, 200, 800, 0)
    laser2_1_indi = sprite.Laser(0, 200, 650, 0)
    laser3_1_indi = sprite.Laser(0, 200, 500, 0)
    laser4_1_indi = sprite.Laser(0, 200, 350, 0)
    laser1_2_indi = sprite.Laser(0, 180, 800, 220)
    laser2_2_indi = sprite.Laser(0, 180, 490, 220)
    laser3_2_indi = sprite.Laser(0, 180, 350, 220)
    laser1_3_indi = sprite.Laser(0, 180, 350, 420)
    laser2_3_indi = sprite.Laser(0, 180, 700, 420)

    laser_indi_list = [laser1_1_indi, laser2_1_indi, laser3_1_indi, laser4_1_indi, laser1_2_indi, laser_0,
                       laser2_2_indi, laser3_2_indi, laser1_3_indi, laser_0,
                       laser2_3_indi]

    insert_box = sprite.ActionPlace('LEVEL_3n4/assets/sprites/action_place/insertBox.png', 1010, 480, 40, 40)
    player_press = sprite.ActionPlace('LEVEL_3n4/assets/sprites/action_place/button.png', 1010, 300, 40, 40)
    player_press_2 = sprite.ActionPlace('LEVEL_3n4/assets/sprites/action_place/button-left.png', 0, 470, 40, 40)

    doors = sprite.Door(0, 220)
    doors_action = sprite.ActionPlace_2(20, 180, 0, 220)

    ##PLATES##

    bridge_plate = sprite.InfoPlate('LEVEL_3n4/assets/sprites/unmovable_obj/bridge.png', 950, 100, 50, 20)
    lvl2 = sprite.InfoPlate('LEVEL_3n4/assets/sprites/unmovable_obj/lvl2.png', 100, 300, 50, 20)
    ########## COLLISIONS ##################
    collision_objects_player = [floor, wall_right, wall_left, box, ceiling, obj11, obj12, obj21, obj22, doors]
    collision_objects_box = [floor, box, wall_right, wall_left, obj11, obj12, obj21, obj22]
    collision_with_lasers = [box, dog]

    collision_interactive = [box, dog]
    #################################### LOAD THE LEVEL #######################################
    dog.position.x, dog.position.y = 900, 100

    box.position.x, box.position.y = 2000, 2000
    box.width, box.height = 20, 20

    button2_pressed_once = False
    ################################# GAME LOOP ##########################
    while running:
        dt = clock.tick(60) * .001 * target_fps
        game_display.blit(level_4_1_background, (0, 0))
        dog.frame = 10

        ################################# CHECK PLAYER INPUT #################################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                flags.next_lvl_3_1.set_flag(True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dog.LEFT_KEY = True
                elif event.key == pygame.K_RIGHT:
                    dog.RIGHT_KEY = True
                elif event.key == pygame.K_DOWN and not gravity and not friction:
                    dog.acceleration.y += .5
                elif event.key == pygame.K_UP and not gravity and not friction:
                    dog.acceleration.y -= .5
                # elif event.key == pygame.K_j:
                #     if flag:
                #         gravity = 0.3
                #         friction = -.12
                #         flag = False
                #     else:
                #         gravity = 0
                #         friction = 0
                #         flag = True
                #     dog.gravity = gravity
                #     dog.friction = friction
                #     box.gravity = gravity
                #     box.friction = friction

                elif event.key == pygame.K_SPACE and player_press.flag and insert_box.flag:
                    button_click.play()
                    button_click.set_volume(0.5)
                    time.sleep(1)
                    doors.width = 0
                    doors.update_rect()
                elif event.key == pygame.K_SPACE and player_press_2.flag:
                    button_click.play()
                    button_click.set_volume(0.5)
                    time.sleep(1)
                    player_press_2.was_pressed = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    dog.LEFT_KEY = False
                    dog.frame = 0
                elif event.key == pygame.K_RIGHT:
                    dog.RIGHT_KEY = False
                    dog.frame = 0

        ################################# UPDATE WINDOW AND DISPLAY #################################

        delay_laser_odd = laser1_1.on_off_odd_master(delay_laser_odd)
        delay_laser_even = laser2_1.on_off_even_master(delay_laser_even)

        for laser in laser_list[2:]:
            if player_press_2.was_pressed:
                laser.width = 0
                laser2_1.width = 0
                laser1_1.width = 0
            else:
                if laser_list.index(laser) % 2:
                    laser.on_off_even_slave(delay_laser_even)
                else:
                    laser.on_off_odd_slave(delay_laser_odd)
        if not player_press_2.was_pressed:
            laser1_2.sound_fx = 0

        for laser in laser_indi_list:
            if player_press_2.was_pressed:
                laser.width = 0
            else:
                if laser_indi_list.index(laser) % 2:
                    laser.on_off_even_slave_indi(delay_laser_even)
                else:
                    laser.on_off_odd_slave_indi(delay_laser_odd)
        if not player_press_2.was_pressed:
            laser1_2_indi.sound_fx = 0

        for laser in laser_indi_list:
            laser.update_rect()

        for laser in laser_list:
            laser.update_rect()

        for obj in obj_list:
            game_display.blit(obj.get_frame(obj.width, obj.height, 1), (obj.x, obj.y))

        dog.collisions = collisions.collision_test(dog.rect, collision_objects_player)
        dog.collision_with_box = collisions.collision_test(dog.rect, [box])
        box.collisions = collisions.collision_test(box.rect, collision_objects_box)

        for laser in laser_list:
            laser.collision = collisions.collision_test(laser.rect, collision_with_lasers)

        insert_box.collision = collisions.collision_test(insert_box.rect, collision_interactive)
        player_press.collision = collisions.collision_test(player_press.rect, [dog])
        player_press.update()
        player_press_2.collision = collisions.collision_test(player_press_2.rect, [dog])
        player_press_2.update()
        doors_action.collision = collisions.collision_test(doors_action.rect, [dog])
        doors_action.update()

        if doors_action.flag:
            running = False
            progress.save_progress.update_progress('Level_3_2', True)
            flags.next_lvl_3_1.set_flag(True)

        game_display.blit(insert_box.get_frame(40, 40, scale), (insert_box.x, insert_box.y))
        game_display.blit(player_press.get_frame(40, 40, scale), (player_press.x, player_press.y))
        game_display.blit(player_press_2.get_frame(40, 40, scale), (player_press_2.x, player_press_2.y))
        game_display.blit(doors.get_frame(doors.width, doors.height, 1), (doors.x, doors.y))

        for laser in laser_indi_list:
            pygame.draw.rect(game_display, (152, 251, 152), laser)

        for laser in laser_list:
            pygame.draw.rect(game_display, (240, 0, 50), laser)

        game_display.blit(lvl2.get_frame(lvl2.width, lvl2.height, 1), (lvl2.x, lvl2.y))
        game_display.blit(bridge_plate.get_frame(bridge_plate.width, bridge_plate.height, 1),
                          (bridge_plate.x, bridge_plate.y))

        game_display.blit(dog.get_frame(40, 30, scale), (dog.position.x, dog.position.y))
        game_display.blit(box.get_frame(20, 20, scale), (box.position.x, box.position.y))

        if player_press_2.was_pressed and player_press_2.flag and not button2_pressed_once:
            box.position.x, box.position.y = 200, 500
            button2_pressed_once = True

        if player_press.flag or player_press_2.flag:
            game_display.blit(text, text_box)

        dog.update(dt)
        box.update(dt)

        insert_box.update()

        for laser in laser_list:
            laser.update_laser()
            if laser.update_laser() == 1:
                running = False
                flags.lvl3_dog_dead_flag.set_flag(True)

        pygame.display.update()
