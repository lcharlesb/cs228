from __future__ import division
# import sys
# sys.path.insert(0, '../..')
import numpy as np
import pickle
import knn

file = open("./userData/train3.p", "rb")
train3 = pickle.load(file);
file.close()

file = open("./userData/train4.p", "rb")
train4 = pickle.load(file);
file.close()

file = open("./userData/test3.p", "rb")
test3 = pickle.load(file);
file.close()

file = open("./userData/test4.p", "rb")
test4 = pickle.load(file);
file.close()

def ReshapeData(set1,set2):
    X = np.zeros((2000,5*2*3),dtype='f')
    y = np.zeros((2000,1),dtype='f')
    for row in range(0,1000):
        y[row] = 3
        y[row+1000] = 4
        col = 0
        for j in range(0,5):
            for k in range(0,2):
                for m in range(0,3):
                    X[row,col] = set1[j,k,m,row]
                    X[row+1000,col] = set2[j,k,m,row]
                    col = col+1
    return X, y

def ReduceData(X):
    X = np.delete(X,1,1)
    X = np.delete(X,1,1)
    X = np.delete(X,1,2)
    X = np.delete(X,1,2)
    X = np.delete(X,1,2)
    return X

def CenterData(X):
    allXCoordinates = X[:,:,0,:]
    meanValue = allXCoordinates.mean()
    X[:,:,0,:] = allXCoordinates - meanValue
    allYCoordinates = X[:,:,1,:]
    meanValue = allYCoordinates.mean()
    X[:,:,1,:] = allYCoordinates - meanValue
    allZCoordinates = X[:,:,2,:]
    meanValue = allZCoordinates.mean()
    X[:,:,2,:] = allZCoordinates - meanValue
    return X

train3 = ReduceData(train3)
train4 = ReduceData(train4)
test3 = ReduceData(test3)
test4 = ReduceData(test4)

train3 = CenterData(train3)
train4 = CenterData(train4)
test3 = CenterData(test3)
test4 = CenterData(test4)

trainX, trainy = ReshapeData(train3, train4)
testX, testy = ReshapeData(test3, test4)

knn = knn.KNN()
knn.Use_K_Of(15)
knn.Fit(trainX, trainy)

correctPredictions = 0
for row in range(0, 2000):
    actualClass = testy[row]
    prediction = knn.Predict(testX[row])
    if(actualClass == prediction):
        correctPredictions = correctPredictions + 1

pickle.dump(knn, open('userData/classifier.p','wb'))
