import numpy as np

containers = {}
balanceMass = 0

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

def calcBalanceMass(containers):
    midway = 6
    leftMass = rightMass = 0

    # print(containers)
    # print(containers[0])
    for key, val in containers.items():
        # check column value to see if mass should be added to left or right side
        if key[1] <= midway:
            leftMass += val
        else:
            rightMass += val

    global balanceMass
    balanceMass = (leftMass + rightMass) // 2

if __name__ == "__main__":
    
    filename = "ShipCase"
    filetype = ".txt"
    file_num = input("Select number 1-5 for approriate test file: ")

    filename += file_num + filetype

    readfile(filename)

    # print(containers)
    calcBalanceMass(containers)

    print(balanceMass)