from math import *
from functools import cache
import pygame, sys

pygame.init()

SCREEN = None

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

def start(dim):
    global SCREEN
    SCREEN = pygame.display.set_mode(dim)

def main():
    global SCREEN
    while True:
        SCREEN.fill(BLACK)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    start((400,400))
    main()
