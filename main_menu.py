import pygame

import flags
import progress.save_progress
from LEVEL_3n4 import sprite, collisions
from flags import menu_flag


def menu():
    pygame.init()
    pygame.mixer.stop()

    running = True

    white = (255, 255, 255)
    black = (0, 0, 0)

    x = 1100
    y = 600

    display_surface = pygame.display.set_mode((x, y))

    # https://www.pixilart.com/art/mars-ac45cfbf1eb0827
    menu_background = sprite.Sprite('menu_assets/menu.png').load_image()

    pygame.display.set_caption('Show Text')

    # https://www.fontspace.com/n%C3%A9o-party-font-f25303
    title = sprite.Sprite(f'menu_assets/title.png').load_image()

    start_button = sprite.MainMenu('menu_assets/start_btn.png', 250, 350, 261, 99)
    exit_button = sprite.MainMenu('menu_assets/exit_btn.png', 600, 350, 222, 99)

    mouse = sprite.Mouse(15, 15)
    mouse_position = pygame.math.Vector2(0, 0)

    while running:
        mouse_position.x, mouse_position.y = pygame.mouse.get_pos()
        display_surface.blit(menu_background, (0, 0))
        display_surface.blit(title, (100, y // 2 - 100))

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.flag:
                    flags.menu_flag.set_flag(True)
                    running = False
                if exit_button.flag:
                    running = False
                    pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    running = False

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        start_button.collision = collisions.collision_test(start_button.rect, [mouse])
        exit_button.collision = collisions.collision_test(exit_button.rect, [mouse])
        display_surface.blit(start_button.get_frame(start_button.width, start_button.height, 1),
                             (start_button.x, start_button.y))
        display_surface.blit(exit_button.get_frame(exit_button.width, exit_button.height, 1),
                             (exit_button.x, exit_button.y))

        # pygame.draw.rect(display_surface, (255, 0, 0), mouse)

        mouse.update_rect()
        start_button.update()
        exit_button.update()

        pygame.display.update()


def splash_screen(path: str):
    pygame.init()
    pygame.mixer.stop()

    running = True

    white = (255, 255, 255)
    black = (0, 0, 0)

    x = 1100
    y = 600

    display_surface = pygame.display.set_mode((x, y))
    background = sprite.Sprite(f'story/{path}.png').load_image()

    pygame.display.set_caption('Show Text')

    font = pygame.font.Font('freesansbold.ttf', 32)

    text = font.render('Press any key', True, white)
    text2 = font.render('to continue', True, white)

    text_rect = text.get_rect()
    text_rect2 = text2.get_rect()

    text_rect.center = (x // 2, y // 2 + 120)
    text_rect2.center = (x // 2, y // 2 + 170)

    flag = False
    if path == 'main_story':
        flag = True

    while running:

        display_surface.blit(background, (0, 0))

        if not flag:
            display_surface.blit(text, text_rect)
            display_surface.blit(text2, text_rect2)

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_SPACE:
                running = False

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()


def choose_level():
    pygame.init()
    pygame.mixer.stop()

    running = True

    white = (255, 255, 255)
    black = (0, 0, 0)

    x = 1100
    y = 600

    level1 = sprite.MainMenu('menu_assets/levels/unlocked/Level1.png', 300, 100, 240, 90)
    level2 = sprite.MainMenu('menu_assets/levels/locked/Level2.png', 600, 100, 235, 90)
    level3_1 = sprite.MainMenu('menu_assets/levels/locked/Level3_1.png', 300, 250, 240, 95)
    level3_2 = sprite.MainMenu('menu_assets/levels/locked/Level3_2.png', 600, 250, 240, 95)
    level4 = sprite.MainMenu('menu_assets/levels/locked/Level4.png', 300, 400, 240, 95)
    level5 = sprite.MainMenu('menu_assets/levels/locked/Level5.png', 600, 400, 240, 90)
    exit_button_lvl = sprite.MainMenu('menu_assets/exit_btn.png', 0, 0, 222, 99)

    level_list = [level1, level2, level3_1, level3_2, level4, level5, exit_button_lvl]
    image_list = ['Level1.png', 'Level2.png', 'Level3_1.png', 'Level3_2.png', 'Level4.png', 'Level5.png']

    level_progress = progress.save_progress.read_2_array()
    level_progress.append('nan')

    for level_num in range(6):
        if level_progress[level_num]:
            level_list[level_num].image = f'menu_assets/levels/unlocked/{image_list[level_num]}'

    display_surface = pygame.display.set_mode((x, y))
    # https://www.pixilart.com/art/mars-ac45cfbf1eb0827
    menu_backgound = sprite.Sprite('menu_assets/menu.png').load_image()

    mouse = sprite.Mouse(15, 15)
    mouse_position = pygame.math.Vector2(0, 0)

    while running:
        mouse_position.x, mouse_position.y = pygame.mouse.get_pos()
        display_surface.blit(menu_backgound, (0, 0))

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if level1.flag:
                    running = False
                    return 1
                elif level2.flag:
                    running = False
                    return 2
                elif level3_1.flag:
                    running = False
                    return "3_1"
                elif level3_2.flag:
                    running = False
                    return "3_2"
                elif level4.flag:
                    running = False
                    return 4
                elif level5.flag:
                    running = False
                    return 5
                elif exit_button_lvl.flag:
                    menu_flag.set_flag(False)
                    running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    running = False

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        for level in level_list:
            if level_progress[level_list.index(level)]:
                level.collision = collisions.collision_test(level.rect, [mouse])
        for level in level_list:
            display_surface.blit(level.get_frame(level.width, level.height, 1), (level.x, level.y))

        # pygame.draw.rect(display_surface, (255, 0, 0), mouse)

        mouse.update_rect()
        for level in level_list:
            level.update()

        pygame.display.update()