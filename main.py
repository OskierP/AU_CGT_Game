import time

import pygame

import physics
import sprite

import DisplayGame

pygame.init()

display_width = 1200
display_height = 900

# gameDisplay = pygame.display.set_mode((display_width, display_height))
gameDisplay = DisplayGame.GameDisplay(display_width, display_height).displayGame()

# black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()
crashed = False
rect = pygame.Rect(500, 500, 200, 50)
# alien1 = pygame.image.load('alien1.png')
r2 = pygame.Rect(50,50,50,50)
r3 = pygame.Rect(200,200,200,200)
dog = sprite.PlayableSprite('dog anim 3.png', 5)
spaceShip = sprite.Sprite('spaceship.png').loadImage()
r1 = sprite.Obsticales(100, 100, 500, 500)
floor = sprite.Obsticales(1200, 20, 0, 750)
celling = sprite.Obsticales(1200, 20, 0,10)

collision_objects_list = [r1, floor, celling]


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
doImoveD = False
doImoveU = False

print(r3.left)

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        if event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_UP:
            #     # dog.amIJumping = True
            if event.key == pygame.K_RIGHT:
                doImoveR = True
            if event.key == pygame.K_LEFT:
                doImoveL = True
            if event.key == pygame.K_DOWN:
                doImoveD = True
            if event.key == pygame.K_UP:
                doImoveU = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                doImoveR = False
                i = 0
            if event.key == pygame.K_LEFT:
                doImoveL = False
                i = 0
            if event.key == pygame.K_DOWN:
                doImoveD = False
            if event.key == pygame.K_UP:
                doImoveU = False

    # if dog.amIJumping:
    #     i = dog.jump(2)


    if doImoveL:
        i = dog.moveLeft(i)


    if doImoveR:
        i = dog.moveRight(i)


    if doImoveD:
        dog.moveDown()

    if doImoveU:
        dog.moveUp()





    # r1.set_color(gameDisplay, (255,255, 0))

    # print(dog.rect)
    gameDisplay.blit(spaceShip, (0,0))
    # pygame.draw.rect(gameDisplay, (255, 0, 0), dog.rect)
    # pygame.draw.rect(gameDisplay, (255,0,255), r2)
    collisions = physics.collision_test(dog.rect, collision_objects_list)
    physics.collison(dog, collisions)
    gameDisplay.blit(dog.getFrame(40,40,i,scale), (dog.x, dog.y))
    pygame.draw.rect(gameDisplay, (255,255,0), celling)

    pygame.draw.rect(gameDisplay, (255, 255, 0), r1)
    pygame.draw.rect(gameDisplay, (255, 255, 0), r3)
    # r1.set_color(gameDisplay, (255, 0,0))



    # TODO
    '''
    make a collison class - a class with collisons that can be replicated
    make a object class - playable character 
    make bigger chracter - form edge to edge
    '''
    pygame.display.update()
    clock.tick(60)  # fps

pygame.quit()
