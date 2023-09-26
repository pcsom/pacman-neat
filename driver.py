import pygame
import neat
import time
import os
import random
import heapq
import copy
pygame.font.init()

WIN_WIDTH = 685
WIN_HEIGHT = 757
GEN = 0

from ghosts import Inky, Blinky, Pinky, Clyde
from pacman import Pacman
from pacUtility import BG_IMG, STAT_FONT, Direction, moveOnGrid, isIntersection, isCorner, turnCorner, onGrid
from pellet import Pellet

PACMAN_IMG = pygame.image.load(os.path.join("imgs", "pacman.png"))
GHOST_IMG = pygame.image.load(os.path.join("imgs", "ghost.png"))
BG_IMG = pygame.image.load(os.path.join("imgs", "bg.png"))
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




gridPoses = []
for y, row in enumerate(GRID):
    for x, col in enumerate(row):
        if col:
            gridPoses.append((y, x))


def draw_window(win, pacmans, blinkys, pinkys, inkys, clydes, pelletGroups, score, gen):
    win.blit(BG_IMG, (0,0))     #draw bg using top left corner coords
    for pacman in pacmans:
        pacman.draw(win)
    for ghost in blinkys:
        ghost.draw(win)
    for ghost in pinkys:
        ghost.draw(win)
    for ghost in inkys:
        ghost.draw(win)
    for ghost in clydes:
        ghost.draw(win)
    for pellets in pelletGroups:
        for key in pellets:
            pellets[key].draw(win)
    text = STAT_FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
    win.blit(text, (10, 10))

    text = STAT_FONT.render("Score: " + str(round(score, 1)), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    pygame.display.update()


def main(genomes, config):     #runs main loop of game
    global GEN
    global gridPoses
    GEN += 1

    nets = []       #keep track of neural network for each bird
    ge = []         #keep track of genome per bird (change its fitness)
    pacmans = []      #list of bird objects
    blinkys = []
    pinkys = []
    inkys = []
    clydes = []
    pelletGroups = []
    pelletAts = []

    for _, g in genomes:        #genomes has genomeID and genome object (its a tuple)
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)

        pacPlace = gridPoses[random.randint(0, len(gridPoses) - 1)]
        ghostPlaces = []
        ghostPlace = None
        if GRID[pacPlace[0] - 1][pacPlace[1]]:
            ghostPlaces.append((pacPlace[0] - 1, pacPlace[1]))
        if GRID[pacPlace[0] + 1][pacPlace[1]]:
            ghostPlaces.append((pacPlace[0] + 1, pacPlace[1]))
        if GRID[pacPlace[0]][pacPlace[1] - 1]:
            ghostPlaces.append((pacPlace[0], pacPlace[1] - 1))
        if GRID[pacPlace[0]][pacPlace[1] + 1]:
            ghostPlaces.append((pacPlace[0], pacPlace[1] + 1))
        if len(ghostPlaces) == 1:
            ghostPlace = ghostPlaces[0]
        else:
            try:
                ghostPlace = ghostPlaces[random.randint(0, len(ghostPlaces) - 1)]
            except Exception:
                print(GRID)
                print(ghostPlaces)
                print(Exception)

        pacmans.append(Pacman(pacPlace[0], pacPlace[1]))
        blinkys.append(Blinky(ghostPlace[0], ghostPlace[1], pacmans[-1]))
        pinkys.append(Pinky(ghostPlace[0], ghostPlace[1], pacmans[-1]))
        inkys.append(Inky(ghostPlace[0], ghostPlace[1], pacmans[-1], blinkys[-1], pinkys[-1]))
        clydes.append(Clyde(ghostPlace[0], ghostPlace[1], pacmans[-1]))
        pellets = {}                    #177 pellets
        pelletAt = copy.deepcopy(GRID)
        for y, row in enumerate(pelletAt):
            for x, col in enumerate(row):
                if col:
                    pellets[(y, x)] = Pellet(y, x)
        pelletGroups.append(pellets)
        pelletAts.append(pelletAt)
        g.fitness = 0
        ge.append(g)


    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))  #init game window
    clock = pygame.time.Clock()
    run = True
    score = 0
    ctr = 0

    while run:
        clock.tick(30)      #run at most 30 ticks per second
        for event in pygame.event.get():        #keeps track of user events (run mouse, button, etc)
            if event.type == pygame.QUIT:       #if clicked red x on window
                run = False

        if not len(pacmans):
            run = False
            break

        score = max(g.fitness for g in ge)

        for x, pacman in enumerate(pacmans):
            # ge[x].fitness += 0.1
            pacman.ticksSinceLastPellet += 1

            #calculate ghost danger in each direction
            ghostPoses = [(blinkys[x].gridY, blinkys[x].gridX), (pinkys[x].gridY, pinkys[x].gridX), (inkys[x].gridY, inkys[x].gridX), (clydes[x].gridY, clydes[x].gridX)]
            totalInput = [0 for i in range(12)]
            dirCtr = 0
            for direction in Direction:
                newY, newX = pacman.getPos()
                prevY, prevX = newY, newX
                hitGhost = False
                hitIntersection = False
                distanceTravelled = 0
                curDir = direction
                while True:
                    while GRID[newY][newX] and not hitGhost and not hitIntersection:
                        prevY, prevX = newY, newX
                        newY, newX = moveOnGrid(curDir, (newY, newX))
                        distanceTravelled += 1
                        if (newY, newX) in ghostPoses:
                            hitGhost = True

                        if GRID[newY][newX] and isIntersection((newY, newX)):
                            hitIntersection = True
                    #we're at a wall, intersection, or ghost
                    if hitGhost:
                        totalInput[dirCtr] = 1/distanceTravelled
                        break
                    elif hitIntersection:
                        totalInput[dirCtr] = 0
                        break
                    else:       #at a corner!
                        curDir = turnCorner((prevY, prevX), curDir)
                        distanceTravelled -= 1
                        newY, newX = prevY, prevX
                dirCtr += 1
            
            #set input for if there's a wall in that direction
            dirCtr = 4
            for direction in Direction:
                totalInput[dirCtr] = onGrid(moveOnGrid(direction, pacman.getPos()))
                dirCtr += 1

            dirCtr = 8
            for direction in Direction:
                newY, newX = moveOnGrid(direction, pacman.getPos())
                while True:
                    if not GRID[newY][newX]:
                        totalInput[dirCtr] = 0
                        break
                    if pelletAts[x][newY][newX]:
                        totalInput[dirCtr] = 1
                        break

                    newY, newX = moveOnGrid(direction, (newY, newX))
                dirCtr += 1



            #print(totalInput)
            neatOutput = nets[x].activate(tuple(totalInput))
            movement = False
            if neatOutput[0] > 0.5:         #DO movement based on outputs (4)
                movement = pacman.moveUp()
            elif neatOutput[1] > 0.5:
                movement = pacman.moveDown()
            elif neatOutput[2] > 0.5:
                movement = pacman.moveLeft()
            elif neatOutput[3] > 0.5:
                movement = pacman.moveRight()


            if movement:        #Update ghost pathing if pacman moved, and see if pacman ate a new pellet
                blinkys[x].updatePath(pacman)
                pinkys[x].updatePath(pacman)
                inkys[x].updatePath(blinkys[x], pinkys[x])
                clydes[x].updatePath(pacman)
                if pelletAts[x][pacman.gridY][pacman.gridX]:
                    ge[x].fitness += 1
                    pelletAts[x][pacman.gridY][pacman.gridX] = 0
                    del pelletGroups[x][(pacman.gridY, pacman.gridX)]
                    pacman.ticksSinceLastPellet = 0


            # ghostCloser = ghosts[x].prevPathLen > len(ghosts[x].path)
            # if movement and not ghostCloser:
            #     ge[x].fitness += 2
            # elif not movement:
            #     ge[x].fitness -= 0.5


        if ctr % 3 == 0:        #move ghost every 3 iterations of loop
            ctr = 0
            for blinky in blinkys:
                blinky.move()
            for pinky in pinkys:
                pinky.move()
            for inky in inkys:
                inky.move()
            for clyde in clydes:
                clyde.move(pacman)

        remInds = []        #remove pacman its related entities if it dies (mark the index for removal at this point)
        for x in range(len(pacmans)):
            rem = False
            if blinkys[x].collide(pacmans[x]):
                ge[x].fitness -= 10
                rem = True
            elif pinkys[x].collide(pacmans[x]):
                ge[x].fitness -= 10
                rem = True
            elif inkys[x].collide(pacmans[x]):
                ge[x].fitness -= 10
                rem = True
            elif clydes[x].collide(pacmans[x]):
                ge[x].fitness -= 10
                rem = True
            elif pacman.ticksSinceLastPellet == 180:
                ge[x].fitness -= 10
                rem = True

            if rem:
                remInds.append(x)

        for ind in remInds[::-1]:       #the actual removal
            blinkys.pop(ind)
            pinkys.pop(ind)
            inkys.pop(ind)
            clydes.pop(ind)
            pacmans.pop(ind)
            pelletAts.pop(ind)
            pelletGroups.pop(ind)
            ge.pop(ind)
            nets.pop(ind)


        draw_window(win, pacmans, blinkys, pinkys, inkys, clydes, pelletGroups, score, GEN)

        if ctr == 90:       #swap ghosts between chase and scatter modes
            for ghost in blinkys:
                ghost.scatter = True
            for ghost in pinkys:
                ghost.scatter = True
            for ghost in inkys:
                ghost.scatter = True
            for ghost in clydes:
                ghost.scatter = True
        elif ctr == 120:
            ctr = 0
            for ghost in blinkys:
                ghost.scatter = False
            for ghost in pinkys:
                ghost.scatter = False
            for ghost in inkys:
                ghost.scatter = False
            for ghost in clydes:
                ghost.scatter = False

        ctr += 1

        if score >= 177:
            run = False
            break




def run(config_path):
    #instantiate configurations
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)     #generate a population

    #gives stats as running
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(100, None, "/content/drive/MyDrive/PacmanSaves/neat-checkpoint-"))


    #run main as the fitness function, 50 times (for 50 generations)
    #need give main params of genomes, config
    winner = p.run(main, 10000)


if __name__ == "__main__":
    #local_dir = os.path.dirname(__file__)       #path to dir we're in rn
    #config_path = os.path.join(local_dir, "config-feedforward.txt")
    config_path = "aiProg/config-feedforward-4game.txt"
    run(config_path)