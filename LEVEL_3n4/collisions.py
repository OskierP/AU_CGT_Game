# Collisions/Tiles/Physics - Pygame Tutorial: Making a Platformer ep. 3,
# https://www.youtube.com/watch?v=abH2MSBdnWc
def collision_test(rect, tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile) and rect != tile:
            collisions.append(tile)
            # print(tile)
    return collisions


def collision(rect, collisions):
    for collision in collisions:
        if abs(rect.rect.left - collision.rect.right) < 11:
            rect.position.x = collision.rect.right
            rect.velocity.x = 0
        if abs(rect.rect.right - collision.rect.left) < 11:
            rect.position.x = collision.rect.left - rect.width
            rect.velocity.x = 0
        if abs(rect.rect.bottom - collision.rect.top) < 10:
            if not rect.on_ground:
                rect.frame = 0
            rect.on_ground = True
            rect.position.y = collision.rect.top - rect.height + 1
        if abs(rect.rect.top - collision.rect.bottom) < 10:
            rect.position.y = collision.rect.bottom


def move_collision(player, boxes):
    for collision in boxes:
        if abs(player.rect.left - collision.rect.right) < 11:
            collision.position.x -= 1
            collision.velocity.x = player.velocity.x
            player.velocity.x = 0
        if abs(player.rect.right - collision.rect.left) < 11:
            collision.position.x += 1
            collision.velocity.x = player.velocity.x
            player.velocity.x = 0
