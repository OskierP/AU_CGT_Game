import time

import pygame

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')

# black = (0, 0, 0)
white = (255, 255, 255)

clock = pygame.time.Clock()
crashed = False
carImg = pygame.image.load('New Piskel.png')
jump = pygame.image.load('New Piskel-5.png.png')


def get_image(sheet, width, heigth, frame, scale):
    image = pygame.Surface((width, heigth))
    image.blit(sheet, (0, 0), ((frame * width), 0, width, heigth))
    image = pygame.transform.scale(image, (width * scale, heigth * scale))
    image.set_colorkey((0, 0, 0))

    return image


def car(x, y, fr, scale, image):
    gameDisplay.blit(get_image(image, 32, 32, fr, scale), (x, y))


# frame = get_image(carImg, 32, 32,1, 10)
x = 800/2
y = 600/2
i = 0
speed = 1
scale=10
fps =1
move=0
doImoveR = False
img = carImg
up = False
flag =0
doImoveL= False
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:

                up = True



            if event.key == pygame.K_q:
                scale+=1
            if event.key == pygame.K_a:
                scale-=1
            if event.key == pygame.K_z:
                fps+=1
                print(fps)
            if event.key == pygame.K_x:
                fps-=1
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
        img = jump

        if not flag:
            y-=5
        else:
            y+=5
        time.sleep(0.001)
        if y==600/2-50:
            flag = 1

        if y==600/2 and flag:
            up = False
            img = carImg
            flag = 0

    if doImoveR:
        move+=10
        time.sleep(0.05)
        if not up:
            img = pygame.image.load('New Piskel.png')
            i += 1
            if i == 4:
                i = 0
            print(move)
    if doImoveL:

        move -= 10
        time.sleep(0.05)

        if not up:
            img = pygame.image.load('New Piskel-left.png')
            i += 1
            if i == 4:
                i = 0
            print(move)


    gameDisplay.fill(white)
    car(move, y, i, scale, img)

    pygame.display.update()
    clock.tick(60) #fps



pygame.quit()

