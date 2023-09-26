import pygame
import neat
import time
import os
import random
import heapq
pygame.font.init()

WIN_WIDTH = 685
WIN_HEIGHT = 757

from pacUtility import getCoordFromGrid, getNextInGrid, GRID, findClosestValidCoord, onGrid
GHOST_IMG = pygame.image.load(os.path.join("imgs", "ghost.png"))

from search import dijkstra, aStar

class Ghost:
    IMG = GHOST_IMG

    def __init__(self, gridY, gridX, pacman, searchFunc):
        self.gridX = gridX
        self.gridY = gridY
        self.searchFunc = searchFunc
        self.path = self.searchFunc((self.gridY, self.gridX), (pacman.gridY, pacman.gridX))        #give dijkstra the row, then col
        self.curPathInd = 0
        self.prevPathLen = len(self.path)
        self.scatter = False

    # def updatePath(self, pacman):
    #     self.prevPathLen = len(self.path)
    #     self.path = self.searchFunc((self.gridY, self.gridX), self.targetFunc())
    #     self.curPathInd = 0

    def move(self):
        # if not random.randint(0,5):
        #     prevPos = (self.gridY, self.gridX)
        #     if GRID[self.gridY - 1][self.gridX]:
        #         self.gridY -= 1
        #     elif GRID[self.gridY + 1][self.gridX]:
        #         self.gridY += 1
        #     elif GRID[self.gridY][self.gridX - 1]:
        #         self.gridX -= 1
        #     elif GRID[self.gridY][self.gridX + 1]:
        #         self.gridX += 1
        #     self.path.insert(self.curPathInd + 1, prevPos)
        if self.curPathInd < len(self.path) - 1:
            self.curPathInd += 1
        self.gridY = self.path[self.curPathInd][0]      #dijkstra returns row, then col
        self.gridX = self.path[self.curPathInd][1]


    def draw(self, win):
        win.blit(self.IMG, (getCoordFromGrid(self.gridX), getCoordFromGrid(self.gridY)))       #draw to window

    def collide(self, pacman):
        if pacman.gridY == self.gridY and pacman.gridX == self.gridX:
            return True

        return False


class Blinky(Ghost):
    def __init__(self, gridY, gridX, pacman):
        super().__init__(gridY, gridX, pacman, aStar)
        self.path = self.searchFunc((self.gridY, self.gridX), (pacman.gridY, pacman.gridX))

    def updatePath(self, pacman):
        self.prevPathLen = len(self.path)
        if self.scatter:
            self.path = self.searchFunc((self.gridY, self.gridX), (1, len(GRID[0]) - 2))
        else:
            self.path = self.searchFunc((self.gridY, self.gridX), (pacman.gridY, pacman.gridX))
        self.curPathInd = 0

class Pinky(Ghost):
    def __init__(self, gridY, gridX, pacman):
        super().__init__(gridY, gridX, pacman, aStar)
        self.path = self.getPath(pacman)
        self.target = self.path[-1]

    def getPath(self, pacman):
        if self.scatter:
            target = (1, 1)
        else:
            i = 0
            target = pacman.getPos()
            while onGrid(getNextInGrid(target, pacman.direction)) and i < 2:
                target = getNextInGrid(target, pacman.direction)
                i += 1
        self.target = target
        return self.searchFunc((self.gridY, self.gridX), target)

    def updatePath(self, pacman):
        self.prevPathLen = len(self.path)
        self.path = self.getPath(pacman)
        
        self.curPathInd = 0


class Inky(Ghost):
    def __init__(self, gridY, gridX, pacman, blinky, pinky):
        super().__init__(gridY, gridX, pacman, dijkstra)
        self.path = self.getPath(blinky, pinky)
        self.target = self.path[-1]
    
    def getPath(self, blinky, pinky):
        if self.scatter:
            target = (len(GRID) - 2, len(GRID[0]) - 2)
        else:
            targetRow = max(1, min(len(GRID) - 2, pinky.target[0]*2 - blinky.gridY))
            targetCol = max(1, min(len(GRID[0]) - 2, pinky.target[1]*2 - blinky.gridX))
            target = findClosestValidCoord((targetRow, targetCol))
        self.target = target

        return self.searchFunc((self.gridY, self.gridX), target)


    def updatePath(self, blinky, pinky):
        self.prevPathLen = len(self.path)
        self.path = self.getPath(blinky, pinky)
        
        self.curPathInd = 0


class Clyde(Ghost):
    def __init__(self, gridY, gridX, pacman):
        super().__init__(gridY, gridX, pacman, dijkstra)
        self.targetPacman = True
        self.path = self.searchFunc((self.gridY, self.gridX), (pacman.gridY, pacman.gridX))
        self.target = self.path[-1]
    
    def getPath(self, pacman):
        if self.scatter:
            return self.searchFunc((self.gridY, self.gridX), (len(GRID) - 2, 1))
        else:
            pathToPacman = self.searchFunc((self.gridY, self.gridX), (pacman.gridY, pacman.gridX))
            if len(self.path) <= 5 and self.targetPacman:
                self.targetPacman = False
            elif len(pathToPacman) > 5 and not self.targetPacman:
                self.targetPacman = True

            if self.targetPacman:
                return pathToPacman
            else:
                return self.searchFunc((self.gridY, self.gridX), (len(GRID) - 2, 1))
        

    def updatePath(self, pacman):
        self.prevPathLen = len(self.path)
        self.path = self.getPath(pacman)
        
        self.curPathInd = 0

    def move(self, pacman):
        self.updatePath(pacman)
        super().move()

