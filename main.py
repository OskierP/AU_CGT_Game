import time

import pygame

import sprite

import DisplayGame

pygame.init()

display_width = 800
display_height = 600

# gameDisplay = pygame.display.set_mode((display_width, display_height))
gameDisplay = DisplayGame.GameDisplay(display_width, display_height).displayGame()

# black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()
crashed = False
rect = pygame.Rect(130, 500, 200, 50)
alien1 = pygame.image.load('alien1.png')

dog = sprite.PlayableSprite('dog anim 3.png', 5)
# dog.loadImage()
mars = sprite.Sprite('marsDemo.png').loadImage()
earth = sprite.Sprite('earth.png').loadImage()
cosmo = sprite.Sprite('cosmo.png')
cosmo.loadImage()





# frame = get_image(carImg, 32, 32,1, 10)
x = 0
y = 450
i = 0
j=0
k=0
speed = 1
scale = 3
fps = 1
move = -110
doImoveR = False
img = dog

up = False
flag = 0
doImoveL = False
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                dog.amIJumping = True
            if event.key == pygame.K_q:
                scale += 1
            if event.key == pygame.K_a:
                scale -= 1
            if event.key == pygame.K_z:
                fps += 1
                print(fps)
            if event.key == pygame.K_x:
                fps -= 1
                print(fps)
            if event.key == pygame.K_RIGHT:
                doImoveR = True
            if event.key == pygame.K_LEFT:
                doImoveL = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                doImoveR = False
                i = 0
            if event.key == pygame.K_LEFT:
                doImoveL = False
                i = 0

    if dog.amIJumping:
        y, i = dog.jump(y, 2)

    if doImoveR:
        move, i = dog.moveRight(move, i)

    if move> 100 and j<1000:
        j+=10
        k+=1
        if k ==4:
            k=0

    gameDisplay.blit(earth, (0,0))
    gameDisplay.blit(dog.getFrame(40,40,i,scale), (move,y))
    gameDisplay.blit(cosmo.getFrame(50,71,0,4), (300, 310))

    # car(move, y, i, scale, img, 40, 40)
    #
    # car(-60+j, 350, k, 4, alien1, 20, 50)
    # car(-80+j, 350, k, 4, alien1, 20, 50)
    # car(-100+j, 350,k, 4, alien1, 20, 50)
    # car(-120+j, 350, k, 4, alien1, 20, 50)
    # car(-140+j, 350, k, 4, alien1, 20, 50)
    # car(-160+j, 350, k, 4, alien1, 20, 50)
    # car(-180+j, 350, k, 4, alien1, 20, 50)
    # car(-200+j, 350, k, 4, alien1, 20, 50)



    # TODO
    '''
    make a collison class - a class with collisons that can be replicated
    make a object class - playable character 
    make bigger chrackter - form edge to edge
    '''
    pygame.display.update()
    clock.tick(60)  # fps

pygame.quit()
