import pygame

import LEVEL_4.DisplayGame as DisplayGame
import LEVEL_4.collisions as collisions
import LEVEL_4.sprite as sprite
from LEVEL_4.movable_objects import Player, Box
import flags as flags

next_level = False

def run_level(run):
    ################################# LOAD UP A BASIC WINDOW AND CLOCK #################################
    pygame.init()
    display_width = 1100  # 1100
    display_height = 600  # 600
    was_pressed = False

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
    space_ship = sprite.Sprite('LEVEL_4/assets/background/lvl42.png').loadImage()

    dog = Player('LEVEL_4/assets/player/dog_anim_left.png', 5, gravity, friction)
    scale = 2.25

    box = Box('LEVEL_4/assets/movable_obj/box.png', gravity, friction)
    box2 = Box('LEVEL_4/assets/movable_obj/box.png', gravity, friction)

    move_arr = [dog, box, box2]

    ################################# OBSTICALES ####################################
    ceiling = sprite.Obsticales(1100, 20, 0, 0)

    floor = sprite.Obsticales(1200, 20, 0, 570)  # spikes

    top = sprite.Platfrom(990, 50, 150)
    arr = []
    for i in range(10):
        arr.append(sprite.Platfrom(980, 50 + 20 * i, 20))
    arrWall = sprite.Obsticales(20, 100, 980, 50)

    wall_right = sprite.Obsticales(20, 900, 1090, 0)
    wall_left = sprite.Obsticales(10, 900, 30, 0)

    platform = sprite.Platfrom(0, 230, 340)
    platform1 = sprite.Platfrom(850, 450, 300)
    platform2 = sprite.Platfrom(450, 350, 300)

    limitor1_1 = sprite.Platfrom(830, 430, 20)
    limitor2_1 = sprite.Platfrom(450, 340, 20)
    limitor2_2 = sprite.Platfrom(730, 340, 20)
    limitor3_1 = sprite.Platfrom(320, 210, 20)

    platformArr = [platform, platform1, platform2]
    limitorArr = [limitor1_1, limitor2_1, limitor2_2, limitor3_1]

    ##BUTTONS##

    press_gravity = sprite.ActionPlace('LEVEL_4/assets/action_place/button.png', 1010, 100, 40, 40)
    keyboard = sprite.ActionPlace('LEVEL_4/assets/action_place/keyboard.png', 50, 150, 40, 40)
    spikes = sprite.ActionPlace_2(1200, 20, 0, 550)

    ########## COLLISIONS ##################

    collision_objects_player = [spikes, floor, wall_right, wall_left, box, box2, ceiling, platform, platform1,
                                platform2, limitor1_1, limitor2_1, limitor2_2, limitor3_1, top, arrWall]

    collision_objects_box = [floor, wall_right, wall_left, platform1, platform2, limitor1_1, limitor2_1, limitor2_2]
    collision_interactive = [dog]
    #################################### LOAD THE LEVEL #######################################
    dog.position.x, dog.position.y = 1000, 100

    box.position.x, box.position.y = 600, 200
    box.width, box.height = 20, 20

    box2.position.x, box2.position.y = 900, 200
    box2.width, box2.height = 20, 20

    ################################# GAME LOOP ##########################
    flag = True

    while running:
        dt = clock.tick(60) * .001 * TARGET_FPS
        game_display.blit(space_ship, (0, 0))

        ################################# CHECK PLAYER INPUT #################################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                flags.next_lvl_4_2.set_flag(True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dog.LEFT_KEY = True
                elif event.key == pygame.K_RIGHT:
                    dog.RIGHT_KEY = True
                elif event.key == pygame.K_SPACE:
                    dog.jump()
                # elif event.key == pygame.K_DOWN and not gravity and not friction:
                #     dog.acceleration.y += .5
                elif event.key == pygame.K_UP and not gravity and not friction:
                    dog.acceleration.y -= .5
                elif event.key == pygame.K_j:  # to delete
                    if flag:
                        gravity = 0.21
                        friction = -.12
                        flag = False
                        # was_pressed = True to change
                    else:
                        gravity = 0
                        friction = 0
                        flag = True
                    for obj in move_arr:
                        obj.gravity = gravity
                        obj.friction = friction

                elif event.key == pygame.K_b and press_gravity.flag and not was_pressed:
                    gravity = 0.21
                    friction = -.12
                    was_pressed = True
                    for obj in move_arr:
                        obj.gravity = gravity
                        obj.friction = friction
                elif event.key == pygame.K_b and keyboard.flag:
                    running = False
                    flags.next_lvl_4_2.set_flag(True)

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

        dog.collisions = collisions.collision_test(dog.rect, collision_objects_player)
        dog.collision_with_box = collisions.collision_test(dog.rect, [box, box2])
        box.collisions = collisions.collision_test(box.rect, collision_objects_box)
        box2.collisions = collisions.collision_test(box2.rect, collision_objects_box)

        game_display.blit(top.getFrame(top.width, top.height, 1), (top.x, top.y))

        for x in arr:
            game_display.blit(x.getFrame(x.width, x.height, 1), (x.x, x.y))

        for plat in platformArr:
            game_display.blit(plat.getFrame(plat.width, plat.height, 1), (plat.x, plat.y))

        for plat in limitorArr:
            game_display.blit(plat.getFrame(plat.width, plat.height, 1), (plat.x, plat.y))

        press_gravity.collision = collisions.collision_test(press_gravity.rect, [dog])
        press_gravity.update_action_place()
        keyboard.collision = collisions.collision_test(keyboard.rect, [dog])
        keyboard.update_action_place()
        spikes.collison = collisions.collision_test(spikes.rect, [dog])
        spikes.update_action()

        if spikes.flag:
            running = False
            flags.lvl4_dog_dead_flag.set_flag(True)

        game_display.blit(press_gravity.getFrame(40, 40, scale), (press_gravity.x, press_gravity.y))
        game_display.blit(keyboard.getFrame(40, 20, scale), (keyboard.x, keyboard.y))

        game_display.blit(dog.getFrame(40, 30, scale), (dog.position.x, dog.position.y))
        game_display.blit(box.getFrame(20, 20, scale), (box.position.x, box.position.y))
        game_display.blit(box2.getFrame(20, 20, scale), (box2.position.x, box2.position.y))

        dog.update(dt)
        box.update(dt)
        box2.update(dt)

        if keyboard.flag or press_gravity.flag:
            game_display.blit(text, text_box)

        pygame.display.update()
