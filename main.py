import time

import pygame

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))

# black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()
crashed = False
carImg = pygame.image.load('New Piskel.png')  # 32x32
jump = pygame.image.load('New Piskel-5.png.png')
background = pygame.image.load('back.png')
rect = pygame.Rect(130, 500, 200, 50)
dog = pygame.image.load('dog anim 3.png')  # 40x40
mars = pygame.image.load('marsDemo.png')
alien1 = pygame.image.load('alien1.png')


def get_image(sheet, width, heigth, frame, scale):
    image = pygame.Surface((width, heigth))
    image.blit(sheet, (0, 0), ((frame * width), 0, width, heigth))
    image = pygame.transform.scale(image, (width * scale, heigth * scale))
    image.set_colorkey((0, 0, 0))

    return image


def car(x, y, fr, scale, image, width, heigth):
    gameDisplay.blit(get_image(image, width, heigth, fr, scale), (x, y))


# frame = get_image(carImg, 32, 32,1, 10)
x = 0
y = 400
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
                up = True

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
                print(i)
            if event.key == pygame.K_LEFT:
                doImoveL = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                doImoveR = False
                i = 0
            if event.key == pygame.K_LEFT:
                doImoveL = False
                i = 0

    if up:
        i = 2

        if not flag:
            y -= 5
        else:
            y += 5
        time.sleep(0.001)
        if y == 400 - 50:
            flag = 1

        if y == 400 and flag:
            up = False
            flag = 0
            i = 0

    if doImoveR:
        move += 10
        time.sleep(0.065)  # fps
        if not up:
            img = dog
            i += 1
            if i == 5:  # for dog anim 3 because there are 5 frames
                i = 0
            print(move)
    if doImoveL:

        move -= 5
        time.sleep(0.1)

        if not up:
            img = dog
            i += 1
            if i == 4:
                i = 0
            print(move)

    if move> 100 and j<1000:
        j+=10
        k+=1
        if k ==4:
            k=0

    gameDisplay.blit(mars, (0, 0))
    car(move, y, i, scale, img, 40, 40)

    car(-60+j, 350, k, 4, alien1, 20, 50)
    car(-80+j, 350, k, 4, alien1, 20, 50)
    car(-100+j, 350,k, 4, alien1, 20, 50)
    car(-120+j, 350, k, 4, alien1, 20, 50)
    car(-140+j, 350, k, 4, alien1, 20, 50)
    car(-160+j, 350, k, 4, alien1, 20, 50)
    car(-180+j, 350, k, 4, alien1, 20, 50)
    car(-200+j, 350, k, 4, alien1, 20, 50)



    # TODO
    '''
    make a collison class - a class with collisons that can be replicated
    make a object class - playable character 
    make bigger chrackter - form edge to edge
    '''
    pygame.display.update()
    clock.tick(60)  # fps

pygame.quit()
