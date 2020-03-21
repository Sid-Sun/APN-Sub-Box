import numpy as np
from pylfsr import LFSR as lfsr


def getstateinbinary(inputstate):
    template = [0, 0, 0, 0, 0, 0, 0, 0]
    binary = [int(i) for i in list('{0:0b}'.format(inputstate))]
    if len(binary) == 8:
        return binary
    elif len(binary) > 8:
        return template
    else:
        spacedBinary = template
        nextBitPosition = len(template) - len(binary)
        for bit in binary:
            template[nextBitPosition] = bit
            nextBitPosition += 1
        return spacedBinary


def dotproduct(x: [], y: []):
    # Returns a single 0 or 1
    intermediate = [None] * 8
    if len(x) != len(y) != 8:
        print("SOMETHING IS ABOMINABLY WRONG")
        exit(1)
    for ind in range(8):
        intermediate[ind] = x[ind] and y[ind]
    currentVal = 0
    for bit in intermediate:
        currentVal = currentVal != bit
    if currentVal:
        return 1
    else:
        return 0


polynomials = [[8, 4, 3, 2], [8, 5, 3, 1], [8, 6, 4, 3, 2, 1], [8, 6, 5, 1], [8, 6, 5, 2], [8, 6, 5, 3], [8, 7, 6, 1],
               [8, 7, 6, 5, 2, 1]]

allPolynomialsArePrimitive = True

stables = []

for i in range(len(polynomials)):
    a = 1
    subBox = []
    while a < 256:
        sr = lfsr(initstate=getstateinbinary(a), fpoly=polynomials[i], verbose=True)
        sr.runFullCycle()
        subArray = []
        b = 1
        while b < 256:
            val = ""
            start = 0
            for index in range(8):
                subSeq = sr.seq[start:start+8]
                val = val + str(dotproduct(subSeq, getstateinbinary(b)))
                start += 8
            subArray.append(int(val, 2))
            if int(val, 2) == 0:
                print("FOUND A ZERO, MAYDAY! MAYDAY!")
                exit(1)
            b += 1
        subBox.append(subArray)
        a += 1
    file = open(str(i+1) + ".json", "w+")
    file.write(str(subBox))
    file.close()
