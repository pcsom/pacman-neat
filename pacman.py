import pygame
from pacUtility import PACMAN_IMG, GRID, getCoordFromGrid, Direction


class Pacman:
    IMG = PACMAN_IMG


    def __init__(self, gridY, gridX):
        self.tick_count = 0     #Keep track when we last jumped
        self.gridX = gridX          #10th column (9 is the index)
        self.gridY = gridY         #12th column (11 is the index)
        self.direction = Direction.RIGHT
        self.ticksSinceLastPellet = 0

    def getPos(self):
        return (self.gridY, self.gridX)


    def moveUp(self):
        if self.gridY > 0 and GRID[self.gridY - 1][self.gridX]:
            self.gridY -= 1
            self.direction = Direction.UP
            return True
        return False

    def moveDown(self):
        if self.gridY < len(GRID) - 1 and GRID[self.gridY + 1][self.gridX]:
            self.gridY += 1
            self.direction = Direction.DOWN
            return True
        return False

    def moveRight(self):
        if self.gridX < len(GRID[0]) - 1 and GRID[self.gridY][self.gridX + 1]:
            self.gridX += 1
            self.direction = Direction.RIGHT
            return True
        return False

    def moveLeft(self):
        if self.gridX > 0 and GRID[self.gridY][self.gridX - 1]:
            self.gridX -= 1
            self.direction = Direction.LEFT
            return True
        return False

    def move(self):
        if self.direction == Direction.UP:
            return self.moveUp()
        elif self.direction == Direction.DOWN:
            return self.moveDown()
        elif self.direction == Direction.LEFT:
            return self.moveLeft()
        elif self.direction == Direction.RIGHT:
            return self.moveRight()

    def turnLeft(self):
        if self.direction == Direction.UP:
            self.direction = Direction.LEFT
        elif self.direction == Direction.DOWN:
            self.direction = Direction.RIGHT
        elif self.direction == Direction.LEFT:
            self.direction = Direction.DOWN
        elif self.direction == Direction.RIGHT:
            self.direction = Direction.UP

    def turnRight(self):
        if self.direction == Direction.UP:
            self.direction = Direction.RIGHT
        elif self.direction == Direction.DOWN:
            self.direction = Direction.LEFT
        elif self.direction == Direction.LEFT:
            self.direction = Direction.UP
        elif self.direction == Direction.RIGHT:
            self.direction = Direction.DOWN

    def turnBack(self):
        if self.direction == Direction.UP:
            self.direction = Direction.DOWN
        elif self.direction == Direction.DOWN:
            self.direction = Direction.UP
        elif self.direction == Direction.LEFT:
            self.direction = Direction.RIGHT
        elif self.direction == Direction.RIGHT:
            self.direction = Direction.LEFT


    def distUp(self):
        curY = self.gridY
        while GRID[curY - 1][self.gridX]:
            curY -= 1
        return abs(self.gridY - curY)

    def distDown(self):
        curY = self.gridY
        while GRID[curY + 1][self.gridX]:
            curY += 1
        return abs(self.gridY - curY)

    def distLeft(self):
        curX = self.gridX
        while GRID[self.gridY][curX - 1]:
            curX -= 1
        return abs(self.gridX - curX)

    def distRight(self):
        curX = self.gridX
        while GRID[self.gridY][curX + 1]:
            curX += 1
        return abs(self.gridX - curX)

    def hasUp(self):
        return int(GRID[self.gridY - 1][self.gridX])
    def hasDown(self):
        return int(GRID[self.gridY + 1][self.gridX])
    def hasLeft(self):
        return int(GRID[self.gridY][self.gridX - 1])
    def hasRight(self):
        return int(GRID[self.gridY][self.gridX + 1])

    def hasRoom(self):
        if self.direction == Direction.UP:
            return self.hasUp()
        elif self.direction == Direction.DOWN:
            return self.hasDown()
        elif self.direction == Direction.LEFT:
            return self.hasLeft()
        elif self.direction == Direction.RIGHT:
            return self.hasRight()


    def draw(self, win):
        win.blit(self.IMG, (getCoordFromGrid(self.gridX), getCoordFromGrid(self.gridY)))       #draw to window


    def get_mask(self):     #used when doing collisions with objects
        return pygame.mask.from_surface(self.IMG)
