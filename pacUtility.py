import pygame
import os
from enum import Enum

pygame.font.init()

PACMAN_IMG = pygame.image.load(os.path.join("imgs", "pacman.png"))
GHOST_IMG = pygame.image.load(os.path.join("imgs", "ghost.png"))
BG_IMG = pygame.image.load(os.path.join("imgs", "bg.png"))
STAT_FONT = pygame.font.SysFont("comicsans", 50)
GRID = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
    [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

def getCoordFromGrid(gridVal):
    return gridVal * 36 + 3

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

def getNextInGrid(coord, dir):
    if dir == Direction.UP:
        return (coord[0] - 1, coord[1])
    elif dir == Direction.DOWN:
        return (coord[0] + 1, coord[1])
    elif dir == Direction.LEFT:
        return (coord[0], coord[1] - 1)
    elif dir == Direction.RIGHT:
        return (coord[0], coord[1] + 1)
    
def onGrid(coord):
    return GRID[coord[0]][coord[1]]
    
rowDiffs = [0, -1, 1, -2, 2]
colDiffs = [0, -1, 1, -2, 2, -3, 3]
def findClosestValidCoord(coord):
    if not GRID[coord[0]][coord[1]]:
        for rowDiff in rowDiffs:
            for colDiff in colDiffs:
                if (0 < coord[0] + rowDiff < len(GRID) - 1) and (0 < coord[1] + colDiff < len(GRID[0]) - 1) and GRID[coord[0] + rowDiff][coord[1] + colDiff]:
                    return (coord[0] + rowDiff, coord[1] + colDiff)
    return coord

def moveOnGrid(direction, coord):
    if direction == Direction.UP:
        return (coord[0] - 1, coord[1])
    elif direction == Direction.DOWN:
        return (coord[0] + 1, coord[1])
    elif direction == Direction.LEFT:
        return (coord[0], coord[1] - 1)
    elif direction == Direction.RIGHT:
        return (coord[0], coord[1] + 1)
    
def isIntersection(coord):
    outlets = 0
    if GRID[coord[0] - 1][coord[1]]:
        outlets += 1
    if GRID[coord[0] + 1][coord[1]]:
        outlets += 1
    if GRID[coord[0]][coord[1] - 1]:
        outlets += 1
    if GRID[coord[0]][coord[1] + 1]:
        outlets += 1

    return outlets > 2

def isCorner(coord):        #doesnt check if the outlets are linear (i.e. not at a bend); that must be checked prior to calling this func
    outlets = 0
    if GRID[coord[0] - 1][coord[1]]:
        outlets += 1
    if GRID[coord[0] + 1][coord[1]]:
        outlets += 1
    if GRID[coord[0]][coord[1] - 1]:
        outlets += 1
    if GRID[coord[0]][coord[1] + 1]:
        outlets += 1

    return outlets == 2

def getReverseDir(curDir):
    if curDir == Direction.UP:
        return Direction.DOWN
    if curDir == Direction.DOWN:
        return Direction.UP
    if curDir == Direction.LEFT:
        return Direction.RIGHT
    if curDir == Direction.RIGHT:
        return Direction.LEFT

def turnCorner(prevCoord, reachedWithDir):      #Return newDirection, nextCoord
    possibDirs = []

    if GRID[prevCoord[0] - 1][prevCoord[1]]:
        possibDirs.append(Direction.UP)
    if GRID[prevCoord[0] + 1][prevCoord[1]]:
        possibDirs.append(Direction.DOWN)
    if GRID[prevCoord[0]][prevCoord[1] - 1]:
        possibDirs.append(Direction.LEFT)
    if GRID[prevCoord[0]][prevCoord[1] + 1]:
        possibDirs.append(Direction.RIGHT)

    if possibDirs[0] != getReverseDir(reachedWithDir):
        # return (possibDirs[0], moveOnGrid(possibDirs[0], prevCoord))
        return possibDirs[0]
    else:
        # return (possibDirs[1], moveOnGrid(possibDirs[1], prevCoord))
        return possibDirs[1]