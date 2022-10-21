import pygame
import math
import collisions


class Sprite:

    def __init__(self, image, x=0, y=0):
        self.image = image
        self.x = x
        self.y = y
        self.width = 0
        self.heigth = 0
        self.frame = 0

    def loadImage(self):
        return pygame.image.load(self.image)

    def getFrame(self, width, heigth, scale):
        frame = pygame.Surface((width, heigth))
        frame.blit(self.loadImage(), (0, 0), ((self.frame * width), 0, width, heigth))
        frame = pygame.transform.scale(frame, (width * scale, heigth * scale))
        # frame.set_colorkey((0, 0, 0))
        self.width = width * scale
        self.heigth = heigth * scale
        return frame


class Player(Sprite):
    def __init__(self, image, frames, gravity, friction):
        Sprite.__init__(self, image, 100, 100)
        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False
        self.is_jumping, self.on_ground = False, False
        self.gravity, self.friction = gravity, friction
        self.position, self.velocity = pygame.math.Vector2(0, 0), pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        self.frames = frames
        self.rect = pygame.Rect(self.position.x, self.position.y, 40 * 2, 41 * 2)
        self.collisions = []
        self.collison_with_box = []

    def updateRect(self):
        self.rect = pygame.Rect(self.position.x, self.position.y, 40 * 2.25, 40 * 2.25)

    def update(self, dt):
        self.horizontal_movement(dt)
        self.vertical_movement(dt)
        collisions.collison(self, self.collisions)
        self.updateRect()
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        if self.frame > self.frames - 1:
            self.frame = 0

    def horizontal_movement(self, dt):
        self.acceleration.x = 0
        if self.LEFT_KEY:
            self.acceleration.x -= .3
            self.frame += 1
        elif self.RIGHT_KEY:
            self.acceleration.x += .3
            self.frame += 1
        if not self.on_ground:
            self.frame = 2

        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(4)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
        if self.collisions:
            collisions.collison(self, self.collisions)
        if self.collison_with_box:
            collisions.move_collision(self, self.collison_with_box)
        print(f'dog spedd: {self.velocity.x}')
        self.rect.x = self.position.x

    def vertical_movement(self, dt):
        # print(f'1: {self.position.y}')
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7: self.velocity.y = 7
        self.position.y += (self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt))

        # print(f'2: {self.position.y}')
        if self.collisions:
            collisions.collison(self, self.collisions)
            # self.on_ground = True
            self.velocity.y = 0
        #     # self.position.y = 630
        self.rect.bottom = self.position.y
        print(self.rect.bottom)

    def limit_velocity(self, max_vel):
        # min(-max_vel, max(self.velocity.x, max_vel))
        # if abs(self.velocity.x) < .01: self.velocity.x = 0
        max_vel_tmp = max_vel
        min(-max_vel, max(self.velocity.x, max_vel))
        if self.gravity == 0:
            if self.velocity.x < 0: max_vel_tmp = -max_vel
            if abs(self.velocity.x) > max_vel: self.velocity.x = max_vel_tmp
        if abs(self.velocity.x) < .01: self.velocity.x = 0

    def jump(self):
        if self.on_ground:
            self.is_jumping = True
            self.velocity.y -= 7
            self.on_ground = False


class Box(Sprite):
    def __init__(self, image, gravity, friction):
        Sprite.__init__(self, image, 100, 100)
        self.on_ground = False
        self.gravity, self.friction = gravity, friction
        self.position, self.velocity = pygame.math.Vector2(0, 0), pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        self.rect = pygame.Rect(self.position.x, self.position.y, self.width, self.heigth)
        self.collisions = []
        self.flag = False

    def updateRect(self):
        self.rect = pygame.Rect(self.position.x, self.position.y, self.width, self.heigth)

    def update(self, dt):
        self.horizontal_movement(dt)
        self.vertical_movement(dt)
        # collisions.collison(self, self.collisions)
        # if self.collisions:
        #     print(main2.placeBox)
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        self.updateRect()

    def horizontal_movement(self, dt):
        self.acceleration.x = 0
        # print(f'box spedd: {self.velocity.x}')
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(5)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)

        if self.collisions:
            print(self)
            collisions.collison(self, self.collisions)

        # self.rect.x = self.position.x

    def vertical_movement(self, dt):
        # print(f'1: {self.position.y}')
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7: self.velocity.y = 7
        self.position.y += (self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt))

        # print(f'2: {self.position.y}')
        if self.collisions:
            collisions.collison(self, self.collisions)
            # self.on_ground = True
            self.velocity.y = 0
        #     # self.position.y = 630
        self.rect.bottom = self.position.y
        # print(self.rect.bottom)

    def limit_velocity(self, max_vel):
        max_vel_tmp = max_vel
        min(-max_vel, max(self.velocity.x, max_vel))
        if self.gravity == 0:
            if self.velocity.x < 0: max_vel_tmp = -max_vel
            if abs(self.velocity.x) > max_vel: self.velocity.x = max_vel_tmp
        if abs(self.velocity.x) < .01: self.velocity.x = 0
