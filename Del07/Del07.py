from __future__ import division
import sys
sys.path.insert(0, '../..')
import Leap
from pygameWindow import PYGAME_WINDOW
import random
import constants
import pickle
import numpy as np

clf = pickle.load(open('userData/classifier.p','rb'))
testData = np.zeros((1,30),dtype='f')

pygameWindow = PYGAME_WINDOW()

x = 250
y = 250
xMin = -100.0
xMax = 100.0
yMin = -100.0
yMax = 100.0
k = 0

def Handle_Vector_From_Leap(v):
    global xMin, xMax, yMin, yMax
    x = ScaleCoordinates(int(v[0]), xMin, xMax, 0, constants.pygameWindowWidth)
    y = ScaleCoordinates(int(v[1]), yMin, yMax, 0, constants.pygameWindowDepth)
    z = ScaleCoordinates(int(v[2]), yMin, yMax, 0, constants.pygameWindowDepth)
    if(x < xMin):
        xMin = x
    if(x > xMax):
        xMax = x
    if(y < yMin):
        yMin = y
    if(y > yMax):
        yMax = y
    return x, y, z

def Handle_Bone(bone):
    base = bone.prev_joint
    tip = bone.next_joint
    baseX, baseY, baseZ = Handle_Vector_From_Leap(base)
    tipX, tipY, tipZ = Handle_Vector_From_Leap(tip)
    pygameWindow.Draw_Black_Line(baseX, baseZ, tipX, tipZ, 3 - bone.type)
    return tipX, tipY, tipZ

def Handle_Finger(finger):
    global k
    for b in range(0,4):
        xTip, yTip, zTip = Handle_Bone(finger.bone(b))
        if((b == 0) or (b == 3)):
            testData[0,k] = xTip
            testData[0,k+1] = yTip
            testData[0,k+2] = zTip
            k = k + 3

def Handle_Frame(frame):
    hand = frame.hands[0]
    fingers = hand.fingers
    for finger in fingers:
        Handle_Finger(finger)

def ScaleCoordinates(value, rangeOneLow, rangeOneHigh, rangeTwoLow, rangeTwoHigh):
    rangeOne = abs(rangeOneHigh - rangeOneLow)
    if(rangeOne == 0):
        return rangeTwoLow
    else:
        rangeTwo = abs(rangeTwoHigh - rangeTwoLow)
        return int((((value - rangeOneLow) * rangeTwo) / rangeOne) + rangeTwoLow)

def CenterData(data):
    # Array to pass back
    newArray = np.zeros((1,30),dtype='f')

    # x coordinates
    xValues = data[0,::3]
    xCount = 0
    xTotal = 0
    for x in xValues:
        xCount = xCount + 1
        xTotal = xTotal + x
    mean = xTotal/xCount
    newArray[0,::3] = data[0,::3] - mean

    # y coordinates
    yValues = data[0,1::3]
    yCount = 0
    yTotal = 0
    for y in yValues:
        yCount = yCount + 1
        yTotal = yTotal + y
    mean = yTotal/yCount
    newArray[0,1::3] = data[0,1::3] - mean

    # z coordinates
    zValues = data[0,2::3]
    zCount = 0
    zTotal = 0
    for z in zValues:
        zCount = zCount + 1
        zTotal = zTotal + z
    mean = zTotal/zCount
    newArray[0,2::3] = data[0,2::3] - mean

    return newArray

controller = Leap.Controller()

pygameX = 0
pygameY = 0

while True:
    pygameWindow.Prepare()
    frame = controller.frame()
    if (len(frame.hands) > 0):
        k = 0
        Handle_Frame(frame)
    #     pygameX = ScaleCoordinates(x, xMin, xMax, 0, constants.pygameWindowWidth)
    #     pygameY = ScaleCoordinates(y, yMin, yMax, 0, constants.pygameWindowDepth)
    # pygameWindow.Draw_Black_Circle(pygameX,(constants.pygameWindowDepth - pygameY))
        testData = CenterData(testData)
        predictedClass = clf.Predict(testData)
        print(predictedClass)
    pygameWindow.Reveal()
