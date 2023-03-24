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

    def exploreMoves(self, nanCounter):
        y, x = self.cranePos

        # loop over all columns and have those a possible starting moves
        # then loop over all columns again and see if those are possible moves to drop the container
        possibleMoves = []
        containersToMove = []
        for i in range(0, len(containers)):
            possibleMoves.append([x+i, y])
        
        for m in possibleMoves:
            containerHeld = self.pickupContainer(m, self.shipLayout)
            if containerHeld != None:
                containersToMove.append(containerHeld)

        self.possibleMoves = possibleMoves

        for container in containersToMove:

            for move in self.possibleMoves:
                child = copy.deepcopy(self)

                newNode = Node(self.balanceMass, self.shipLayout, self, child.namesOfContainers)
                newNode.gn = self.gn + 1
                newNode.possibleMoves = self.getDropoffLocs(container, move, self.shipLayout)
                # use this condition for drop off, don't want to drop off in same column
                if container[0] != move[0]:
                    updateMove, newNode.shipLayout = newNode.dropContainer(move, container, child.shipLayout)
                    newNode.updateLeftRightWeights(nanCounter)

                    newNode.hn = self.calcHN(newNode.shipLayout, newNode.leftMass, newNode.rightMass)
                    newNode.fn = newNode.gn + newNode.hn
                    visitedShips = [n.shipLayout for n in visitedStates]

                    #  and newNode.shipLayout not in createdStates
                    if newNode.shipLayout not in visitedShips and newNode.shipLayout not in createdStates:
                        m = list(container)
                        newNode.movesToMake[0] = m
                        newNode.movesToMake[1] = updateMove
                        
                        # update this with container name
                        newNode.containerName = newNode.namesOfContainers[m[0]][m[1]]
                        # update namesOfContainers to reflect updated container pos
                        newNode.namesOfContainers = newNode.updateNamesOfContainers(m, updateMove)
                        
                        hq.heappush(exploreStates, newNode)
                        createdStates.append(newNode.shipLayout)
                        global maxSize
                        maxSize = max(maxSize, len(exploreStates))

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

    def updateNamesOfContainers(self, start, end):
        temp = self.namesOfContainers[end[0]][end[1]]
        self.namesOfContainers[end[0]][end[1]] = self.namesOfContainers[start[0]][start[1]]
        self.namesOfContainers[start[0]][start[1]] = temp
        return self.namesOfContainers

    # drop container into empty spot
    def dropContainer(self, move, containerHeld, shipLayout):
        column = shipLayout[move[0]]
        locToDrop = [-1, -1]

        # find actual row value to drop container
        for i, c in enumerate(column):
            # second condition is so we don't "put" the contianer in an empty position above where it was in the same column
            if c == 0:
                locToDrop[1] = i
                break

        # means no empty spot in this column
        if locToDrop[1] == -1:
            return (locToDrop, shipLayout)
            
        locToDrop[0] = move[0]
        shipLayout[locToDrop[0]][locToDrop[1]] = shipLayout[containerHeld[0]][containerHeld[1]]
        shipLayout[containerHeld[0]][containerHeld[1]] = 0
        return (locToDrop, shipLayout)

    def pickupContainer(self, move, shipLayout):
        column = shipLayout[move[0]]

        for c in column[::-1]:
            if c > 0:
                row = shipLayout[move[0]].index(c)
                return (move[0], row)

    def getDropoffLocs(self, container, move, shipLayout):
        possibleDropOffs = []
        column = shipLayout[move[0] - 1]

        for i, col in enumerate(shipLayout):
            for j, val in enumerate(col):
                if val == 0 and i != container[0]:
                    possibleDropOffs.append([i, j])
                    break

        return possibleDropOffs
    

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


class Puzzle:
    def __init__(self):
        # if 0, left side is heavier
        # if 1, right side is heavier
        self.heavySide = -1
        self.balanceMass = -1
        self.nanCounter = -1

    def readfile(self, filename):
        nanCounter = 0
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(", ")
                    row, col = map(int, parts[0].strip()[1:-1].split(","))
                    row -= 1
                    col -= 1
                    weight = int(parts[1].strip()[1:-1])
                    if parts[-1] == "NAN":
                        dummyContainers[row, col] = [-1, ""]
                        nanCounter += 1
                    else:
                        dummyContainers[row, col] = [weight, parts[-1]]

        return nanCounter

    # change containers from row formation to column formation
    def formatContainers(self):
        keys = list(dummyContainers.keys())
        numRows, numCols = keys[-1][0] + 1, keys[-1][1] + 1
        for i in range(0, numCols):
            j = 0
            temp = []
            names = []
            while j < numRows:
                temp.append(dummyContainers[j, i][0])
                names.append(dummyContainers[j, i][1])
                j += 1
            containers.append(temp)
            namesOfContainers.append(names)

    def calcBalanceMass(self, node):
        midway = len(containers) // 2

        # calc mass of left side
        for col in containers[0:midway]:
            node.leftMass += sum(col)
        node.leftMass += self.nanCounter // 2

        # calc mass of right side
        for col in containers[midway:]:
            node.rightMass += sum(col)
        node.rightMass += self.nanCounter // 2

        node.balanceMass = (node.leftMass + node.rightMass) // 2
        self.balanceMass = node.balanceMass

    def balance(self):

        while len(exploreStates) != 0:
            node = hq.heappop(exploreStates)

            hq.heappush(visitedStates, node)
            
            lowerWeightLimit = int(0.9 * self.balanceMass)
            upperWeightLimit = int(1.1 * self.balanceMass)

            if lowerWeightLimit < node.rightMass < upperWeightLimit and lowerWeightLimit < node.leftMass < upperWeightLimit:
                moves, names = self.printSolution(node)
                return (node.gn, moves, names, node.shipLayout)

            node.exploreMoves(self.nanCounter)

    def onloadOffload(self, onloads, offloads):
        while len(exploreStates) != 0:
            node = hq.heappop(exploreStates)

            hq.heappush(visitedStates, node)

            # if len(onloads) == 0 and len(offloads) == 0:
            # node above one we want to take out is empty
            if node.shipLayout[node.endCoordinate[0]+1][node.endCoordinate[1]] == 0:
                #  done with solution 
                return
            
            node.exploreOnloadOffload(self.nanCounter)

    # inspo for this algorithm comes from Harvard's Intro to AI With Python course, linked below
    # https://cdn.cs50.net/ai/2020/spring/lectures/0/src0/maze.py
    def findPath2(self, moves, shipLayout):
        full_paths = []
        i = 0
        for m in moves:
            temp = []
            startCopy = m[0]
            endCopy = m[1]
            start = m[0]
            end = m[1]
            temp.append(startCopy[:])

            while start != end:
                # go right
                if start[0] < end[0]:
                    test = [start[0] + 1, start[1]]
                    if shipLayout[test[0]][test[1]] == 0:
                        start = test
                    # something in the way, go up and try again
                    else:
                        start[1] += 1
                    
                    temp.append(start[:])
                    continue

                # go left
                elif start[0] > end[0]:
                    test = [start[0] - 1, start[1]]
                    if shipLayout[test[0]][test[1]] == 0:
                        start = test
                    # something in the way, go up and try again
                    else:
                        start[1] += 1
                    
                    temp.append(start[:])
                    continue
                
                # go down
                elif start[1] > end[1]:
                    test = [start[0], start[1] - 1]
                    if shipLayout[test[0]][test[1]] == 0:
                        start = test
                    # something in the way, go down and try again
                    else:
                        start[1] -= 1
                    
                    temp.append(start[:])
                    continue

            full_paths.append(temp)
            # swap containers to update change
            t = shipLayout[startCopy[0]][startCopy[1]]
            shipLayout[startCopy[0]][startCopy[1]] = 0
            shipLayout[endCopy[0]][endCopy[1]] = t

        return full_paths

    def printSolution(self, endNode):
        nodes = []
        movesToMake = []
        namesOfContainers = []

        while endNode.parent:
            nodes.append(endNode)
            endNode = endNode.parent

        nodes = nodes[::-1]
        # print("\t\t", nodes[0].parent.movesToMake)
        for n in nodes:
            movesToMake.append(n.movesToMake)
            namesOfContainers.append(n.containerName)
            newNode = Node(balanceMass=0, shipLayout=n.parent.shipLayout, parent=None, names=[])
            newNode.curPos = n.movesToMake[0]
            newNode.start = n.movesToMake[0]
            newNode.goal = n.movesToMake[1]
            hq.heappush(pathStates, newNode)

        return (movesToMake, namesOfContainers)
    
    def writeOutboundManifest(self, shipName, shipLayout):
        filename = shipName + "_OUTBOUNDManifest.txt"
        f = open(filename, "w")

        for i in range(0, len(shipLayout[0])):
            for j in range(len(shipLayout)):
                weight = shipLayout[j][i]
                f.write(f"[{i+1:02d}, {j+1:02d}], ")
                # NAN cell
                if weight == -1:
                    f.write(f"{{{0:05d}}}, NAN\n")
                # empty cell
                elif weight == 0:
                    f.write(f"{{{0:05d}}}, UNUSED\n")
                else:
                    containerName = ""
                    for val in dummyContainers.values():
                        if val[0] == weight:
                            containerName = val[1]
                            f.write(f"{{{weight:05d}}}, {containerName}\n")
                            break
        f.close()
        return filename, f

if __name__ == "__main__":
    
    filename = "ShipCase"
    filetype = ".txt"
    file_num = input("Select number 1-5 for approriate test file: ")

    shipName = filename + file_num
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
        print("Starting...")
        hq.heappush(exploreStates, node)

        depth, moves, names, goalState = puzzle.balance()

        full_paths = puzzle.findPath2(moves, node.shipLayout)
        for i, f in enumerate(full_paths):
            print(f"\t{names[i]} --> {f}")

        outboundManifestFileName, outboundManifest = puzzle.writeOutboundManifest(shipName, goalState)

        print("Took", depth, "levels to find solution")
        print(f"Took {time.time() - start:.1f} seconds")
        print("Outbound Manifest Printed:", outboundManifestFileName)

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