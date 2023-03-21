import itertools

dummyContainers = {}
containers = []
balanceMass = 0
nanCounter = 0
leftMass = 0
rightMass = 0
movesToMake = []
visitedStates = []
# default starting pos is first column, top row
cranePos = [1, 3]

def readfile(filename):
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(", ")
                row, col = map(int, parts[0].strip()[1:-1].split(","))
                weight = int(parts[1].strip()[1:-1])
                if parts[-1] == "NAN":
                    dummyContainers[row, col] = -1
                    global nanCounter
                    nanCounter += 1
                else:
                    dummyContainers[row, col] = weight

# change containers from row formation to column formation
def formatContainers():
    # size = len(dummyContainers)
    # print(size)
    keys = list(dummyContainers.keys())
    # print(keys)
    numRows, numCols = keys[-1][0], keys[-1][1]
    # print("NR", numRows, "NC", numCols)
    for i in range(1, numCols+1):
        j = 1
        temp = []
        while j < numRows+1:
            # print(i, j)
            temp.append(dummyContainers[j, i])
            j += 1
        containers.append(temp)

    # print("--------------------------------------------------------")
    # print(containers)

def calcBalanceMass():
    midway = len(containers) // 2
    global leftMass
    global rightMass

    for col in containers[0:midway]:
        leftMass += sum(col)
    leftMass += nanCounter // 2

    for col in containers[midway:]:
        rightMass += sum(col)
    rightMass += nanCounter // 2

    # print(leftMass, rightMass)

    global balanceMass
    balanceMass = (leftMass + rightMass) // 2

def exploreMoves():
    x, y = cranePos
    print(x, y)
    # loop over all columns and have those a possible starting moves
    # then loop over all columns again and see if those are possible moves to drop the container
    possibleMoves = []
    pass

'''
input: 2 sets of coordinates
output: manhattan distance between said coordinates
'''
def calcDistance(x1, y1, x2, y2):
    return (y2-y1) + (x2-x1)

def calcHN():
    hnCount = 0
    midway = len(containers) // 2
    weightsToMove = containers[0:midway] if leftMass > rightMass else containers[midway:]
    deficit = balanceMass - min(leftMass, rightMass)
    weightsToMove = list(itertools.chain.from_iterable(weightsToMove))

    for w in weightsToMove:
        if w <= deficit and w > 0:
            deficit -= w
            hnCount += 1
            print("\t", deficit)

    return hnCount

if __name__ == "__main__":
    
    # filename = "ShipCase"
    # filetype = ".txt"
    # file_num = input("Select number 1-5 for approriate test file: ")

    # filename += file_num + filetype
    filename = "ShipCase0.txt"

    readfile(filename)

    formatContainers()
    # print(containers)
    # exploreMoves()
    calcBalanceMass()
    # print("LM", leftMass, "RM", rightMass)

    # print("H(N):", calcHN())
    exploreMoves()