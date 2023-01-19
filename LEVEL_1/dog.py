import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 3
        self.max_health = 3
        self.attack = 1
        self.velocity = 0
        self.image = pygame.image.load("LEVEL_1/assets/sprite_dog1.png")
        self.rect = self.image.get_rect()
        self.rect.x = 1580
        self.rect.y = 2985
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.ground_y = 500

        # jump
        self.jumping = False
        self.jumpingVelocity = 0

        # sprite
        # animation déplacement
        self.facingRight = True
        self.walkAnimationRight = False
        self.walkAnimationLeft = False
        self.spritesWalkRight = [pygame.image.load('LEVEL_1/assets/sprite_dog1.png'),
                                 pygame.image.load('LEVEL_1/assets/sprite_dog2.png'),
                                 pygame.image.load('LEVEL_1/assets/sprite_dog_jump.png'),
                                 pygame.image.load('LEVEL_1/assets/sprite_dog3.png'),
                                 pygame.image.load('LEVEL_1/assets/sprite_dog4.png')]
        self.spritesWalkLeft = [pygame.transform.flip(self.spritesWalkRight[0], True, False),
                                pygame.transform.flip(self.spritesWalkRight[1], True, False),
                                pygame.transform.flip(self.spritesWalkRight[2], True, False),
                                pygame.transform.flip(self.spritesWalkRight[3], True, False),
                                pygame.transform.flip(self.spritesWalkRight[4], True, False)]
        self.walkFrame = 0

        self.spritesJumpRight = pygame.image.load('LEVEL_1/assets/sprite_dog_jump.png')
        self.spritesJumpLeft = pygame.transform.flip(self.spritesJumpRight, True, False)

    def jump(self):
        # only jumps if on ground
        '''
        if self.rect.y == 2985 :
            self.jumping = True
            self.jumpingVelocity = 5
        '''
        self.jumping = True
        self.jumpingVelocity = 35

    def gravity(self):
        if self.jumpingVelocity <= -23:
            self.jumpingVelocity = -23
        else:
            self.jumpingVelocity -= 1.5

        '''
        # if we are jumping, continue going upwards
        if self.jumping:
            # move upwards
            self.rect.y = min(self.rect.y - self.jumpingVelocity, 2985)

            # decrease y-velocity
            self.jumpingVelocity = self.jumpingVelocity - 0.04

            if self.rect.y == 2985:
                # if on the ground, stop
                self.jumping = False
                self.jumpingVelocity = 0
        '''

    def move_right(self):
        self.rect.x += self.velocity
        self.walkAnimationRight = True
        self.facingRight = True

    def move_left(self):
        self.rect.x += self.velocity
        self.walkAnimationLeft = True
        self.facingRight = False
