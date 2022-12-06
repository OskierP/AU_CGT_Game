#Initialise all libraries to do with text 
import pygame
pygame.font.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Specify my font type & size
textfont = pygame.font.SysFont("monospace", 30)

# Create boolean variables 
running = True 

while running:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
    
    # text To Be Displayed
    # 1 is the anti-aliasing, then our colour 
    textTBD = textfont.render(("Level 1"), 1, (255,255,255))

    # Specify the width & height where I want the text to be displayed (x, y) position
    SCREEN.blit(textTBD, (450, 100))

    pygame.display.update()

pygame.display.quit()
pygame.quit()