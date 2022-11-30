import pygame

# import LEVEL_1.game
import flags
import LEVEL_1.game as Game
# from game import *
import LEVEL_1.dog as Dog
import LEVEL_1.camera as Camera

def level_1():
    pygame.init()

    clock = pygame.time.Clock()
    fps = 60
    '''''LOADING OF THE WORLD'''''
    # World
    # game = World()
    game = Game.World()

    # Windows
    pygame.display.set_caption("level1")
    DISPLAY_W, DISPLAY_H = 1100, 600
    canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
    screen = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
    running = True
    background = pygame.image.load('LEVEL_1/assets/all1.png').convert()
    '''
    screen.blit(background, (0,0))
    screen.blit(game.player.image,game.player.rect)
    pygame.display.flip()
    '''
    '''''LOADING OF THE CAMERA'''''
    camera = Camera.Camera(game.player)
    follow = Camera.Follow(camera, game.player)
    border = Camera.Border(camera, game.player)
    auto = Camera.Auto(camera, game.player)
    camera.setmethod(follow)

    print(game.tile_list)

    # create plateform
    game.create_list()

    while running:

        clock.tick(fps)
        '''
        screen.blit(background, (0,0))
        screen.blit(game.player.image,game.player.rect)
        pygame.display.flip()
        '''

        # Check Mouvements

        # Jump
        if game.press.get(pygame.K_UP) and game.player.jumping == False:
            game.player.jump()
            print(game.player.jumpingVelocity)
            '''
        if game.press.get(pygame.K_UP) == False:
            game.player.jumping = False
            '''

            # Move right/left
        game.player.velocity = 0
        if game.press.get(pygame.K_RIGHT) and game.player.rect.x < 8000:
            game.player.velocity = 10
        else:
            game.player.walkAnimationRight = False

        if game.press.get(pygame.K_LEFT) and game.player.rect.x > 0:
            game.player.velocity = -10
        else:
            game.player.walkAnimationLeft = False

        # Gravity
        game.player.gravity()

        # Collision
        for tile in game.tile_list:
            # Check x
            if tile[1].colliderect(game.player.rect.x + 315 + game.player.velocity, game.player.rect.y - 100, game.player.width, game.player.height):
                game.player.velocity = 0
            # Check y
            if tile[1].colliderect(game.player.rect.x + 315, game.player.rect.y - game.player.jumpingVelocity - 100, game.player.width, game.player.height):
                if game.player.jumpingVelocity > 0:
                    game.player.rect.y += tile[1].bottom - game.player.rect.top + 100
                    game.player.jumpingVelocity = 0
                elif game.player.jumpingVelocity <= 0:
                    game.player.rect.y += tile[1].top - game.player.rect.bottom + 100
                    game.player.jumpingVelocity = 0
                    game.player.jumping = False

        # Update Player

        game.player.rect.y -= game.player.jumpingVelocity

        if game.player.velocity > 0:
            game.player.move_right()
        if game.player.velocity < 0:
            game.player.move_left()

        if game.player.rect.bottom > 2985 + game.player.height:
            game.player.rect.bottom = 2985 + game.player.height
            game.player.jumping = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # pygame.quit()
                flags.next_lvl_1.set_flag(True)
                print("Game ended")

            # Mouvements
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    camera.setmethod(follow)
                elif event.key == pygame.K_2:
                    camera.setmethod(auto)
                elif event.key == pygame.K_3:
                    camera.setmethod(border)
                else:
                    game.press[event.key] = True
            elif event.type == pygame.KEYUP:
                game.press[event.key] = False



        # Update

        # if walking in any direction, increase frame
        if game.player.jumping :
            if game.player.facingRight:
                game.player.image = game.player.spritesJumpRight
            else:
                game.player.image = game.player.spritesJumpLeft
        elif (game.player.walkAnimationLeft or game.player.walkAnimationRight):
            game.player.walkFrame = (game.player.walkFrame + 1) % 20 # %20 because we have 5 frames * 4 ticks each
        else :
            if game.player.facingRight:
                game.player.image = game.player.spritesWalkRight[0]
            else:
                game.player.image = game.player.spritesWalkLeft[0]


        # set current sprite
        if (game.player.walkAnimationLeft):
            game.player.image = game.player.spritesWalkLeft[game.player.walkFrame // 4]  # //4 because update every 4 ticks
        elif (game.player.walkAnimationRight):
            game.player.image = game.player.spritesWalkRight[game.player.walkFrame // 4]  # //4 because update every 4 ticks

        camera.scroll()

        canvas.blit(background, (0 - camera.offset.x, 0 - camera.offset.y))
        canvas.blit(game.player.image, (game.player.rect.x - camera.offset.x + 315, game.player.rect.y - camera.offset.y - 100))
        game.draw(canvas, camera)
        screen.blit(canvas, (0, 0))

        pygame.display.update()
        print(game.player.jumpingVelocity)
