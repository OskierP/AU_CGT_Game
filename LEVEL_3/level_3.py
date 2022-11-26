import os
import random

import pygame

import flags

pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN.fill((29, 17, 53))

FLYING = [pygame.image.load(os.path.join(r"LEVEL_3/Assets/Rocket/Rocket1.png")),
          pygame.image.load(os.path.join(r"LEVEL_3/Assets/Rocket/Rocket2.png")),
          pygame.image.load(os.path.join(r"LEVEL_3/Assets/Rocket/Rocket3.png")),
          pygame.image.load(os.path.join(r"LEVEL_3/Assets/Rocket/Rocket4.png"))]
JUMPING = pygame.image.load(os.path.join(r"LEVEL_3/Assets/Rocket/Rocket4.png"))
DUCKING = [pygame.image.load(os.path.join(r"LEVEL_3/Assets/Rocket/Rocket1.png")),
           pygame.image.load(os.path.join(r"LEVEL_3/Assets/Rocket/Rocket2.png"))]

SMALL_ALIEN = [pygame.image.load(os.path.join(r"LEVEL_3/Assets/Alien/asteroid1.png")),
               pygame.image.load(os.path.join(r"LEVEL_3/Assets/Alien/asteroid1.png")),
               pygame.image.load(os.path.join(r"LEVEL_3/Assets/Alien/asteroid1.png"))]
MILKYWAY = [pygame.image.load(os.path.join(r"LEVEL_3/Assets/Alien/milkyway.png")),
            pygame.image.load(os.path.join(r"LEVEL_3/Assets/Alien/milkyway2.png"))]

UFO = [pygame.image.load(os.path.join(r"LEVEL_3/Assets/Spaceship/Spaceship1.png")),
       pygame.image.load(os.path.join(r"LEVEL_3/Assets/Spaceship/Spaceship2.png"))]

PLANET = pygame.image.load(os.path.join(r"LEVEL_3/Assets/Other/Planet.png"))

BG = SCREEN.fill((29, 17, 53))


class Rocket:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = FLYING
        self.jump_img = JUMPING

        self.rocket_duck = False
        self.rocket_run = True
        self.rocket_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.rocket_rect = self.image.get_rect()
        self.rocket_rect.x = self.X_POS
        self.rocket_rect.y = self.Y_POS

    def update(self, userInput):
        if self.rocket_duck:
            self.duck()
        if self.rocket_run:
            self.run()
        if self.rocket_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.rocket_jump:
            self.rocket_duck = False
            self.rocket_run = False
            self.rocket_jump = True
        elif userInput[pygame.K_DOWN] and not self.rocket_jump:
            self.rocket_duck = True
            self.rocket_run = False
            self.rocket_jump = False
        elif not (self.rocket_jump or userInput[pygame.K_DOWN]):
            self.rocket_duck = False
            self.rocket_run = True
            self.rocket_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.rocket_rect = self.image.get_rect()
        self.rocket_rect.x = self.X_POS
        self.rocket_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.rocket_rect = self.image.get_rect()
        self.rocket_rect.x = self.X_POS
        self.rocket_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.rocket_jump:
            self.rocket_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.rocket_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rocket_rect.x, self.rocket_rect.y))


class Planet:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = PLANET
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallAlien(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class Milkway(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        self.rect.y = 300


class Ufo(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Rocket()
    planet = Planet()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Kilometers travelled: " + str(points), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (900, 40)
        SCREEN.blit(text, textRect)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if points > 2000:  #### TO DO: Around 2000 points Mars could move to sight and then level would end. Cutscene and new level
            run = False
            flags.next_lvl_3.set_flag(True)

        SCREEN.fill((29, 17, 53))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallAlien(SMALL_ALIEN))
            elif random.randint(0, 2) == 1:
                obstacles.append(Milkway(MILKYWAY))
            elif random.randint(0, 2) == 2:
                obstacles.append(Ufo(UFO))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.rocket_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        planet.draw(SCREEN)
        planet.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    print('hej1')
    while run:

        if flags.next_lvl_3.get_flag():
            run = False

        SCREEN.fill((29, 17, 53))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (255, 255, 255))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (255, 255, 255))
            score = font.render("Kilometers travelled: " + str(points), True, (255, 255, 255))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(FLYING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()

# menu(death_count=0)
