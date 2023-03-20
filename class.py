import itertools
import heapq as hq
import copy
import time

dummyContainers = {}
containers = []
visitedStates = []
createdStates = []
exploreStates = []
maxSize = 1

class Node:
    def __init__(self, balanceMass, shipLayout, parent):
        self.shipLayout = shipLayout
        self.balanceMass = balanceMass
        self.leftMass = 0
        self.rightMass = 0
        self.movesToMake = []
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
        self.parent = parent

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
                newNode = Node(self.balanceMass, self.shipLayout, self)
                newNode.gn = self.gn + 1
                newNode.possibleMoves = self.getDropoffLocs(container, move, self.shipLayout)
                # print(newNode.possibleMoves)
                # use this condition for drop off, don't want to drop off in same column
                if container[0] != move[0]:
                    # print("\t", move)
                    # print("\t", newNode.possibleMoves)
                    print("BEFORE UPDATE...", newNode.shipLayout)
                    newNode.shipLayout = newNode.dropContainer(move, container, child.shipLayout)
                    print("AFTER UPDATE...", newNode.shipLayout)
                    newNode.updateLeftRightWeights(nanCounter)
                    print(newNode.leftMass, newNode.rightMass)

                    newNode.hn = self.calcHN(newNode.shipLayout, newNode.leftMass, newNode.rightMass)
                    newNode.fn = newNode.gn + newNode.hn
                    print("\tFN", newNode.fn, "GN", newNode.gn, "HN", newNode.hn)
                    visitedShips = [n.shipLayout for n in visitedStates]

                    #  and newNode.shipLayout not in createdStates
                    if newNode.shipLayout not in visitedShips and newNode.shipLayout not in createdStates:
                        print("\tPushing this layout...", newNode.shipLayout)
                        hq.heappush(exploreStates, newNode)
                        createdStates.append(newNode.shipLayout)
                        global maxSize
                        maxSize = max(maxSize, len(exploreStates))



                print("----------------")
            print("\n\n\n")

            # return

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
            return shipLayout
            
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
        return shipLayout

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

        print("WeightsToMove", weightsToMove)
        print("Otherside", otherSide)

        for w in weightsToMoveCopy:
            if w <= deficit and w > 0:
                print("Moving", w)
                print(self.index_2d(weightsToMove, w))
                print(self.index_2d(otherSide, 0))
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
                        dummyContainers[row, col] = -1
                        nanCounter += 1
                    else:
                        dummyContainers[row, col] = weight

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
            while j < numRows:
                # print(i, j)
                temp.append(dummyContainers[j, i])
                j += 1
            containers.append(temp)

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

    def solve(self):
        f = open("output.txt", "w")

        while len(exploreStates) != 0:
            # print("LENGTH:", len(exploreStates))
            # print(exploreStates)
            node = hq.heappop(exploreStates)

            hq.heappush(visitedStates, node)
            
            lowerWeightLimit = int(0.9 * self.balanceMass)
            upperWeightLimit = int(1.1 * self.balanceMass)

            # left side is heavier
            # if self.heavySide == 0 and node.rightMass >= lowerWeightLimit and node.leftMass <= self.balanceMass:
            #     f.write("\n\n!!!!!!!!!!!!!!!!DONE WITH SEARCH0!!!!!!!!!!!!!!!!\n")
            #     f.write(str(node.shipLayout))
            #     print("!!!!!!!!!!!!!!!!DONE WITH SEARCH0!!!!!!!!!!!!!!!!")
            #     print(node.shipLayout)
            #     print(lowerWeightLimit, node.leftMass, node.rightMass, self.balanceMass)
            #     self.printSolution(node)
            #     return node.gn
            # # right side is heavier
            # elif self.heavySide == 1 and node.leftMass >= lowerWeightLimit and node.rightMass <= self.balanceMass:
            #     f.write("\n\n!!!!!!!!!!!!!!!!DONE WITH SEARCH1!!!!!!!!!!!!!!!!\n")
            #     f.write(str(node.shipLayout))
            #     print("!!!!!!!!!!!!!!!!DONE WITH SEARCH1!!!!!!!!!!!!!!!!")
            #     print(node.shipLayout)
            #     print(lowerWeightLimit, node.leftMass, node.rightMass, self.balanceMass)
            #     self.printSolution()
            #     return node.gn

            if lowerWeightLimit < node.rightMass < upperWeightLimit and lowerWeightLimit < node.leftMass < upperWeightLimit:
                f.write("\n\n!!!!!!!!!!!!!!!!DONE WITH SEARCH0!!!!!!!!!!!!!!!!\n")
                f.write(str(node.shipLayout))
                print("!!!!!!!!!!!!!!!!DONE WITH SEARCH0!!!!!!!!!!!!!!!!")
                print(node.shipLayout)
                print(lowerWeightLimit, node.leftMass, node.rightMass, self.balanceMass)
                self.printSolution(node)
                return node.gn

            node.exploreMoves(f, self.nanCounter)
            # print("--------------------------------------------------------------------")
            f.write("\n--------------------------------------------------------------------\n\n")

        f.close()

    def printSolution(self, endNode):
        nodes = []

        while endNode.parent:
            nodes.append(endNode)
            print("\tadding node to nodes...")
            endNode = endNode.parent

        print("All nodes", len(nodes))
        nodes = nodes[::-1]
        print(nodes[0].parent.shipLayout)
        print("\t", nodes[0].parent.fn, nodes[0].parent.gn, nodes[0].parent.hn)
        for n in nodes:
            print(n.shipLayout)
            print("\t", n.fn, n.gn, n.hn)
            # print(n.calcHN(n.shipLayout, n.leftMass, n.rightMass))

if __name__ == "__main__":
    
    # filename = "ShipCase"
    # filetype = ".txt"
    # file_num = input("Select number 1-5 for approriate test file: ")

    # filename += file_num + filetype
    filename = "ShipCase5.txt"

    # node = Node(None)
    puzzle = Puzzle()
    nanCounter = puzzle.readfile(filename)
    puzzle.formatContainers()
    puzzle.nanCounter = nanCounter
    node = Node(0, containers, None)
    node.shipLayout = containers
    # node.updateLeftRightWeights()
    # node.hn = node.calcHN(node.shipLayout, node.leftMass, node.rightMass)
    # node.fn = node.gn + node.hn
    # print(dummyContainers)
    print(containers)

    puzzle.calcBalanceMass(node)
    puzzle.heavySide = 0 if node.leftMass > node.rightMass else 1
    # print(puzzle.heavySide)
    print("LM", node.leftMass, "RM", node.rightMass)

    # print("H(N):", node.calcHN())
    # node.exploreMoves()

    start = time.time()
    hq.heappush(exploreStates, node)

    depth = puzzle.solve()

    print("Took", depth, "levels to find solution")
    print(f"Took {time.time() - start:.1f} seconds")
    print("Max size", maxSize)
    print(node.shipLayout)
    # print(len(createdStates))
    # for x in createdStates:
        # print(x, "\n")