import math
import random
import matplotlib.pyplot as plt


def makeList(qubits):
    listnum = []
    for i in range(2**qubits):
        listnum.append(i+1)
    random.shuffle(listnum)
    return listnum

qubits = int(input("Enter the number of qubits (must be integer and greater than 1)\n"))
listnum = makeList(qubits)
INDEX = random.randint(0, 2**qubits - 1)
target = listnum[INDEX]

def printList(lists):
    for num in lists:
        print(num)

def createOracle(target):
    return lambda x: 1 if x == target else 0

def oracleGate(index, state):
    state[index]*=-1
    return state

def diffuser(listnum):
    total = 0
    average = 0
    for num in listnum:
        total += num
    average = total/len(listnum)
    for i in range(len(listnum)):
        currentProb = listnum[i]
        listnum[i] = 2*average - currentProb
    return listnum

def superPosition(qubits):
    superList = []
    for i in range(qubits):
        superList.append(1/(qubits**0.5))
    return superList

def squareChecker(lists):
    num = 0
    for value in lists:
        num+= value**2
    return num

def mathPlotter(lists):
    labels = ["Amplitude", "Probability", "Other Amp"]
    i = 0
    for manyLists in lists:
        label = labels[i]
        i+=1
        plt.plot(range(1, iterations + 1), manyLists, marker='o', label=label)
    plt.title("Amplitude/Probability/Other change over each iteration")
    plt.xlabel("Iteration")
    plt.ylabel("Amplitude/Probability/Other")
    plt.legend() 
    plt.grid(True)
    plt.show()

def grover(qubits, target, listnum, iterations):
    ampList = superPosition(2**qubits)
    targetIndex = 0
    currentHigh = 0
    num1 = 0
    testIndex = 0
    ampPlot = []
    probPlot = []
    otherPlot = []
    oracleList = list(map(createOracle(target), listnum))
    #print(oracleList)
    #for i in range(int((math.pi/4)*(2**qubits)**0.5)):
    for i in range(iterations):
        num1+=1
        print(f"Iteration: {num1}")
        #simulate only flipping the marked one
        if oracleList[listnum.index(target)]:
            ampList = oracleGate(listnum.index(target), ampList)
        ampList = diffuser(ampList)
        ampPlot.append(ampList[listnum.index(target)])
        probPlot.append(ampList[listnum.index(target)]**2)
        print(f"Amplitude {ampList[listnum.index(target)]}")
        if listnum.index(target) == testIndex:
            testIndex+=1
        print(f"Other Amplitudes {ampList[testIndex]}")
        otherPlot.append(ampList[testIndex])
        print(f"Probability {ampList[listnum.index(target)]**2}")
        print(f"Squared Correctly? {squareChecker(ampList)}")
      
    #print(ampList)
    for i in range(len(listnum)):
        ampList[i] = ampList[i]**2
        #print(f"At index {i}: {ampList[i]}")
        if ampList[i] > currentHigh:
            #print(f"At index {i}: {currentHigh} < {ampList[i]}")
            currentHigh = ampList[i]
            targetIndex = i
            #print(targetIndex)
    #print(ampList)
    print(f"Highest probability is {ampList[targetIndex]} at index {targetIndex}")
    print(f"Highest amplitude is {ampList[targetIndex]**0.5} at index {targetIndex}")
    mathPlotter([ampPlot, probPlot, otherPlot])
    return targetIndex

iterations = int(input("Enter the number of iterations (must be integer and greater than 0)\n"))
found = grover(qubits, target, listnum, iterations)

print(f"Target number {target} in list {listnum} was found at index {found}")


