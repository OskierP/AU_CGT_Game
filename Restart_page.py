
import pygame

import DisplayGame
import sprite


def restart():
    pygame.init()

    running = True

    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)
    black =(0,0,0)

    X = 1100
    Y = 600

    display_surface = pygame.display.set_mode((X, Y))

    pygame.display.set_caption('Show Text')

    font = pygame.font.Font('freesansbold.ttf', 32)

    text = font.render('X has died :,-(', True, white, black)
    text2 = font.render('Press R to restart level', True, white, black)

    textRect = text.get_rect()
    textRect2 = text2.get_rect()

    textRect.center = (X // 2, Y // 2 -100)
    textRect2.center = (X // 2, Y // 2 -50)

    while running:

        display_surface.fill(black)

        display_surface.blit(text, textRect)
        display_surface.blit(text2, textRect2)

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    running = False

            if event.type == pygame.QUIT:
                pygame.quit()

                quit()

            pygame.display.update()


