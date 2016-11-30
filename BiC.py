import csv
import random
import math
import operator
import time

def loadDataset(filename, split, trainingSet=[], testSet=[]):
    with open(filename,'rb') as csvfile:
        lines = csv.reader(csvfile)
        next(lines,None)
        dataset = list(lines)
        for i in range(len(dataset)):
            for j in range(12):
                dataset[i][j]= float(dataset[i][j])
            if random.random() < split:
                del dataset[i][0]
                trainingSet.append(dataset[i])
            else:
                del dataset[i][0]
                testSet.append(dataset[i])

def loadDataTrain(filename, trainingSet=[]):
    with open(filename,'rb') as csvfile:
        lines = csv.reader(csvfile)
        next(lines,None)
        dataset = list(lines)
        for i in range(len(dataset)):
            for j in range(12):
                dataset[i][j]=float(dataset[i][j])
            del dataset[i][0]
            trainingSet.append(dataset[i])

def loadDataTest(filename, testSet=[]):
    with open(filename,'rb') as csvfile:
        lines = csv.reader(csvfile)
        next(lines,None)
        dataset = list(lines)
        for i in range(len(dataset)):
            for j in range(11):
                dataset[i][j]=float(dataset[i][j])
            del dataset[i][0]
            testSet.append(dataset[i])

def saveDataTest(recordType, testSet=[]):
    filename = time.strftime("%y%m%d-%H%M%S");
    with open('Record'+recordType+'/'+filename,'wb') as recordFile:
        record = csv.writer(recordFile, delimiter='[',
                             quoting=csv.QUOTE_MINIMAL)
        record.writerows(testSet)

def euclideanDistance(instance1, instance2, length):
    distance=0
    for x in range(length):
        distance += pow((instance1[x]-instance2[x]),2)
    return math.sqrt(distance)

def getNeighbor(trainingSet, testInstance, k):
    distance=[]
    length = len(testInstance)-1
    for i in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[i],length)
        distance.append((trainingSet[i],dist))
    distance.sort(key=operator.itemgetter(1))
    neighbors = []
    for i in range(k):
        neighbors.append(distance[i][0])
    return neighbors

def getResponse(neighbors):
    classVotes = {}
    for i in range(len(neighbors)):
        response = neighbors[i][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.iteritems(),key=operator.itemgetter(1), reverse = True)
    return sortedVotes[0][0]

def getAccuracy(testSet, predictions):
    correct = 0
    for i in range(len(testSet)):
        if testSet[i][-1] == predictions[i]:
            correct += 1
    return (correct/float(len(testSet))) * 100.0

def mainTrain():
    trainingSet = []
    testSet = []
    recordSet = []
    split = 0.80
    loadDataset('Data/Train.csv',split,trainingSet,testSet)
    print 'Train Set: '+repr(len(trainingSet))
    print 'Test Set: '+repr(len(testSet))
    predictions=[]
    # k = 5
    k = 269
    for i in range(len(testSet)):
        neighbors = getNeighbor(trainingSet,testSet[i],k)
        result = getResponse(neighbors)
        predictions.append(result)
        print '> '+repr(i+1)+'. predicted=' + repr(result) + ', actual=' + repr(testSet[i][-1])
        recordSet.append(['>'+repr(i+1)+' predicted=' + repr(result) + ', actual=' + repr(testSet[i][-1])])
    accuracy = getAccuracy(testSet, predictions)
    print('Accuracy: '+ repr(accuracy)+'%')
    recordSet.append(['Accuracy: '+ repr(accuracy)+'%'])
    saveDataTest('Train',recordSet)

def mainTest():
    trainingSet = []
    testSet = []
    recordSet = []
    loadDataTrain('Data/Train.csv',trainingSet)
    loadDataTest('Data/Test.csv',testSet)
    print 'Train Set: '+repr(len(trainingSet))
    print 'Test Set: '+repr(len(testSet))
    predictions=[]
    k = 5
    recordSet.append(['ID,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,y'])
    for i in range(len(testSet)):
        neighbors = getNeighbor(trainingSet,testSet[i],k)
        result = (getResponse(neighbors))
        print repr(i+1)+',' + ','.join(map(str,testSet[i])) + ',' + repr(result)
        # print '> Data-'+repr(i+1)+'=' + repr(testSet[i]) + ', result=' + repr(result)
        recordSet.append([repr(i+1)+',' + ','.join(map(str,testSet[i])) + ',' + repr(result)])
    saveDataTest('Test',recordSet)

# mainTest()
mainTest()
