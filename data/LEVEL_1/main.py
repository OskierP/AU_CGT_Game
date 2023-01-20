
import time

import data.LEVEL_3n4.restart_page
from data import flags
import data.progress.save_progress
from data.LEVEL_1.camera import *
import data.LEVEL_1.game as game_module

def level1():
    pygame.init()

    clock = pygame.time.Clock()
    fps = 60
    '''''LOADING OF THE WORLD'''''
    # World
    game = game_module.World()

    # Windows
    pygame.display.set_caption("MARTIAN MISSION- level 1")
    DISPLAY_W, DISPLAY_H = 1100, 600
    canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
    screen = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
    running = True
    background = pygame.image.load('data/LEVEL_1/assets/all2.png').convert()
    burn = pygame.transform.scale(pygame.image.load("data/LEVEL_1/assets/esc.png"), (800,800))
    tuto = pygame.transform.scale(pygame.image.load("data/LEVEL_1/assets/tuto.png"), (800,800))
    burn_showed = False
    '''''LOADING OF THE CAMERA'''''
    camera = Camera(game.player)
    follow = Follow(camera, game.player)
    border = Border(camera, game.player)
    auto = Auto(camera, game.player)
    camera.setmethod(follow)

    # create plateform
    game.create_list()

    timer_star = 0
    while running:

        clock.tick(fps)


        # Check Mouvements
        if pygame.event.get(pygame.QUIT):
            running = False
            flags.next_lvl_1.set_flag(True)
        # Jump
        if game.press.get(pygame.K_UP) and game.player.jumping == False:
            game.player.jump()

        # Move right/left
        game.player.velocity = 0
        if game.press.get(pygame.K_RIGHT) and game.player.rect.x < 8500:
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
            if tile[1].colliderect(game.player.rect.x + 315 + game.player.velocity, game.player.rect.y - 100,
                                   game.player.width, game.player.height):
                game.player.velocity = 0
            # Check y
            if tile[1].colliderect(game.player.rect.x + 315, game.player.rect.y - game.player.jumpingVelocity - 100,
                                   game.player.width, game.player.height):
                if game.player.jumpingVelocity > 0:
                    game.player.rect.y += tile[1].bottom - game.player.rect.top + 100
                    game.player.jumpingVelocity = 0
                elif game.player.jumpingVelocity <= 0:
                    game.player.rect.y += tile[1].top - game.player.rect.bottom + 100
                    game.player.jumpingVelocity = 0
                    game.player.jumping = False

        for star in game.all_star:
            if star.rect.colliderect(game.player.rect.x + 315, game.player.rect.y - game.player.jumpingVelocity - 100, game.player.width/2,
                                     game.player.height/2):

                data.LEVEL_3n4.restart_page.restart()
                game.player.rect.x = 2920
                game.player.rect.y = 2985

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
                pygame.quit()
                print("Game ended")

            # Mouvements
            elif event.type == pygame.KEYDOWN:
                game.press[event.key] = True
            elif event.type == pygame.KEYUP:
                game.press[event.key] = False

        # Stars

        dt = clock.tick()
        timer_star += dt

        if timer_star > 6 and game.player.rect.x > 3200:
            timer_star = 0
            game.rain_star(game.player.rect.x, game.player.rect.y)

        for star in game.all_star:
            star.fall()

        # Update

        # if walking in any direction, increase frame
        if game.player.jumping:
            if game.player.facingRight:
                game.player.image = game.player.spritesJumpRight
            else:
                game.player.image = game.player.spritesJumpLeft
        elif (game.player.walkAnimationLeft or game.player.walkAnimationRight):
            game.player.walkFrame = (game.player.walkFrame + 1) % 20  # %20 because we have 5 frames * 4 ticks each
        else:
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

        if game.player.rect.x > 2800 and burn_showed == False:
            time_start = time.time()
            canvas.blit(background, (0 - camera.offset.x, 0 - camera.offset.y))
            canvas.blit(game.player.image,
                        (game.player.rect.x - camera.offset.x + 315, game.player.rect.y - camera.offset.y - 100))
            canvas.blit(burn, (game.player.rect.x - camera.offset.x , game.player.rect.y - camera.offset.y - 600))
            game.draw(canvas, camera)
            game.star_draw(canvas, camera)
            screen.blit(canvas, (0, 0))
            pygame.display.update()
            burn_showed = True
            while time.time() - time_start < 4:
                continue

        else:
            canvas.blit(background, (0 - camera.offset.x, 0 - camera.offset.y))
            canvas.blit(tuto, (1875 - camera.offset.x, 3000 - camera.offset.y - 475))
            canvas.blit(game.player.image,
                        (game.player.rect.x - camera.offset.x + 315, game.player.rect.y - camera.offset.y - 100))
            game.draw(canvas, camera)
            game.star_draw(canvas, camera)
            screen.blit(canvas, (0, 0))
            pygame.display.update()

        if 1755 > game.player.rect.y > 1250 and game.player.rect.x > 8475:
            running = False
            flags.next_lvl_1.set_flag(True)
            data.progress.save_progress.update_progress('Level_2', True)