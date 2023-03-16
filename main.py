dummyContainers = {}
containers = []
balanceMass = 0
# update the weights to be in proper spots after moving them by modulo 6
leftSideWeights = []
rightSideWeights = []
movesToMake = []
visitedStates = []
# default starting pos is first column, top row
cranePos = [2, 1]

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
                else:
                    dummyContainers[row, col] = weight

# change containers from row formation to column formation
def formatContainers():
    # print(len(dummyContainers))
    size = len(dummyContainers)
    print(size)
    keys = list(dummyContainers.keys())
    print(keys)
    numRows, numCols = keys[-1][0], keys[-1][1]
    print("NR", numRows, "NC", numCols)
    for i in range(1, numCols+1):
        j = 1
        temp = []
        while j < numRows+1:
            # print(i, j)
            temp.append(dummyContainers[j, i])
            j += 1
        containers.append(temp)

    print("--------------------------------------------------------")
    print(containers)

'''
input: 2 sets of coordinates
output: manhattan distance between said coordinates
'''
def calcDistance(x1, y1, x2, y2):
    return (y2-y1) + (x2-x1)

if __name__ == "__main__":
    
    # filename = "ShipCase"
    # filetype = ".txt"
    # file_num = input("Select number 1-5 for approriate test file: ")

    # filename += file_num + filetype
    filename = "ShipCase1.txt"

    readfile(filename)

    # print(dummyContainers)
    formatContainers()
    exit()
    # exploreMoves()
    calcBalanceMass()

    print("Balance Mass", balanceMass)
