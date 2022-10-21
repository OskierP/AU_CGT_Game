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
delay = 0

gravity = 0
friction = 0

################################# LOAD PLAYER AND SPRITESHEET###################################
gameDisplay = DisplayGame.GameDisplay(display_width, display_height).displayGame()
spaceShip = sprite.Sprite('spaceshipv3.png').loadImage()
dog = Player('dog anim 3.png', 5, gravity, friction)
scale = 2.25

box = Box('box.png', gravity, friction)
box2 = Box('box.png', gravity, friction)

################################# OBSTICALES ####################################
celing = sprite.Obsticales(1100, 20, 0, 0)
obj11 = sprite.Obsticales(100, 15, 0, 200)
obj12 = sprite.Obsticales(1100, 15, 250, 200)
obj21 = sprite.Obsticales(500, 15, 0, 400)
obj22 = sprite.Obsticales(500, 15, 650, 400)
floor = sprite.Obsticales(1200, 20, 0, 570)

wall_left = sprite.Obsticales(20, 900, 1090, 0)
wall_right = sprite.Obsticales(10, 900, 0, 0)
placeBox = sprite.Obsticales(50, 60, 1050, 480)
open_door = sprite.Obsticales(50, 60, 1050, 300)
laser = sprite.Obsticales(0, 600, 600, 0)
########## COLLISIONS ##################
collision_objects_player = [floor, wall_right, wall_left, box, laser, celing, box2]
collision_objects_box = [floor, box2, box, wall_right, wall_left]
collision_objects_box_player = [box, box2]
collision_interactive = [box, dog]
#################################### LOAD THE LEVEL #######################################
dog.position.x, dog.position.y = 100, 100
box.position.x, box.position.y = 200, 500
box2.position.x, box2.position.y = 100, 400
box.width, box.heigth = 20, 20
box2.width, box2.heigth = 20, 20

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
                dog.acceleration.y += .5
            elif event.key == pygame.K_UP and not gravity and not friction:
                dog.acceleration.y -= .5
            elif event.key == pygame.K_j:
                if flag:
                    gravity = 0.3
                    friction = -.12
                    flag = False
                else:
                    gravity = 0
                    friction = 0
                    flag = True
                print(gravity)
                dog.gravity = gravity
                dog.friction = friction
                box.gravity = gravity
                box.friction = friction
                box2.gravity = gravity
                box2.friction = friction
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

    delay += 1
    if delay == 70:
        if laser.width == 0:
            laser.width = 5

        elif laser.width == 5:
            laser.width = 0
        delay = 0

    laser.update_rect()
    print('witdth:', laser.width)
    # laser.width=10

    gameDisplay.blit(spaceShip, (0, 0))
    pygame.draw.rect(gameDisplay, (255, 0, 0), celing)
    pygame.draw.rect(gameDisplay, (255, 0, 0), floor)
    pygame.draw.rect(gameDisplay, (255, 0, 0), wall_left)
    pygame.draw.rect(gameDisplay, (255, 0, 0), wall_right)
    pygame.draw.rect(gameDisplay, (255, 0, 255), obj11)
    pygame.draw.rect(gameDisplay, (255, 0, 255), obj12)
    pygame.draw.rect(gameDisplay, (255, 0, 255), obj21)
    pygame.draw.rect(gameDisplay, (255, 0, 255), obj22)
    # pygame.draw.rect(gameDisplay, (255, 0, 0), r1)
    dog.collisions = collisions.collision_test(dog.rect, collision_objects_player)
    dog.collison_with_box = collisions.collision_test(dog.rect, collision_objects_box_player)
    box.collisions = collisions.collision_test(box.rect, collision_objects_box)
    box2.collisions = collisions.collision_test(box2.rect, collision_objects_box)

    placeBox.collison = collisions.collision_test(placeBox.rect, collision_interactive)
    open_door.collison = collisions.collision_test(open_door.rect, collision_interactive)

    pygame.draw.rect(gameDisplay, (0, 255, 0), placeBox)
    pygame.draw.rect(gameDisplay, (0, 255, 0), open_door)
    pygame.draw.rect(gameDisplay, (0, 240, 0), laser)

    gameDisplay.blit(dog.getFrame(40, 40, scale), (dog.position.x, dog.position.y))
    gameDisplay.blit(box.getFrame(20, 20, scale), (box.position.x, box.position.y))
    gameDisplay.blit(box2.getFrame(20, 20, scale), (box2.position.x, box2.position.y))
    # pygame.draw.rect(gameDisplay, (255, 255, 0), dog.rect)
    # pygame.draw.rect(gameDisplay, (255, 0, 255), box.rect)
    # print(dog.rect.colliderect(box.rect))
    # print(dog.rect.colliderect(floor))
    # dog.collisions = collisions.collision_test(dog.rect, collision_objects_player)
    # print(dog.collisions)

    # print(floor.rect.top)
    # print(dog.rect.bottom
    dog.update(dt)
    box2.update(dt)  # bug - box which is second/last will move rest of boxes TODO
    box.update(dt)

    placeBox.update_continous()
    open_door.update_press()
    # dog.updateRect()

    pygame.display.update()
