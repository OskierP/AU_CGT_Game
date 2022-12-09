import time

import pygame

import LEVEL_3n4.DisplayGame as DisplayGame
import LEVEL_3n4.collisions as collisions
import LEVEL_3n4.sprite as sprite
import flags as flags


def run_level(run):
    ################################# LOAD UP A BASIC WINDOW AND CLOCK #################################
    pygame.init()
    display_width = 1100  # 1100
    display_height = 600  # 600

    pygame.mixer.init()

    running = run

    mouse_position = pygame.math.Vector2(0, 0)

    font = pygame.font.Font('freesansbold.ttf', 22)
    text = font.render('SPACE BAR:', True, (78, 150, 6))
    text_box = text.get_rect()
    text2 = font.render('show sequence', True, (78, 150, 6))
    text2_box = text2.get_rect()
    text3 = font.render('and restart clicks', True, (78, 150, 6))
    text3_box = text2.get_rect()

    text_box.x, text_box.y = 870, 220
    text2_box.x, text2_box.y = 870, 250
    text3_box.x, text3_box.y = 870, 280
    ################################# LOAD PLAYER AND SPRITE SHEET###################################
    game_display = DisplayGame.GameDisplay(display_width, display_height).display_game()
    level_4_3_background = sprite.Sprite('LEVEL_3n4/assets/sprites/background/level4_3.png').load_image()

    ################################# MAIN LEDS ####################################
    red_led = sprite.ActionPlacePuzzle(347, 141, 159, 156, 'red')
    blue_led = sprite.ActionPlacePuzzle(541, 140, 159, 156, 'blue')
    green_led = sprite.ActionPlacePuzzle(349, 319, 159, 156, 'green')
    yellow_led = sprite.ActionPlacePuzzle(542, 316, 159, 156, 'yellow')
    non_led = sprite.ActionPlacePuzzle(0, 0, 0, 0, 'yellow')
    led_array = [red_led, blue_led, green_led, yellow_led]
    ################################# LEVEL LEDS #################################
    level_led_1 = sprite.ActionPlacePuzzle(868, 68, 57, 72)
    level_led_2 = sprite.ActionPlacePuzzle(942, 68, 57, 72)
    level_led_3 = sprite.ActionPlacePuzzle(1015, 68, 57, 72)
    level_led_arr = [level_led_1, level_led_2, level_led_3]
    ################################# ERROR LEDS #################################
    error_led_1 = sprite.ActionPlacePuzzle(17, 81, 52, 50)
    error_led_2 = sprite.ActionPlacePuzzle(99, 81, 52, 50)
    error_led_3 = sprite.ActionPlacePuzzle(182, 81, 52, 50)
    error_arr = [error_led_1, error_led_2, error_led_3]

    ################################# MOUSE #################################
    mouse = sprite.Mouse(15, 15)

    ################################# ARRAYS #################################
    level_solutions = [[red_led, blue_led, green_led, non_led],
                       [yellow_led, red_led, green_led, blue_led, red_led, non_led],
                       [green_led, blue_led, red_led, yellow_led, blue_led, green_led, blue_led, non_led]]

    ################################# VARIABLES #################################
    level = 0
    errors = 0
    clicks = 0
    led_light_num = 1
    led_solution_num = 0
    led_flag = False
    player_clicks = []
    ################################# GAME LOOP ##########################

    while running:

        mouse_position.x, mouse_position.y = pygame.mouse.get_pos()
        game_display.blit(level_4_3_background, (0, 0))

        ################################# CHECK PLAYER INPUT #################################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                flags.next_lvl_4.set_flag(True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Sound('LEVEL_3n4/assets/sound/click_sound_effect.mp3').play()
                    led_flag = True
                    player_clicks.clear()
                    clicks = 0
                # if event.key == pygame.K_n:
                #     led_solution_num+=1
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound('LEVEL_3n4/assets/sound/click_sound_effect.mp3').play()
                for led in led_array:
                    if led.flag:
                        player_clicks.append(led)
                        clicks += 1

        if level == len(level_solutions):
            time.sleep(2)
            running = False
            flags.next_lvl_4.set_flag(True)

        if errors == 3:
            running = False
            flags.lvl3_dog_dead_flag.set_flag(True)

        game_display.blit(text, text_box)
        game_display.blit(text2, text2_box)
        game_display.blit(text3, text3_box)

        ################################ UPDATE WINDOW AND DISPLAY #################################

        if led_flag:

            pygame.draw.rect(game_display, rect=level_solutions[led_solution_num][led_light_num - 1],
                             color=level_solutions[led_solution_num][led_light_num - 1].get_fingerprint())
            if led_light_num:
                time.sleep(1)

            if led_light_num == len(level_solutions[led_solution_num]):
                led_flag = False
                led_light_num = 0
            else:

                led_light_num += 1
                print(led_light_num)

        for error_index in range(errors):
            pygame.draw.rect(game_display, rect=error_arr[error_index], color='red')

        for c in range(clicks):
            if not player_clicks[c] == level_solutions[led_solution_num][c]:
                errors += 1
                clicks = 0
                player_clicks.clear()

        if clicks == len(level_solutions[led_solution_num]) - 1:
            pygame.mixer.Sound('LEVEL_3n4/assets/sound/success_effect.wav').play()
            level += 1
            clicks = 0
            player_clicks.clear()
            if level < 3:
                led_solution_num += 1

        for error_index in range(errors):
            pygame.draw.rect(game_display, rect=error_arr[error_index], color='red')

        for level_index in range(level):
            pygame.draw.rect(game_display, rect=level_led_arr[level_index], color='green')

        for led in led_array:
            led.collision = collisions.collision_test(led.rect, [mouse])
            led.update()
            if led.flag:
                pygame.draw.rect(game_display, rect=led, color=led.get_fingerprint())

        mouse.update_rect()
        if led_flag:
            mouse.stop_rect()
        pygame.display.update()
