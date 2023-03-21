# import numpy as np

containers = {}
balanceMass = 0
# update the weights to be in proper spots after moving them by modulo 6
leftSideWeights = []
rightSideWeights = []

def readfile(filename):

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(", ")
                row, col = map(int, parts[0].strip()[1:-1].split(","))
                weight = int(parts[1].strip()[1:-1])
                # global containers
                containers[row, col] = weight

def calcBalanceMass():
    midway = 6
    leftMass = rightMass = 0

    for key, val in containers.items():
        # check column value to see if mass should be added to left or right side
        if key[1] <= midway:
            leftMass += val
            leftSideWeights.append(val)
        else:
            rightMass += val
            rightSideWeights.append(val)

    global balanceMass
    balanceMass = (leftMass + rightMass) // 2
    # print(leftSideWeights)
    # print(rightSideWeights)

# TODO: stop when BalanceScore = min(left,right)/max(left,right) > 0.9
def calcHN():
    hnCount = 0
    leftMass = sum(leftSideWeights)
    rightMass = sum(rightSideWeights)
    weightsToMove = leftSideWeights if leftMass > rightMass else rightSideWeights
    deficit = balanceMass - min(leftMass, rightMass)
    weightsToMove.sort(reverse=True)

    for w in weightsToMove:
        if w <= deficit and w > 0:
            deficit -= w
            hnCount += 1

    return hnCount

if __name__ == "__main__":
    
    filename = "ShipCase"
    filetype = ".txt"
    file_num = input("Select number 1-5 for approriate test file: ")

    filename += file_num + filetype

    readfile(filename)

    # print(containers)
    calcBalanceMass()

    print("Balance Mass", balanceMass)

    print(calcHN())