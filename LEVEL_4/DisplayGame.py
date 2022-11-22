import pygame.display
class GameDisplay():

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def displayGame(self):
        return pygame.display.set_mode((self.width, self.height))
