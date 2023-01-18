
import os
import pygame
from pygame import mixer
import random


pygame.init()

clock = pygame.time.Clock()
fps = 50

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DARK_BLUE = (29, 17, 53)

#load images
rocket_img1 = pygame.image.load('Assets/Rocket/Rocket1.png')
rocket_img2 = pygame.image.load('Assets/Rocket/Rocket2.png')
rocket_img3 = pygame.image.load('Assets/Rocket/Rocket3.png')
rocket_img4 = pygame.image.load('Assets/Rocket/Rocket4.png')
asteroid_img = pygame.image.load('Assets/Alien/asteroid1.png')
milkyway_img1 = pygame.image.load('Assets/Alien/milkyway1.png')
milkyway_img2 = pygame.image.load('Assets/Alien/milkyway2.png')
spaceship_img1 = pygame.image.load('Assets/Spaceship/Spaceship1.png')
spaceship_img2 = pygame.image.load('Assets/Spaceship/Spaceship2.png')
planet_img = pygame.image.load('Assets/Other/Planet.png')

#background image
bg_img = pygame.image.load('Assets/Other/spacebg.png').convert_alpha()
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

#load music and sounds
# source https://www.youtube.com/watch?v=9NcPvmk4vfo
pygame.mixer.music.load('Assets/Other/space_ride_music.mp3')
pygame.mixer.music.set_volume(.3)
pygame.mixer.music.play(-1, 0.0, 5000)
FLYING = [rocket_img1, rocket_img2, rocket_img3, rocket_img4]
JUMPING = rocket_img4
DUCKING = [rocket_img1, rocket_img2]
SMALL_ALIEN = [asteroid_img, asteroid_img, asteroid_img]
MILKYWAY = [milkyway_img1, milkyway_img2]
UFO = [spaceship_img1, spaceship_img2]
PLANET = planet_img

def draw_bg():
    SCREEN.fill(DARK_BLUE)
    width = bg_img.get_width()
    for x in range(10):
        SCREEN.blit(bg_img, ((x * width), 0))

# The base classes of this code come from the following source. Alterations were made for the purpose of Martian Mission.
# codewmax (2020) chrome-dinosaur main.py (Version unknown) [Source code]. https://github.com/codewmax/chrome-dinosaur

class Rocket:
    Y_POS = SCREEN_HEIGHT / 2
    X_POS = 80
    #Y_POS = 310 # this is y-position of the rocket
    JUMP_VEL = 5.0
    DUCK_VEL = 5.0

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = FLYING
        self.jump_img = JUMPING

        self.rocket_duck = False
        self.rocket_run = True
        self.rocket_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.duck_vel = self.DUCK_VEL
        self.image = self.run_img[0]
        self.rocket_rect = self.image.get_rect()
        self.rocket_rect.x = self.X_POS
        self.rocket_rect.y = self.Y_POS
        #self.rocket_rect.y = self.Y_POS

    def update(self, userInput):
        dy = self.rocket_rect.y

        if self.rocket_duck:
            self.duck()
        if self.rocket_run:
            self.run()
        if self.rocket_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if (userInput[pygame.K_UP] and not self.rocket_jump) and self.rocket_jump < SCREEN_HEIGHT:
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
        # if userInput[pygame.K_UP] and not self.rocket_jump and self.rocket_jump < SCREEN_HEIGHT:
        #     self.rocket_rect.y -= 20
        # elif userInput[pygame.K_DOWN] and not self.rocket_jump:
        #     self.rocket_rect.y += 20

        if self.rocket_rect.bottom >= SCREEN_HEIGHT:
            self.rocket_rect.y = dy
        if self.rocket_rect.top <= 0:
            self.rocket_rect.y = 0


    #Duck currently goes up then down
    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        if self.rocket_duck:
            self.rocket_rect.y += self.duck_vel * 4
            self.duck_vel += 0.2
        if self.duck_vel < - self.DUCK_VEL:
            self.rocket_duck = False
            self.duck_vel = self.DUCK_VEL

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        if self.rocket_run:
            self.rocket_rect.y -= self.jump_vel
            self.jump_vel -= 0.6
        if self.jump_vel < - self.JUMP_VEL:
            self.rocket_jump = False
            self.jump_vel = self.JUMP_VEL
        self.step_index += 1


    def jump(self):
        self.image = self.jump_img
        if self.rocket_jump:
            self.rocket_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < self.JUMP_VEL:
            self.rocket_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rocket_rect.x, self.rocket_rect.y))


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
    global game_speed , x_pos_bg , y_pos_bg , points , obstacles
    run = True
    clock = pygame.time.Clock ()
    player = Rocket ()
    # planet = Planet()
    game_speed = 15
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf' , 20)
    obstacles = []
    death_count = 0

    def score():
        global points , game_speed
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
            # elif event.key == pygame.K_ESC:
            #     run = False

        if points > 2500:  #### TO DO: Around 2000 points Mars could move to sight and then level would end. Cutscene and new level
            run = False

        SCREEN.fill((29, 17, 53))
        userInput = pygame.key.get_pressed()

        draw_bg()
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

        #planet.draw(SCREEN)
        #planet.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((DARK_BLUE))
        font = pygame.font.Font('freesansbold.ttf', 30)

        #if points == 100:
         #   pygame.time.delay(2000)
          #  death_count += 1
           # menu(death_count)

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


menu(death_count=0)


# It jumps whilst running, don't make it look like a jump so much (or make the jumps smaller)
# Ducks goes wayyy to far off screen & is sudden from the current position
# Implement collisions so things blow up when you touch them
# Would be cool to have stuff flying toward me

pygame.display.quit()
pygame.quit()
