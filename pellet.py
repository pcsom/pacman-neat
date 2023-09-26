import pygame
import neat
import time
import os
import random
import heapq
pygame.font.init()

WIN_WIDTH = 685
WIN_HEIGHT = 757

PELLET_IMG = pygame.image.load(os.path.join("imgs", "pellet.png"))

from search import dijkstra, aStar

class Pellet:
    IMG = PELLET_IMG

    def __init__(self, gridY, gridX):
        self.gridX = gridX
        self.gridY = gridY

    def draw(self, win):
        win.blit(self.IMG, (36*self.gridX + 16, 36*self.gridY + 16))       #draw to window

    def collide(self, pacman):
        if pacman.gridY == self.gridY and pacman.gridX == self.gridX:
            return True

        return False

