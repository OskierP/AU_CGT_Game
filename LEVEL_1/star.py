import pygame


class Star(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/star.png"), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.velocity = 7

    def fall(self):
        self.rect.y += self.velocity
        self.rect.x += self.velocity / 2
