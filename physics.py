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
        print(abs(rect.rect.top - collison.rect.bottom))
        if abs(rect.rect.left - collison.rect.right) < 10:
            rect.x = collison.rect.right
        if abs(rect.rect.right - collison.rect.left) < 10:
            rect.x = collison.rect.left - rect.width
        if abs(rect.rect.bottom - collison.rect.top) < 10:
            rect.y = collison.rect.top - rect.heigth
        if abs(rect.rect.top - collison.rect.bottom) < 10:
            rect.y = collison.rect.bottom
