from __future__ import division
import sys
sys.path.insert(0, '../..')
import Leap
from pygameWindow import PYGAME_WINDOW
import pygame.image
import random
import constants
import pickle
import numpy as np
from random import seed
from random import randint
import time

clf = pickle.load(open('userData/classifier.p','rb'))
testData = np.zeros((1,30),dtype='f')

pygameWindow = PYGAME_WINDOW()

x = 250
y = 250
xMin = -100.0
xMax = 100.0
yMin = -100.0
yMax = 100.0
programState = 0
handPos = 0
countForHandPos = 0
countForNumCorrect = 0
currentNumCorrect = 1
numToSign = 0
k = 0
countForProgramState = 0

def Handle_Vector_From_Leap(v):
    global xMin, xMax, yMin, yMax
    x = ScaleCoordinates(int(v[0]), xMin, xMax, 0, constants.pygameWindowWidth/2)
    y = ScaleCoordinates(int(v[1]), yMin, yMax, 0, constants.pygameWindowDepth/2)
    z = ScaleCoordinates(int(v[2]), yMin, yMax, 0, constants.pygameWindowDepth/2)
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

def Handle_Hand_Position(frame):
    global handPos, countForHandPos
    hand = frame.hands[0]
    fingers = hand.fingers
    for finger in fingers:
        tip = finger.bone(3).next_joint
        x, y, z = Handle_Vector_From_Leap(tip)
        if(x < 0):
            pygameWindow.Draw_Instruction_Right()
            handPos = 0
            countForHandPos = 0
        elif(x > 200):
            pygameWindow.Draw_Instruction_Left()
            handPos = 0
            countForHandPos = 0
        else:
            if(y < 110):
                pygameWindow.Draw_Instruction_Up()
                handPos = 0
                countForHandPos = 0
            elif(y > 190):
                pygameWindow.Draw_Instruction_Down()
                handPos = 0
                countForHandPos = 0
            else:
                if(z < 0):
                    pygameWindow.Draw_Instruction_In()
                    handPos = 0
                    countForHandPos = 0
                elif(z > 100):
                    pygameWindow.Draw_Instruction_Out()
                    handPos = 0
                    countForHandPos = 0
                else:
                    pygameWindow.Draw_Instruction_Success()
                    handPos = 1
                    countForHandPos += 1



def HandleState0(frame):
    global programState
    pygameWindow.Draw_Instruction_Picture()
    if HandOverDevice(frame):
        programState = 1

def HandleState1(frame):
    global programState, handPos, countForHandPos
    Handle_Frame(frame)
    if(countForHandPos >= 250):
        programState = 2
    Handle_Hand_Position(frame)
    if not HandOverDevice(frame):
        programState = 0

def HandleState2(frame, num):
    if(num == 8):
        num = 5
    global testData, clf, countForNumCorrect, currentNumCorrect, programState
    if(num == 1):
        pygameWindow.Draw1()
    elif(num == 2):
        pygameWindow.Draw2()
    elif(num == 3):
        pygameWindow.Draw3()
    elif(num == 4):
        pygameWindow.Draw4()
    elif(num == 5):
        pygameWindow.Draw5()
    elif(num == 6):
        pygameWindow.Draw6()
    elif(num == 7):
        pygameWindow.Draw7()
    elif(num == 8):
        pygameWindow.Draw8()
    elif(num == 9):
        pygameWindow.Draw9()
    Handle_Frame(frame)
    testData = CenterData(testData)
    predictedClass = clf.Predict(testData)
    print(predictedClass)
    if(predictedClass == num):
        countForNumCorrect += 1
    else:
        countForNumCorrect = 0
    if(countForNumCorrect >= 10):
        currentNumCorrect = 1
        programState = 3

def HandleState3(frame):
    global programState, countForProgramState
    pygameWindow.Draw_Instruction_Success()
    if(countForProgramState > 50):
        programState = 2
    countForProgramState += 1

def HandOverDevice(frame):
    if(len(frame.hands) > 0):
        return True
    return False

controller = Leap.Controller()

pygameX = 0
pygameY = 0

seed(1)

while True:
    pygameWindow.Prepare()
    frame = controller.frame()
    k = 0
    if(len(frame.hands) < 1):
        programState = 0
    if programState == 0:
        HandleState0(frame)
    elif programState == 1:
        HandleState1(frame)
    elif programState == 2:
        if(currentNumCorrect == 1):
            numToSign = randint(1,9)
            currentNumCorrect = 0
            countForNumCorrect = 0
        HandleState2(frame,numToSign)
    elif programState == 3:
        HandleState3(frame)
    pygameWindow.Reveal()
