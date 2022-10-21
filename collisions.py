import pygame


def collision_test(rect, tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile) and rect != tile:
            collisions.append(tile)
            # print(tile)
    return collisions


def collison(rect, collisons):
    for collison in collisons:
        # print(rect.rect.bottom - collison.rect.top)
        if abs(rect.rect.left - collison.rect.right) < 11:
            rect.position.x = collison.rect.right
            # if not rect.collison_with_box:
            #     rect.velocity.x = 0
            # print('a')
        if abs(rect.rect.right - collison.rect.left) < 11:
            rect.position.x = collison.rect.left - rect.width
            # if not rect.collison_with_box: # why did I add that ????
            #     rect.velocity.x = 0
            # print('b')
        if abs(rect.rect.bottom - collison.rect.top) < 10:
            rect.frame = 0
            rect.on_ground = True
            rect.position.y = collison.rect.top - rect.heigth
            # print(f'3: {rect.position.y}')
        if abs(rect.rect.top - collison.rect.bottom) < 11:
            rect.position.y = collison.rect.bottom
            # print('c')

def move_collision(player, boxes):

    for collison in boxes:
        if abs(player.rect.left - collison.rect.right) < 11:
            #  =
            collison.position.x -=1
            # player.position.x = collison.rect.right
            collison.velocity.x = player.velocity.x
            # print('what a')
        if abs(player.rect.right - collison.rect.left) < 11:
            collison.position.x +=1
            #  =
            # player.position.x = collison.rect.left - player.width
            collison.velocity.x = player.velocity.x
            # print('what b')
        # if abs(player.rect.bottom - collison.rect.top) < 10:
        #     # player.on_ground = True
        #     # player.position.y = collison.rect.top - player.heigth
        # if abs(player.rect.top - collison.rect.bottom) < 11:
        #     # player.position.y = collison.rect.bottom
        #     print('c')



