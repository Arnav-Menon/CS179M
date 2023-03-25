# HEAVY HEAVY HEAVY inspo from CS170 8 Puzzle project, linked here:
# https://github.com/Arnav-Menon/CS170/blob/523587237ddec22717e4973c0cd4aa29417ec87c/8puzzle/main.py


import itertools
import heapq as hq
import copy
import time

dummyContainers = {}
containers = []
namesOfContainers = []
visitedStates = []
createdStates = []
exploreStates = []
pathStates = []
visitedPaths = []
createdPaths = []
onOffShipsDone = []
createdOnOffShips = []
maxSize = 1

class Node:
    def __init__(self, balanceMass, shipLayout, parent, names):
        self.shipLayout = shipLayout
        self.balanceMass = balanceMass
        self.leftMass = 0
        self.rightMass = 0
        self.movesToMake = [[], []]
        self.possibleMoves = []
        # default starting pos is first column, top row
        self.cranePos = [12,0]
        self.fn = 0
        self.gn = 0
        self.hn = 0
        # this is which container is held by the crane, if any
        self.containerHeld = []
        self.containerName = ""
        self.namesOfContainers = names
        self.parent = parent
        self.start = []
        self.goal = []
        self.curPos = []
        self.path = []
        self.endCoordinate = []
        self.onload = False

    def exploreOnloadOffload(self, onloads, offloads):
        y, x = self.cranePos

        possibleMoves = [[x-1, y], [x+1, y], [x, y-1], [x, y+1]]
        actualMoves = self.validMoves(possibleMoves, self.shipLayout)

        if len(offloads) > 0:
            startContainer = offloads[0]
        else:
            startContainer = onloads[0]

        self.endCoordinate = [startContainer[1], startContainer[0]]

        for m in actualMoves:
            pass

    def validMoves(self, possibleMoves, shipLayout):
        actualMoves = []
        width, height = len(shipLayout), len(shipLayout[0])
        for m in possibleMoves:
            # if move is within the board and isn't a NAN square
            if 0 <= m[0] < width and 0 <= m[1] < height and shipLayout[m[0]][m[1]] != -1:
                actualMoves.append(m)

        return actualMoves   

    '''
    input: 2 sets of coordinates
    output: manhattan distance between said coordinates
    '''
    def calcDistance(self, x1, y1, x2, y2):
        return (y2-y1) + (x2-x1)

    def calcHN(self, shipLayout, leftMass, rightMass):
        hnCount = 0
        midway = len(shipLayout) // 2
        weightsToMove = shipLayout[0:midway] if leftMass > rightMass else shipLayout[midway:]
        otherSide = shipLayout[midway:] if leftMass > rightMass else shipLayout[0:midway]
        deficit = self.balanceMass - min(leftMass, rightMass)
        weightsToMoveCopy = list(itertools.chain.from_iterable(weightsToMove))

        for w in weightsToMoveCopy:
            if w <= deficit and w > 0:
                deficit -= w
                hnCount += 1

        return hnCount
    
    def index_2d(self, otherList, element):
        for i, x in enumerate(otherList):
            if element in x:
                return (i, x.index(element))
    
    def updateLeftRightWeights(self, nanCounter):
        midway = len(self.shipLayout) // 2

        # calc mass of left side
        for col in self.shipLayout[0:midway]:
            self.leftMass += sum(col)
        self.leftMass += nanCounter // 2

        # calc mass of right side
        for col in self.shipLayout[midway:]:
            self.rightMass += sum(col)
        self.rightMass += nanCounter // 2
    
    # need this wrapper for hq.heappush() call
    def __lt__(self, other):
        return self.fn < other.fn

if __name__ == "__main__":
    
    filename = "ShipCase"
    filetype = ".txt"
    file_num = input("Select number 1-5 for approriate test file: ")

    filename += file_num + filetype
    # filename = "ShipCase4.txt"

    puzzle = Puzzle()
    nanCounter = puzzle.readfile(filename)
    puzzle.formatContainers()
    puzzle.nanCounter = nanCounter
    node = Node(0, containers, None, namesOfContainers)
    node.shipLayout = containers

    # mode = int(input("Would you like to balance the ship or onload/offload? 1 for balance, 2 for onload/offload"))
    mode = 1

    # mode == 1, balance
    if mode == 1:
        puzzle.calcBalanceMass(node)
        puzzle.heavySide = 0 if node.leftMass > node.rightMass else 1

        start = time.time()
        hq.heappush(exploreStates, node)

        depth, moves, names, goalState = puzzle.balance()

        full_paths = puzzle.findPath2(moves, node.shipLayout)
        for i, f in enumerate(full_paths):
            print(f"{names[i]} --> {f}")

        print("Took", depth, "levels to find solution")
        print(f"Took {time.time() - start:.1f} seconds")

    # mode == 2, onload/offload
    else:
        onloads = []
        offloads = []
        on = input("Enter comma separated values for names of containers you would like to LOAD ONTO the ship: ").split(",")
        for x in on:
            onloads.append(x.strip().capitalize())
            
        off = input("Enter comma separated values for names of containers you would like to OFFLOAD from ship: ").split(",")
        for x in off:
            offloads.append(x.strip().capitalize())
        
        actualOnloads = []
        actualOffloads = []

        for key, val in dummyContainers.items():
            if val[1] in onloads:
                actualOnloads.append(key)
            if val[1] in offloads:
                actualOffloads.append(key)

        start = time.time()
        hq.heappush(exploreStates, node)

        puzzle.onloadOffload(actualOnloads, actualOffloads)
