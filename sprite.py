import pygame.image
import time

import DisplayGame


class Sprite:

    def __init__(self, image, x=0,y=0):
        self.image = image
        self.x = x
        self.y = y
        self.width = 0
        self.heigth= 0
        self.gravity = 4

    def loadImage(self):
        return pygame.image.load(self.image)

    def getFrame(self, width, heigth, frame_nr, scale):
        frame = pygame.Surface((width, heigth))
        frame.blit(self.loadImage(), (0, 0), ((frame_nr * width), 0, width, heigth))
        frame = pygame.transform.scale(frame, (width * scale, heigth * scale))
        frame.set_colorkey((0, 0, 0))
        self.width = width * scale
        self.heigth = heigth * scale


        return frame

    def scale(self, width, height):
        return pygame.image.load(pygame.transform.scale(self.image, (width, height)))



class PlayableSprite(Sprite):

    def __init__(self, image, frames):
        Sprite.__init__(self, image,100, 100)
        self.frames = frames
        self.amIJumping = False
        self.amIFalling = False
        self.rect = pygame.Rect(self.x, self.y,40*3, 40*3)
        self.collisions = []
        self.onGround = False
        self.jumpHeight = self.y

    def updateRect(self):
        self.rect = pygame.Rect(self.x, self.y, 40*3, 40*3)


    def moveRight(self, frame):
        self.x += 5
        time.sleep(0.04)  # fps

        if self.onGround:
            frame += 1
            if frame == self.frames:
                frame = 0

        self.updateRect()
        return frame

    def moveLeft(self, frame):

        self.x -= 5

        # time.sleep(0.065)  # fps

        if not self.amIJumping:
            frame += 1
            if frame == self.frames:
                frame = 0
            print(self.x)


        self.updateRect()
        return frame

    def moveDown(self):
        self.y +=5
        # time.sleep(0.065)
        self.updateRect()

    def moveUp(self):
        self.y-= 5
        # time.sleep(0.065)
        self.updateRect()
        self.update()

    def jump(self, frame,):
        if not self.amIFalling:
            self.y -= 5
        else:
            self.y += 5
        time.sleep(0.001)
        if self.y == 400 - 50:
            self.amIFalling = True
        if self.y == 400 and self.amIFalling:
            self.amIJumping = False
            self.amIFalling = False
            frame = 0
        return frame

    def vertical(self):
        if not self.onGround:
            self.y += self.gravity
        if self.amIJumping:
            self.y -=10
        if self.y <= self.jumpHeight or self.collisions:
            self.amIJumping = False

        self.updateRect()

    def j(self):
        if self.onGround:
            self.amIJumping = True
            self.onGround = False
            self.jumpHeight = (self.y - 100)/self.gravity
        self.update()

        # if self.collisions:
        #     for collison in self.collisions:
        #         if abs(self.rect.bottom - collison.rect.top) < 10:
        #             self.y = collison.rect.top - self.heigth



    def update(self):
        self.vertical()



class Obsticales:

    def __init__(self, width, heigth, x, y):
        self.width = width
        self.height = heigth
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x ,self.y, self.width, self.height)
        self.collison = []
        self.flag = False

    def update_rect(self):
         self.rect = pygame.Rect(self.x ,self.y, self.width, self.height)
         # print(f' WITDH: {self.width}')# use when level ready

    def update_continous(self):
        if self.collison:
            self.flag = True
        else:
            self.flag = False

    def update_press(self):
        if self.collison:
            self.flag = True



