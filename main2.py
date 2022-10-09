import DisplayGame
import collisions
import sprite
from player import Player
import pygame

################################# LOAD UP A BASIC WINDOW AND CLOCK #################################
pygame.init()
display_width = 1200
display_height = 800

running = True
clock = pygame.time.Clock()
TARGET_FPS = 60

################################# LOAD PLAYER AND SPRITESHEET###################################
gameDisplay = DisplayGame.GameDisplay(display_width, display_height).displayGame()
spaceShip = sprite.Sprite('spaceship.png').loadImage()
dog = Player('dog anim 3.png', 5)
scale = 3
################################# OBSTICALES ####################################
floor = sprite.Obsticales(1200, 20, 0, 750)
r1 = sprite.Obsticales(100, 100, 500, 500)
########## COLLISIONS ##################
collision_objects_list = [floor, r1]
#################################### LOAD THE LEVEL #######################################
dog.position.x, dog.position.y = 100, 100

################################# GAME LOOP ##########################
while running:
    dt = clock.tick(60) * .001 * TARGET_FPS
    ################################# CHECK PLAYER INPUT #################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dog.LEFT_KEY = True
            elif event.key == pygame.K_RIGHT:
                dog.RIGHT_KEY = True
            elif event.key == pygame.K_SPACE:
                dog.jump()
            elif event.key == pygame.K_DOWN:
                dog.acceleration.y +=.5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                dog.LEFT_KEY = False
                dog.frame = 0
            elif event.key == pygame.K_RIGHT:
                dog.RIGHT_KEY = False
                dog.frame = 0
            elif event.key == pygame.K_SPACE:
                if dog.is_jumping:
                    dog.velocity.y *= .25
                    dog.is_jumping = False
            elif event.key == pygame.K_DOWN:
                dog.acceleration.y=0



    ################################# UPDATE/ Animate SPRITE #################################


    ################################# UPDATE WINDOW AND DISPLAY #################################
    gameDisplay.blit(spaceShip, (0, 0))
    pygame.draw.rect(gameDisplay, (255, 0, 0), floor)
    pygame.draw.rect(gameDisplay, (255, 0, 0), r1)
    # pygame.draw.rect(gameDisplay, (255, 255, 0), dog.rect)
    gameDisplay.blit(dog.getFrame(40, 40, scale), (dog.position.x, dog.position.y))
    dog.collisions = collisions.collision_test(dog.rect, collision_objects_list)
    print(dog.rect.colliderect(floor))
    # dog.collisions = collisions.collision_test(dog.rect, collision_objects_list)
    print(dog.collisions)

    # print(floor.rect.top)
    # print(dog.rect.bottom
    dog.update(dt)
    # dog.updateRect()

    pygame.display.update()
