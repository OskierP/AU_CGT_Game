import time

import pygame

import LEVEL_4.DisplayGame as DisplayGame
import LEVEL_4.collisions as collisions
import LEVEL_4.sprite as sprite
import flags as flags
from LEVEL_4.movable_objects import Player, Box


def run_level(run):
    ################################# LOAD UP A BASIC WINDOW AND CLOCK #################################
    pygame.init()
    display_width = 1100  # 1100
    display_height = 600  # 600

    running = run
    clock = pygame.time.Clock()


    mouse_position = pygame.math.Vector2(0, 0)

    font = pygame.font.Font('freesansbold.ttf', 22)
    text = font.render('Press B to press the button', True, (0, 0, 0))
    text_box = text.get_rect()
    ################################# LOAD PLAYER AND SPRITE SHEET###################################
    game_display = DisplayGame.GameDisplay(display_width, display_height).display_game()
    level_4_3_background = sprite.Sprite('LEVEL_4/assets/background/level4_3.png').load_image()

    ################################# MAIN LEDS ####################################
    red_led = sprite.ActionPlacePuzzle(347,141,159, 156, 'red')
    blue_led = sprite.ActionPlacePuzzle(541, 140, 159, 156, 'blue')
    green_led = sprite.ActionPlacePuzzle(349, 319, 159, 156, 'green')
    yellow_led= sprite.ActionPlacePuzzle(542, 316, 159, 156, 'yellow')
    non_led = sprite.ActionPlacePuzzle(0, 0, 0, 0, 'yellow')
    led_array = [red_led, blue_led, green_led,yellow_led]
    ################################# LEVEL LEDS #################################
    level_led_1= sprite.ActionPlacePuzzle(868,68,57, 72)
    level_led_2=sprite.ActionPlacePuzzle(942,68,57, 72)
    level_led_3=sprite.ActionPlacePuzzle(1015,68,57, 72)
    level_led_arr =[level_led_1,level_led_2,level_led_3]
    ################################# ERROR LEDS #################################
    error_led_1=sprite.ActionPlacePuzzle(17,81 ,52, 50)
    error_led_2=sprite.ActionPlacePuzzle(99,81 ,52, 50)
    error_led_3=sprite.ActionPlacePuzzle(182,81 ,52, 50)
    error_arr = [error_led_1, error_led_2, error_led_3]

    ################################# MOUSE #################################
    mouse = sprite.Mouse(15,15)

    ################################# ARRAYS #################################
    level_solutions=[[red_led, blue_led, green_led, non_led],
                     [yellow_led, red_led, green_led,blue_led,red_led, non_led],
                     [green_led,blue_led,red_led,yellow_led,blue_led,green_led,blue_led, non_led]]

    led_light_num = 1
    led_solution_num = 0
    led_flag = False
    player_clicks=[]
    ################################# VARIABLES #################################
    level = 0
    errors=0
    ################################# GAME LOOP ##########################
    flag = True
    clicks=0

    while running:

        mouse_position.x, mouse_position.y = pygame.mouse.get_pos()
        game_display.blit(level_4_3_background, (0, 0))

        ################################# CHECK PLAYER INPUT #################################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                flags.next_lvl_4_2.set_flag(True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    led_flag=True
                    player_clicks.clear()
                    clicks=0
                # if event.key == pygame.K_n:
                #     led_solution_num+=1
            if event.type == pygame.MOUSEBUTTONDOWN:
                for led in led_array:
                    if led.flag:
                        player_clicks.append(led)
                        clicks+=1


        if level == len(level_solutions):
            running = False
            flags.next_lvl_4_3.set_flag(True)

        if errors == 3:
            running = False



        ################################ UPDATE WINDOW AND DISPLAY #################################
        # pygame.draw.rect(game_display, rect=red_led, color='red')
        # pygame.draw.rect(game_display, rect=blue_led, color='blue')
        # pygame.draw.rect(game_display, rect=green_led, color='green')
        # pygame.draw.rect(game_display, rect=yellow_led, color='yellow')

        # for led in level_solutions[0]:
        #     pygame.display.update()
        #     led.update_rect()
        #     # print(led.get_fingerprint())
        #
        #
        #     pygame.draw.rect(game_display, rect=led.rect, color=led.get_fingerprint())
        #     led.width=0
        #     time.sleep(1)
        #     pygame.display.update()
        #     led.update_rect()
        #     pygame.draw.rect(game_display, rect=led.rect, color=led.get_fingerprint())
        #     led.width = 159
            # pygame.display.update()
        # print(len(level_solutions[0]))

        if led_flag:

            pygame.draw.rect(game_display, rect=level_solutions[led_solution_num][led_light_num-1],
                             color=level_solutions[led_solution_num][led_light_num-1].get_fingerprint())
            if led_light_num:
                time.sleep(1)

            if led_light_num == len(level_solutions[led_solution_num]):
                led_flag = False
                led_light_num=0
            else:

                led_light_num += 1
                print(led_light_num)


        # print(player_clicks)

        # for led in led_array:
        #     led.collision = collisions.collision_test(led.rect, [mouse])
        #
        # for led in led_array:
        #     if led.

        # pygame.draw.rect(game_display, rect=level_led_1, color='green')
        # pygame.draw.rect(game_display, rect=level_led_2, color='green')
        # pygame.draw.rect(game_display, rect=level_led_3, color='green')
        #
        # pygame.draw.rect(game_display, rect=error_led_1, color='red')
        # pygame.draw.rect(game_display, rect=error_led_2, color='red')
        # pygame.draw.rect(game_display, rect=error_led_3, color='red')
        #
        # pygame.draw.rect(game_display, rect=mouse.rect, color='black')

        for c in range(clicks):
            if not player_clicks[c].get_fingerprint() == level_solutions[led_solution_num][c].get_fingerprint():
                errors+=1
                clicks = 0
                player_clicks.clear()

        if clicks == len(level_solutions[led_solution_num])-1:
            level+=1
            clicks=0
            player_clicks.clear()
            led_solution_num+=1


        # for c in range(clicks):
        #     print(f'{c+1}: {player_clicks[c].get_fingerprint()} = {level_solutions[led_solution_num][c].get_fingerprint()}')

        for error_index in range(errors):
            # print(error_arr[error_index])
            # print(errors)
            pygame.draw.rect(game_display, rect=error_arr[error_index], color='red')
            # clicks=0

        for level_index in range(level):
            pygame.draw.rect(game_display, rect=level_led_arr[level_index], color='green')

        for led in led_array:
            led.collision = collisions.collision_test(led.rect, [mouse])

        for led in led_array:
            led.update()
        # print(mouse_position)
        mouse.update_rect()
        # if led_flag:
        #     time.sleep(2)
        pygame.display.update()