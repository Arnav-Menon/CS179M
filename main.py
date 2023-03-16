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
cranePos = [2, 1]

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

    print(leftMass, rightMass)

    global balanceMass
    balanceMass = (leftMass + rightMass) // 2


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

    return hnCount