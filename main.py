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