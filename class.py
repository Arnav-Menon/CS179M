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
        # TODO: CHANGE THIS TO [12,0] WHEN READY FOR FINAL VERSION
        self.cranePos = [2,0]
        self.fn = 0
        self.gn = 0
        self.hn = 0
        # this is used to evaluate if crane should pick up or drop off container on certain level of search tree
        # defualt is True bc first level is always going to be a pickup of container 
        # self.pickUp = False
        # this is which container is held by the crane, if any
        self.containerHeld = []
        self.containerName = ""
        self.namesOfContainers = names
        self.parent = parent
        self.start = []
        self.goal = []
        self.curPos = []

    def exploreMoves(self, f, nanCounter):
        y, x = self.cranePos

        # print(x, y)
        # loop over all columns and have those a possible starting moves
        # then loop over all columns again and see if those are possible moves to drop the container
        possibleMoves = []
        containersToMove = []
        for i in range(0, len(containers)):
            possibleMoves.append([x+i, y])
        print("possible moves", possibleMoves)
        
        for m in possibleMoves:
            containerHeld = self.pickupContainer(m, self.shipLayout)
            print("\t\t\t", containerHeld)
            if containerHeld != None:
                containersToMove.append(containerHeld)

        self.possibleMoves = possibleMoves
        # possibleMoves = []
        # for move in self.possibleMoves:
            # possibleMoves.append = self.getDropoffLocs(, , self.shipLayout)
        # print(containersToMove)

        f.write("Posssible Moves ")
        f.write(str(possibleMoves))
        f.write("\n")
        f.write(str(self.possibleMoves))
        # print(self.shipLayout)

        for container in containersToMove:
            print("Containers to move", containersToMove)
            # child = copy.deepcopy(self)
            print("Starting with this layout...", self.shipLayout)
            print("Coordinates to container to move:", container)

            #### self.possibleMoves = self.getDropoffLocs
            #### print(self.possibleMoves)

            for move in self.possibleMoves:
                child = copy.deepcopy(self)

                print("\tMOVE", move)
                newNode = Node(self.balanceMass, self.shipLayout, self, child.namesOfContainers)
                newNode.gn = self.gn + 1
                newNode.possibleMoves = self.getDropoffLocs(container, move, self.shipLayout)
                # print(newNode.possibleMoves)
                # use this condition for drop off, don't want to drop off in same column
                if container[0] != move[0]:
                    # print("\t", move)
                    # print("\t", newNode.possibleMoves)
                    print("BEFORE UPDATE...", newNode.shipLayout)
                    # print(move)
                    updateMove, newNode.shipLayout = newNode.dropContainer(move, container, child.shipLayout)
                    # print("AMSWER", answer)
                    # updateMove, newNode.shipLayout = answer[0], answer[1]
                    print("AFTER UPDATE...", newNode.shipLayout)
                    newNode.updateLeftRightWeights(nanCounter)
                    print(newNode.leftMass, newNode.rightMass)

                    newNode.hn = self.calcHN(newNode.shipLayout, newNode.leftMass, newNode.rightMass)
                    newNode.fn = newNode.gn + newNode.hn
                    print("\tFN", newNode.fn, "GN", newNode.gn, "HN", newNode.hn)
                    visitedShips = [n.shipLayout for n in visitedStates]

                    #  and newNode.shipLayout not in createdStates
                    if newNode.shipLayout not in visitedShips and newNode.shipLayout not in createdStates:
                        m = list(container)
                        print("\tPushing this layout...", newNode.shipLayout)
                        print("\t\t\t\t", m, updateMove)
                        print("\t\t\t\t", newNode.namesOfContainers)
                        # print("\t\t\t\t", newNode.namesOfContainers[m[0]][m[1]])
                        newNode.movesToMake[0] = m
                        newNode.movesToMake[1] = updateMove
                        
                        # update this with container name
                        newNode.containerName = newNode.namesOfContainers[m[0]][m[1]]
                        # update namesOfContainers to reflect updated container pos
                        newNode.namesOfContainers = newNode.updateNamesOfContainers(m, updateMove)
                        
                        print(newNode.movesToMake)
                        hq.heappush(exploreStates, newNode)
                        createdStates.append(newNode.shipLayout)
                        global maxSize
                        maxSize = max(maxSize, len(exploreStates))
                        print("MS", maxSize)


                print("----------------")
            print("\n\n\n")

            # return

    def updateNamesOfContainers(self, start, end):
        # print(start, end)
        # print("BEFORE", self.namesOfContainers)
        # print(self.namesOfContainers[start[0]][start[1]])
        temp = self.namesOfContainers[end[0]][end[1]]
        self.namesOfContainers[end[0]][end[1]] = self.namesOfContainers[start[0]][start[1]]
        self.namesOfContainers[start[0]][start[1]] = temp
        # print("AFTER", self.namesOfContainers)
        return self.namesOfContainers

    # drop container into empty spot
    def dropContainer(self, move, containerHeld, shipLayout):
        print("Container Held", containerHeld)
        print("Drop location", move)

        column = shipLayout[move[0]]
        locToDrop = [-1, -1]

        # find actual row value to drop container
        for i, c in enumerate(column):
            # print("\t\t\t\t\t", i, c, move[0])
            # second condition is so we don't "put" the contianer in an empty position above where it was in the same column
            if c == 0:
                locToDrop[1] = i
                break

        # print("\t\t\t\t\tLOC DROP", locToDrop)
        # means no empty spot in this column
        if locToDrop[1] == -1:
            print("...returning -1...")
            return (locToDrop, shipLayout)
            
        locToDrop[0] = move[0]
        # print("LOC DROP", locToDrop)
        # print(locToDrop[0], locToDrop[1])
        # print(shipLayout)
        # print("\t\t\t", shipLayout[locToDrop[0]][locToDrop[1]])
        # print(containerHeld[0], containerHeld[1])
        # print("\t\t\t", shipLayout[containerHeld[0]][containerHeld[1]])
        # print("BEFORE UPDATE", s)
        # temp = 
        shipLayout[locToDrop[0]][locToDrop[1]] = shipLayout[containerHeld[0]][containerHeld[1]]
        shipLayout[containerHeld[0]][containerHeld[1]] = 0
        # print("AFTER UPDATE", s)
        return (locToDrop, shipLayout)

    def pickupContainer(self, move, shipLayout):
        # print(move, shipLayout)
        # print(move)
        # bc values are stored as 1 index
        column = shipLayout[move[0]]
        # print(column)

        for c in column[::-1]:
            # if c != 0:
            if c > 0:
                row = shipLayout[move[0]].index(c)
                # print("\t", move[0] - 1, move[1] - 2)
                # self.containerHeld = shipLayout[move[0] - 1][row]
                return (move[0], row)
                # print("\tCON", self.containerHeld)
                # break

    def getDropoffLocs(self, container, move, shipLayout):
        # print(move, shipLayout)
        possibleDropOffs = []
        column = shipLayout[move[0] - 1]

        for i, col in enumerate(shipLayout):
            # print(col)
            for j, val in enumerate(col):
                # print("\t", i, j, val)
                if val == 0 and i != container[0]:
                    possibleDropOffs.append([i, j])
                    break

        # print("\tPD", possibleDropOffs)
        return possibleDropOffs
    

    '''
    input: 2 sets of coordinates
    output: manhattan distance between said coordinates
    '''
    def calcDistance(self, x1, y1, x2, y2):
        return (y2-y1) + (x2-x1)

    def calcHN(self, shipLayout, leftMass, rightMass):
        # print(self.shipLayout)
        # print(self.balanceMass, self.leftMass, self.rightMass)
        hnCount = 0
        midway = len(shipLayout) // 2
        weightsToMove = shipLayout[0:midway] if leftMass > rightMass else shipLayout[midway:]
        otherSide = shipLayout[midway:] if leftMass > rightMass else shipLayout[0:midway]
        deficit = self.balanceMass - min(leftMass, rightMass)
        weightsToMoveCopy = list(itertools.chain.from_iterable(weightsToMove))

        # print("WeightsToMove", weightsToMove)
        # print("Otherside", otherSide)

        for w in weightsToMoveCopy:
            if w <= deficit and w > 0:
                print("Moving", w)
                # print(self.index_2d(weightsToMove, w))
                # print(self.index_2d(otherSide, 0))
                deficit -= w
                hnCount += 1
                # print("\t\t\t\t\t", deficit)

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
        # size = len(dummyContainers)
        # print(size)
        keys = list(dummyContainers.keys())
        # print(keys)
        numRows, numCols = keys[-1][0] + 1, keys[-1][1] + 1
        # print("NR", numRows, "NC", numCols)
        for i in range(0, numCols):
            j = 0
            temp = []
            names = []
            while j < numRows:
                # print(i, j)
                temp.append(dummyContainers[j, i][0])
                names.append(dummyContainers[j, i][1])
                j += 1
            containers.append(temp)
            namesOfContainers.append(names)

        # print("--------------------------------------------------------")
        # print(containers)

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

        # print(leftMass, rightMass)

        # global balanceMass
        node.balanceMass = (node.leftMass + node.rightMass) // 2
        self.balanceMass = node.balanceMass

    def balance(self):
        f = open("output.txt", "w")

        while len(exploreStates) != 0:
            # print("LENGTH:", len(exploreStates))
            # print(exploreStates)
            node = hq.heappop(exploreStates)

            hq.heappush(visitedStates, node)
            
            lowerWeightLimit = int(0.9 * self.balanceMass)
            upperWeightLimit = int(1.1 * self.balanceMass)

            if lowerWeightLimit < node.rightMass < upperWeightLimit and lowerWeightLimit < node.leftMass < upperWeightLimit:
                f.write("\n\n!!!!!!!!!!!!!!!!DONE WITH SEARCH0!!!!!!!!!!!!!!!!\n")
                f.write(str(node.shipLayout))
                print("!!!!!!!!!!!!!!!!DONE WITH SEARCH0!!!!!!!!!!!!!!!!")
                print(node.shipLayout)
                print(lowerWeightLimit, node.leftMass, node.rightMass, self.balanceMass)
                moves, names = self.printSolution(node)
                return (node.gn, moves, names, node.shipLayout)

            node.exploreMoves(f, self.nanCounter)
            # print("--------------------------------------------------------------------")
            f.write("\n--------------------------------------------------------------------\n\n")

        f.close()

    def onloadOffload(self):
        while len(exploreStates) != 0:
            node = hq.heappop(exploreStates)

            hq.heappush(visitedStates, node)

    def findPath(self, goalState):
        paths = []

        while len(pathStates) != 0:
            node = hq.heappop(pathStates)
            print("\t", node.shipLayout)
            print("\t", node.curPos)
            print("\t", node.start)
            print("\t", node.goal)

            if node.shipLayout == goalState:
                while node.parent:
                    paths.append(node.curPos)
                    node = node.parent

                return paths[::-1]
            
            y, x = node.curPos
            possible_moves = [[y, x-1], [y, x+1], [y-1, x], [y+1, x]]
            # possible_moves = [[x-1, y], [x+1, y], [x, y-1], [x, y+1]]
            actualMoves = self.validMoves(possible_moves, node.shipLayout)
            print(possible_moves)
            print(actualMoves)
            for m in actualMoves:
                # if that position we want to go to isn't blocked by another container
                if node.shipLayout[m[0]][m[1]] == 0:
                    temp = node.shipLayout[node.curPos[0]][node.curPos[1]]
                    node.shipLayout[node.curPos[0]][node.curPos[1]] = node.shipLayout[m[0]][m[1]]
                    node.shipLayout[m[0]][m[1]] = temp
                    print("Before curpos", node.curPos)
                    node.curPos = m
                    print("ShipLayout", node.shipLayout)
                    print("After curpos", node.curPos)

                    if node.shipLayout not in createdPaths:
                        child = Node(balanceMass=node.balanceMass, shipLayout=node.shipLayout, parent=node, names=[])
                        child.curPos = node.curPos
                        hq.heappush(pathStates, child)
                        createdPaths.append(node.shipLayout)

                print("---------")

            hq.heappush(visitedPaths, node)
            print("------------------------------------------------------------")

    def validMoves(self, possibleMoves, shipLayout):
        actualMoves = []
        width, height = len(shipLayout), len(shipLayout[0])
        print(width, height, shipLayout)
        for m in possibleMoves:
            # print(m)
            # if move is within the board and isn't a NAN square
            if 0 <= m[0] < width and 0 <= m[1] < height and shipLayout[m[0]][m[1]] != -1:
                # print("\t\t", m)
                # print(shipLayout[m[0]][m[1]])
                actualMoves.append(m)

        return actualMoves

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
            # print(m)
            # print("\t", start, end)

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
            print("\tadding node to nodes...")
            endNode = endNode.parent

        print("All nodes", len(nodes))
        nodes = nodes[::-1]
        print(nodes[0].parent.shipLayout)
        print("\t", nodes[0].parent.fn, nodes[0].parent.gn, nodes[0].parent.hn)
        # print("\t\t", nodes[0].parent.movesToMake)
        for n in nodes:
            print(n.shipLayout)
            print("\t", n.fn, n.gn, n.hn)
            print("\t\t", n.namesOfContainers)
            movesToMake.append(n.movesToMake)
            namesOfContainers.append(n.containerName)
            newNode = Node(balanceMass=0, shipLayout=n.parent.shipLayout, parent=None, names=[])
            newNode.curPos = n.movesToMake[0]
            newNode.start = n.movesToMake[0]
            newNode.goal = n.movesToMake[1]
            # pathStates.append(newNode)
            hq.heappush(pathStates, newNode)
            # print("\t\t", n.movesToMake)
            # print(n.calcHN(n.shipLayout, n.leftMass, n.rightMass))

        return (movesToMake, namesOfContainers)

if __name__ == "__main__":
    
    # filename = "ShipCase"
    # filetype = ".txt"
    # file_num = input("Select number 1-5 for approriate test file: ")

    # filename += file_num + filetype
    filename = "ShipCase8.txt"

    # node = Node(None)
    puzzle = Puzzle()
    nanCounter = puzzle.readfile(filename)
    puzzle.formatContainers()
    puzzle.nanCounter = nanCounter
    node = Node(0, containers, None, namesOfContainers)
    node.shipLayout = containers
    # node.updateLeftRightWeights()
    # node.hn = node.calcHN(node.shipLayout, node.leftMass, node.rightMass)
    # node.fn = node.gn + node.hn
    # print(dummyContainers)
    # print(containers)
    # print(namesOfContainers)

    # mode = int(input("Would you like to balance the ship or onload/offload? 1 for balance, 2 for onload/offload"))
    mode = 1

    # mode == 1, balance
    if mode == 1:
        puzzle.calcBalanceMass(node)
        puzzle.heavySide = 0 if node.leftMass > node.rightMass else 1
        # print(puzzle.heavySide)
        print("LM", node.leftMass, "RM", node.rightMass)

        # print("H(N):", node.calcHN())
        # node.exploreMoves()

        start = time.time()
        hq.heappush(exploreStates, node)

        depth, moves, names, goalState = puzzle.balance()

        print(node.shipLayout)
        # print(moves)
        # print(names)
        # print(pathStates)
        # time.sleep(1)
        print("\n\n\n")
        full_paths = puzzle.findPath2(moves, node.shipLayout)
        for i, f in enumerate(full_paths):
            print(f"{names[i]} --> {f}")

        print("Took", depth, "levels to find solution")
        print(f"Took {time.time() - start:.1f} seconds")
        print("Max size", maxSize)
        print("GOAL STATE", goalState)

    # mode == 2, onload/offload
    else:
        onloads = []
        offloads = []
        on = input("Enter comma separated values for names of containers you would like to LOAD ONTO the ship: ").split(",")
        for x in on:
            onloads.append(x.strip())
            
        off = input("Enter comma separated values for names of containers you would like to OFFLOAD from ship: ").split(",")
        for x in off:
            offloads.append(x.strip())
        
        print("ON", onloads)
        print("OFF", offloads)

        start = time.time()
        hq.heappush(exploreStates, node)

        puzzle.onloadOffload()