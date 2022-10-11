import DisplayGame
import collisions
import sprite
from player import Player, Box
import pygame

################################# LOAD UP A BASIC WINDOW AND CLOCK #################################
pygame.init()
display_width = 1100  # 1100
display_height = 600  # 600

running = True
clock = pygame.time.Clock()
TARGET_FPS = 60

gravity = 0
friction = 0


################################# LOAD PLAYER AND SPRITESHEET###################################
gameDisplay = DisplayGame.GameDisplay(display_width, display_height).displayGame()
spaceShip = sprite.Sprite('spaceshipv3.png').loadImage()
dog = Player('dog anim 3.png', 5, gravity, friction)
scale = 3

box = Box('box.png', gravity, friction)

################################# OBSTICALES ####################################
floor = sprite.Obsticales(1200, 20, 0, 750)
r1 = sprite.Obsticales(100, 100, 500, 500)
wall_left = sprite.Obsticales(20, 400, 1000, 350 )
########## COLLISIONS ##################
collision_objects_player = [floor, r1, wall_left, box]
collision_objects_box = [floor]
collision_objects_box_player = [box]
#################################### LOAD THE LEVEL #######################################
dog.position.x, dog.position.y = 100, 100
box.position.x, box.position.y = 200, 200
box.width, box.heigth = 20,20


################################# GAME LOOP ##########################
flag = True
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
            elif event.key == pygame.K_DOWN and not gravity and not friction:
                dog.acceleration.y +=.5
            elif event.key == pygame.K_j:
                if flag:
                    gravity = 0.3
                    flag = False
                else:
                    gravity = 0
                    flag = True
                print(gravity)
                dog.gravity = gravity
                box.gravity = gravity
                # pygame.quit()

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
            # move movment to player class
            # elif event.key == pygame.K_DOWN and not gravity and not friction:
            #     dog.acceleration.y+=0



    ################################# UPDATE/ Animate SPRITE #################################


    ################################# UPDATE WINDOW AND DISPLAY #################################
    gameDisplay.blit(spaceShip, (0, 0))
    pygame.draw.rect(gameDisplay, (255, 0, 0), floor)
    pygame.draw.rect(gameDisplay, (255, 0, 0), wall_left)
    pygame.draw.rect(gameDisplay, (255, 0, 0), r1)
    print(dog.gravity)
    dog.collisions = collisions.collision_test(dog.rect, collision_objects_player)
    dog.obj = collisions.collision_test(dog.rect, collision_objects_box_player)
    box.collisions = collisions.collision_test(box.rect, collision_objects_box)


    gameDisplay.blit(dog.getFrame(40, 40, scale), (dog.position.x, dog.position.y))
    gameDisplay.blit(box.getFrame(20, 20, scale), (box.position.x, box.position.y))

    # pygame.draw.rect(gameDisplay, (255, 255, 0), dog.rect)
    # pygame.draw.rect(gameDisplay, (255, 0, 255), box.rect)
    # print(dog.rect.colliderect(box.rect))
    # print(dog.rect.colliderect(floor))
    # dog.collisions = collisions.collision_test(dog.rect, collision_objects_player)
    # print(dog.collisions)

    # print(floor.rect.top)
    # print(dog.rect.bottom
    dog.update(dt)
    box.update(dt)
    # dog.updateRect()

    pygame.display.update()
