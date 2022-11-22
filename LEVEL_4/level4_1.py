import pygame

import DisplayGame
import collisions
import sprite
from movable_objects import Player, Box
import flags

next_level = False
dog_died = False


def run_level(run):
    ################################# LOAD UP A BASIC WINDOW AND CLOCK #################################
    pygame.init()
    display_width = 1100  # 1100
    display_height = 600  # 600

    running = run
    clock = pygame.time.Clock()
    tick = pygame.time.get_ticks()
    TARGET_FPS = 60
    delay_laser_odd = 0
    delay_laser_even = 0

    gravity = 0
    friction = 0

    font = pygame.font.Font('freesansbold.ttf', 22)
    text = font.render('Press B to press the button', True, (0, 0, 0))
    text_box = text.get_rect()
    ################################# LOAD PLAYER AND SPRITESHEET###################################
    game_display = DisplayGame.GameDisplay(display_width, display_height).displayGame()
    space_ship = sprite.Sprite('assets/background/spaceship.png').loadImage()
    dog = Player('assets/player/dog_anim_left.png', 5, gravity, friction)
    scale = 2.25

    box = Box('assets/movable_obj/box.png', gravity, friction)

    ################################# OBSTICALES ####################################
    celing = sprite.Obsticales(1100, 20, 0, 0)
    obj11 = sprite.Platfrom(0, 200, 100)
    obj12 = sprite.Platfrom(250, 200, 1100)
    obj21 = sprite.Platfrom(0, 400, 500)
    obj22 = sprite.Platfrom(650, 400, 500)
    floor = sprite.Obsticales(1200, 20, 0, 570)

    obj_list = [obj11, obj12, obj21, obj22]

    wall_left = sprite.Obsticales(20, 900, 1090, 0)
    wall_right = sprite.Obsticales(10, 900, 0, 0)

    laser1_1 = sprite.Laser(0, 200, 800, 0)
    laser2_1 = sprite.Laser(0, 200, 650, 0)
    laser3_1 = sprite.Laser(0, 200, 500, 0)
    laser4_1 = sprite.Laser(0, 200, 350, 0)
    laser1_2 = sprite.Laser(0, 180, 800, 220)
    laser2_2 = sprite.Laser(0, 180, 650, 220)
    laser3_2 = sprite.Laser(0, 180, 490, 220)
    laser4_2 = sprite.Laser(0, 180, 350, 220)
    laser1_3 = sprite.Laser(0, 180, 350, 420)
    laser_0 = sprite.Laser(0, 0, 0, 0)
    laser2_3 = sprite.Laser(0, 180, 700, 420)

    laser_list = [laser1_1, laser2_1, laser3_1, laser4_1, laser1_2, laser2_2, laser3_2, laser4_2, laser1_3, laser_0,
                  laser2_3]

    insert_box = sprite.ActionPlace('assets/action_place/insertBox.png', 1010, 480, 40, 40)
    player_press = sprite.ActionPlace('assets/action_place/button.png', 1010, 300, 40, 40)

    doors = sprite.Door(0, 220)
    doors_action = sprite.ActionPlace_2(20, 180, 0, 220)

    ##PLATES##

    bridge_plate = sprite.InfoPlate('assets/unmovable_obj/bridge.png', 950, 100, 50, 20)
    lvl2 = sprite.InfoPlate('assets/unmovable_obj/lvl2.png', 100, 300, 50, 20)
    ########## COLLISIONS ##################
    collision_objects_player = [floor, wall_right, wall_left, box, celing, obj11, obj12, obj21, obj22, doors]
    collision_objects_box = [floor, box, wall_right, wall_left, obj11, obj12, obj21, obj22]
    collision_with_lasers = [box, dog]

    collision_interactive = [box, dog]
    #################################### LOAD THE LEVEL #######################################
    dog.position.x, dog.position.y = 900, 100

    box.position.x, box.position.y = 200, 500
    box.width, box.height = 20, 20

    ################################# GAME LOOP ##########################
    flag = True

    while running:
        dt = clock.tick(60) * .001 * TARGET_FPS
        game_display.blit(space_ship, (0, 0))
        dog.frame = 2

        ################################# CHECK PLAYER INPUT #################################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                flags.next_lvl_1.set_flag(True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dog.LEFT_KEY = True
                elif event.key == pygame.K_RIGHT:
                    dog.RIGHT_KEY = True
                elif event.key == pygame.K_SPACE:
                    dog.jump()
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

                elif event.key == pygame.K_b and player_press.flag and insert_box.flag:
                    doors.width = 0
                    doors.update_rect()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    dog.LEFT_KEY = False
                    dog.frame = 0
                elif event.key == pygame.K_RIGHT:
                    dog.RIGHT_KEY = False
                    dog.frame = 0
                elif event.key == pygame.K_SPACE:
                    if dog.is_jumping:
                        dog.velocity.y *= .25
                        dog.is_jumping = False

        ################################# UPDATE WINDOW AND DISPLAY #################################

        delay_laser_odd = laser1_1.on_off_odd_master(delay_laser_odd)
        delay_laser_even = laser2_1.on_off_even_master(delay_laser_even)

        for laser in laser_list[2:]:
            if laser_list.index(laser) % 2:
                laser.on_off_even_slave(delay_laser_even)
            else:
                laser.on_off_odd_slave(delay_laser_odd)

        for laser in laser_list:
            laser.update_rect()

        for obj in obj_list:
            game_display.blit(obj.getFrame(obj.width, obj.height, 1), (obj.x, obj.y))

        dog.collisions = collisions.collision_test(dog.rect, collision_objects_player)
        dog.collision_with_box = collisions.collision_test(dog.rect, [box])
        box.collisions = collisions.collision_test(box.rect, collision_objects_box)

        for laser in laser_list:
            laser.collison = collisions.collision_test(laser.rect, collision_with_lasers)

        insert_box.collision = collisions.collision_test(insert_box.rect, collision_interactive)
        player_press.collision = collisions.collision_test(player_press.rect, [dog])
        player_press.update_action_place()
        doors_action.collison = collisions.collision_test(doors_action.rect, [dog])
        doors_action.update_action()

        if doors_action.flag:
            running = False
            flags.next_lvl_1.set_flag(True)

        game_display.blit(insert_box.getFrame(40, 40, scale), (insert_box.x, insert_box.y))
        game_display.blit(player_press.getFrame(40, 40, scale), (player_press.x, player_press.y))
        game_display.blit(doors.getFrame(doors.width, doors.height, 1), (doors.x, doors.y))

        for laser in laser_list:
            pygame.draw.rect(game_display, (0, 240, 0), laser)

        game_display.blit(lvl2.getFrame(lvl2.width, lvl2.height, 1), (lvl2.x, lvl2.y))
        game_display.blit(bridge_plate.getFrame(bridge_plate.width, bridge_plate.height, 1),
                          (bridge_plate.x, bridge_plate.y))

        game_display.blit(dog.getFrame(40, 30, scale), (dog.position.x, dog.position.y))
        game_display.blit(box.getFrame(20, 20, scale), (box.position.x, box.position.y))

        if player_press.flag:
            game_display.blit(text, text_box)

        dog.update(dt)
        box.update(dt)

        insert_box.update_action_place()

        for laser in laser_list:
            if laser.update_laser() == 1:
                running = False
                flags.dog_dead_flag.set_flag(True)

        pygame.display.update()
