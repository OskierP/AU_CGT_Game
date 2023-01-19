import dog
import pygame
from star import Star
import random


class World:

    def __init__(self):
        self.player = dog.Player()
        self.press = {
            "right": False,
            "left": False
        }

        self.tile_list = []
        self.all_star = pygame.sprite.Group()

    def create_list(self, ):
        img = pygame.image.load("assets/tile.png")

        img_rect = img.get_rect()
        img_rect.x = 7037
        img_rect.y = 2662
        tile = (img, img_rect)
        self.tile_list.append(tile)

        img_rect = img.get_rect()
        img_rect.x = 6537
        img_rect.y = 2362
        tile = (img, img_rect)
        self.tile_list.append(tile)

        img_rect = img.get_rect()
        img_rect.x = 7300
        img_rect.y = 2462
        tile = (img, img_rect)
        self.tile_list.append(tile)

        img_rect = img.get_rect()
        img_rect.x = 7137
        img_rect.y = 2162
        tile = (img, img_rect)
        self.tile_list.append(tile)

        img_rect = img.get_rect()
        img_rect.x = 6337
        img_rect.y = 2162
        tile = (img, img_rect)
        self.tile_list.append(tile)

        img_rect = img.get_rect()
        img_rect.x = 6637
        img_rect.y = 1800
        tile = (img, img_rect)
        self.tile_list.append(tile)

        img_rect = img.get_rect()
        img_rect.x = 6837
        img_rect.y = 1500
        tile = (img, img_rect)
        self.tile_list.append(tile)

        img_rect = img.get_rect()
        img_rect.x = 7137
        img_rect.y = 1200
        tile = (img, img_rect)
        self.tile_list.append(tile)

        img_rect = img.get_rect()
        img_rect.x = 7537
        img_rect.y = 1275
        tile = (img, img_rect)
        self.tile_list.append(tile)

        for i in range(5):
            img_rect = img.get_rect()
            img_rect.x = 7837 + 50 * i
            img_rect.y = 1350 + 75 * i
            tile = (img, img_rect)
            self.tile_list.append(tile)

        for i in range(0, 5):
            img_rect = img.get_rect()
            img_rect.x = 8173 + 150 * i
            img_rect.y = 1680
            tile = (img, img_rect)
            self.tile_list.append(tile)

    def rain_star(self,x,y):
        if random.randint(0, 7)%3 ==0:
            self.all_star.add(Star(x-200,y-500))
        else:
            self.all_star.add(Star(x + 200*random.randint(1,6), y - 700))

    def star_draw(self, screen, camera):
        for star in self.all_star:
            screen.blit(star.image, (star.rect.x - camera.offset.x, star.rect.y - camera.offset.y))

    def draw(self, screen, camera):
        for tile in self.tile_list:
            screen.blit(tile[0], (tile[1].x - camera.offset.x, tile[1].y - camera.offset.y))
