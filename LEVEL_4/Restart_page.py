import pygame


def restart():
    pygame.init()
    pygame.mixer.stop()

    running = True

    white = (255, 255, 255)
    black = (0, 0, 0)

    x = 1100
    y = 600

    display_surface = pygame.display.set_mode((x, y))

    pygame.display.set_caption('Show Text')

    font = pygame.font.Font('freesansbold.ttf', 32)

    text = font.render('X has died :,-(', True, white, black)
    text2 = font.render('Press R to restart level', True, white, black)

    text_rect = text.get_rect()
    text_rect2 = text2.get_rect()

    text_rect.center = (x // 2, y // 2 - 100)
    text_rect2.center = (x // 2, y // 2 - 50)

    while running:

        display_surface.fill(black)

        display_surface.blit(text, text_rect)
        display_surface.blit(text2, text_rect2)

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    running = False

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            pygame.display.update()


def restart_lvl_3():
    pygame.init()
    pygame.mixer.stop()

    running = True

    white = (255, 255, 255)
    black = (0, 0, 0)

    x = 1100
    y = 600

    display_surface = pygame.display.set_mode((x, y))

    pygame.display.set_caption('Show Text')

    font = pygame.font.Font('freesansbold.ttf', 32)

    text = font.render('Oh no, ship has blown up!', True, white, black)
    text2 = font.render('Press R to restart level', True, white, black)

    text_rect = text.get_rect()
    text_rect2 = text2.get_rect()

    text_rect.center = (x // 2, y // 2 - 100)
    text_rect2.center = (x // 2, y // 2 - 50)

    while running:

        display_surface.fill(black)

        display_surface.blit(text, text_rect)
        display_surface.blit(text2, text_rect2)

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    running = False

            if event.type == pygame.QUIT:
                pygame.quit()

                quit()

            pygame.display.update()
