import pygame.image
import time

import DisplayGame


class Sprite:

    def __init__(self, image):
        self.image = image

    def loadImage(self):
        return pygame.image.load(self.image)

    def getFrame(self, width, heigth, frame_nr, scale):
        frame = pygame.Surface((width, heigth))
        frame.blit(self.loadImage(), (0, 0), ((frame_nr * width), 0, width, heigth))
        frame = pygame.transform.scale(frame, (width * scale, heigth * scale))
        frame.set_colorkey((0, 0, 0))

        return frame


class PlayableSprite(Sprite):

    def __init__(self, image, frames):
        Sprite.__init__(self, image)
        self.frames = frames
        self.amIJumping = False
        self.amIFalling = False

    def moveRight(self, x, frame):
        x += 10
        time.sleep(0.065)  # fps

        if not self.amIJumping:
            frame += 1
            if frame == self.frames:
                frame = 0
            print(x)
        return x, frame

    def moveLeft(self, x, frame):
        x -= 10
        time.sleep(0.065)  # fps

        if not self.amIJumping:
            frame += 1
            if frame == self.frames:
                frame = 0
            print(x)

        return x, frame

    def jump(self, y, frame,):
        if not self.amIFalling:
            y -= 5
        else:
            y += 5
        time.sleep(0.001)
        if y == 400 - 50:
            self.amIFalling = True
        if y == 400 and self.amIFalling:
            self.amIJumping = False
            self.amIFalling = False
            frame = 0
        return y, frame

    # def moveUp(self, frame, y):
