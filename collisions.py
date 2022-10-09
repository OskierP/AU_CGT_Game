import pygame


def collision_test(rect, tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile):
            collisions.append(tile)
            print(tile)

    return collisions


def collison(rect, collisons):
    for collison in collisons:
        print(rect.rect.bottom - collison.rect.top)
        if abs(rect.rect.left - collison.rect.right) < 11:
            rect.position.x = collison.rect.right
            print('a')
        if abs(rect.rect.right - collison.rect.left) < 11:
            rect.position.x = collison.rect.left - rect.width
            print('b')
        if abs(rect.rect.bottom - collison.rect.top) < 10:
            rect.frame = 0
            rect.position.y = collison.rect.top - rect.heigth
            print(f'3: {rect.position.y}')
        if abs(rect.rect.top - collison.rect.bottom) < 10:
            rect.position.y = collison.rect.bottom
            print('c')


