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
import atexit

seed(2)

############### HAND POSITION VARIABLES ###############

# The controller object itself.
controller = Leap.Controller()
# The window used to display to the user.
pygameWindow = PYGAME_WINDOW()
# x, y, z used as coordinates for hand tracking
x = 250
y = 250
z = 250
#xMin, xMax, yMin, yMax used for scaling the hand to fit the window.
xMin = -100.0
xMax = 100.0
yMin = -100.0
yMax = 100.0

############### DATABASE/KNN VARIABLES ###############
# database loaded in from file.
database = pickle.load(open('userData/database.p','rb'))
# userName set to current user's name (raw_input).
userName = ""
# k is used for handling the user's hand location.
k = 0
# clf is our classifier for our machine learning algorithm (knn).
clf = pickle.load(open('userData/classifier.p','rb'))
# testData is our test data for the knn algorithm.
testData = np.zeros((1,30),dtype='f')

############### PROGRAM LOGIC VARIABLES ###############

# programState is used to transition between stages of the program.
programState = 0
# countForHandPos is steadily incremented while the user's hand is in the correct location, and is used to switch to programState 2 when the count reached 150.
countForHandPos = 0
# countForCorrectSign increments when the user's sign matches the displayed sign, and is reset when it reaches 10 (switches to programState 3).
countForCorrectSign = 0
# displayNewDigit is used within HandleState2 to decide whether or not to display a new digit to the user.
displayNewDigit = True
# digitToSign is set randomly to a digit for the user to sign.
digitToSign = 0
#numCounter is used to track when to display that the user has failed the current digit (if it is greater than timeAllowedPerNumber)
numCounter = 0
timeAllowedPerNumber = 40
# counterForSuccessDisplay iterates every time success is displayed to the user, up until 20, then a new digit is shown to the user.
counterForSuccessDisplay = 0
# counterForFailureDisplay iterates every time failure is displayed to the user, up until 20, then a new digit is shown to the user.
counterForFailureDisplay = 0

############### SCAFFOLDING VARIABLES ###############

# successCounterForScaffolding is first used to add another digit to display to the user every 5 successes,
# and then used to decrease the time allowed every 20 successes.
successCounterForScaffolding = 0
# numbersToDisplay determines the pool from which the random digit will be chosen from.
# Incremented once every time successCounterForScaffolding reaches 5, until all 9 digits are presented to the user.
numbersToDisplay = 3
# reducedTimeStage is set to True once all 9 digits have been displayed to the user.
reducedTimeStage = False
# countAttempts is incremented upon success or failure to sign a digit, and is used to calculate the user's percentage of correctly signed digits.
countAttempts = 0
# countSuccesses is incremented upon success to sign a digit, and is used to calculate the user's percentage of correctly signed digits.
countSuccesses = 0
# previousPercentage is set to the percentage of cumulative success for all previous attempts for the current user.
previousPercentage = 0
# toggleHandColor: True = green, False = black.
toggleHandColor = False
# totalPercentage is stored in the DB, and is a cumulative number of the user's percent success for every login. Stored as (1.00 == 100%), and is divided by number of logins to determine the total percentage.
totalPercentage = 1.0
# countUsers counts the number of users in the DB, used to determine the current user's rank.
countUsers = 0
# currUserRank is increased when another user in the DB has a higher overall percentage than the current user.
currUserRank = 1

############### FUNCTIONS ###############

def Handle_Vector_From_Leap(v):
    global xMin, xMax, yMin, yMax
    x = int(v[0])
    y = int(v[1])
    z = int(v[2])

    if(x < xMin):
        xMin = x
    if(x > xMax):
        xMax = x
    if(y < yMin):
        yMin = y
    if(y > yMax):
        yMax = y

    x = ScaleCoordinates(x, xMin, xMax, 0, constants.pygameWindowWidth/2)
    y = ScaleCoordinates(y, yMin, yMax, 0, constants.pygameWindowDepth/2)
    z = ScaleCoordinates(z, yMin, yMax, 0, constants.pygameWindowDepth/2)

    return x, y, z

def Handle_Bone(bone):
    global toggleHandColor
    base = bone.prev_joint
    tip = bone.next_joint

    baseX, baseY, baseZ = Handle_Vector_From_Leap(base)
    tipX, tipY, tipZ = Handle_Vector_From_Leap(tip)

    pygameWindow.Draw_Black_Line(baseX, baseZ, tipX, tipZ, 3 - bone.type)
    pygameWindow.Draw_Line(baseX, baseZ, tipX, tipZ, 3 - bone.type, toggleHandColor)

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
    diff = value - rangeOneLow
    oldRange = rangeOneHigh - rangeOneLow
    newRange = rangeTwoHigh - rangeTwoLow
    if(oldRange == 0):
        return value
    oldFraction = diff / oldRange
    newValue = oldFraction * newRange
    return newValue

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
    global countForHandPos
    hand = frame.hands[0]
    fingers = hand.fingers

    for finger in fingers:

        tip = finger.bone(3).next_joint
        x, y, z = Handle_Vector_From_Leap(tip)

        if(x < 0):
            pygameWindow.Draw_Instruction_Right()
            countForHandPos = 0
        elif(x > 400):
            pygameWindow.Draw_Instruction_Left()
            countForHandPos = 0
        else:
            if(y < 100):
                pygameWindow.Draw_Instruction_Up()
                countForHandPos = 0
            elif(y > 250):
                pygameWindow.Draw_Instruction_Down()
                countForHandPos = 0
            else:
                if(z < 0):
                    pygameWindow.Draw_Instruction_In()
                    countForHandPos = 0
                elif(z > 100):
                    pygameWindow.Draw_Instruction_Out()
                    countForHandPos = 0
                else:
                    pygameWindow.Draw_Instruction_Success()
                    countForHandPos += 1

def DrawNumber(num):
    global numbersToDisplay, pygameWindow

    if(num == 1):
        pygameWindow.Draw1()
        if(numbersToDisplay != 9):
            pygameWindow.Draw1Num()
    elif(num == 2):
        pygameWindow.Draw2()
        if(numbersToDisplay != 9):
            pygameWindow.Draw2Num()
    elif(num == 3):
        pygameWindow.Draw3()
        if(numbersToDisplay != 9):
            pygameWindow.Draw3Num()
    elif(num == 4):
        pygameWindow.Draw4()
        if(numbersToDisplay != 9):
            pygameWindow.Draw4Num()
    elif(num == 5):
        pygameWindow.Draw5()
        if(numbersToDisplay != 9):
            pygameWindow.Draw5Num()
    elif(num == 6):
        pygameWindow.Draw6()
        if(numbersToDisplay != 9):
            pygameWindow.Draw6Num()
    elif(num == 7):
        pygameWindow.Draw7()
        if(numbersToDisplay != 9):
            pygameWindow.Draw7Num()
    elif(num == 8):
        pygameWindow.Draw8()
        if(numbersToDisplay != 9):
            pygameWindow.Draw8Num()
    elif(num == 9):
        pygameWindow.Draw9()
        if(numbersToDisplay != 9):
            pygameWindow.Draw9Num()

# HandleState0 draws instructions for the user to put their hand over the device.
def HandleState0(frame):
    global programState
    pygameWindow.Draw_Instruction_Picture()
    # If hand is over device, move on to programState 1.
    if HandOverDevice(frame):
        programState = 1

# HandleState1 instructs the user to position their hand in the right location over the device.
def HandleState1(frame):
    global programState, countForHandPos
    Handle_Frame(frame)
    # If hand is correctly over the device for a count of 150, move on to the signing portion of the program.
    if(countForHandPos >= 150):
        programState = 2
    Handle_Hand_Position(frame)
    # If hand is not over device, show instruction to put hand over device.
    if not HandOverDevice(frame):
        programState = 0

# HandleState2 displays a digit for the user to sign, and uses counts to decide whether the user signs the digit correctly or not.
def HandleState2(frame):
    global testData, clf, countForCorrectSign, displayNewDigit, programState, numbersToDisplay, toggleHandColor, successCounterForScaffolding, reducedTimeStage, timeAllowedPerNumber, numCounter, digitToSign, database, counterForFailureDisplay, counterForSuccessDisplay
    counterForSuccessDisplay = 0

    if(successCounterForScaffolding >= 5 and reducedTimeStage == False):
        if(numbersToDisplay == 3):
            numbersToDisplay = 4
        elif(numbersToDisplay == 4):
            numbersToDisplay = 5
        elif(numbersToDisplay == 5):
            numbersToDisplay = 6
        elif(numbersToDisplay == 6):
            numbersToDisplay = 7
        elif(numbersToDisplay == 7):
            numbersToDisplay = 8
        elif(numbersToDisplay == 8):
            numbersToDisplay = 9
            reducedTimeStage = True
        successCounterForScaffolding = 0

    if(successCounterForScaffolding >= 20 and reducedTimeStage == False):
        if(timeAllowedPerNumber == 40):
            timeAllowedPerNumber = 35
        if(timeAllowedPerNumber == 35):
            timeAllowedPerNumber = 30
        if(timeAllowedPerNumber == 30):
            timeAllowedPerNumber = 25
        successCounterForScaffolding = 0

    if(numCounter >= timeAllowedPerNumber):
        numCounter = 0
        programState = 4

    if(displayNewDigit == True):
        numCounter = 0
        digitToSign = randint(1,numbersToDisplay)
        displayNewDigit = False
        countForCorrectSign = 0
        userEntry = database[userName]
        numToIncrement = userEntry['digit'+str(digitToSign)+'attempted']
        numToIncrement += 1
        userEntry['digit'+str(digitToSign)+'attempted'] = numToIncrement

    DrawNumber(digitToSign)
    Handle_Frame(frame)

    testData = CenterData(testData)
    predictedClass = clf.Predict(testData)

    # Show hand color as green if sign is correct, black if sign is incorrect
    if(predictedClass == digitToSign):
        toggleHandColor = True
        countForCorrectSign += 1
    else:
        toggleHandColor = False
        countForCorrectSign = 0

    # Display success if sign is correct for a count of 10
    if(countForCorrectSign >= 10):
        toggleHandColor = False
        displayNewDigit = True
        programState = 3

    numCounter += 1

    pickle.dump(database, open('userData/database.p','wb'))

# HandleState3 draws success on screen for a count of 20
def HandleState3(frame):
    global programState, counterForSuccessDisplay, successCounterForScaffolding, countAttempts, countSuccesses
    pygameWindow.Draw_Instruction_Success()
    if(counterForSuccessDisplay >= 20):
        successCounterForScaffolding += 1
        programState = 2
        countAttempts += 1
        countSuccesses += 1
    counterForSuccessDisplay += 1

# HandleState4 draws failure on the screen for a count of 20
def HandleState4(frame):
    global programState, counterForFailureDisplay, displayNewDigit, countAttempts
    if(counterForFailureDisplay >= 20):
        programState = 2
        displayNewDigit = True
        counterForFailureDisplay = 0
        countAttempts += 1
    counterForFailureDisplay += 1
    pygameWindow.Draw_Instruction_Failure()

# HandOverDevice determines whether a hand is over the device (true, false)
def HandOverDevice(frame):
    if(len(frame.hands) > 0):
        return True
    return False

def HandleDatabase():
    global database, userName, countUsers, currUserRank

    userName = raw_input('Please enter your name: ')

    if userName in database:
        print('welcome back ' + userName + '.')
        userEntry = database[userName]
        incrementMe = userEntry['logins']
        incrementMe += 1
        userEntry['logins'] = incrementMe
        previousPercentage = userEntry['percentSuccess']
    else:
        database[userName] = {'logins': 1}
        print('welcome ' + userName + '.')
        userEntry = database[userName]
        for i in range(1,10):
            userEntry['digit'+str(i)+'attempted'] = 0
        userEntry['totalPercentage'] = 0.0

    totalPercentage = userEntry['totalPercentage']
    currUserTotalPercentageCalculated = totalPercentage / userEntry['logins']
    for name in database:
        countUsers += 1
        otherUser = database[name]
        otherUserTotalPercentageCalculated = otherUser['totalPercentage'] / otherUser['logins']
        if otherUserTotalPercentageCalculated > currUserTotalPercentageCalculated:
            currUserRank += 1

# exit_handler is called on exit of program, saves user data (percentSuccess, totalPercentage)
def exit_handler():
    global database, userName, countAttempts, countSuccesses
    userEntry = database[userName]
    prevSuccessRate = 0

    if countAttempts != 0:
        prevSuccessRate = countSuccesses / countAttempts

    if(countAttempts == 0):
        userEntry['percentSuccess'] =  1.0
    else:
        userEntry['percentSuccess'] = prevSuccessRate

    totalPercentage = userEntry['totalPercentage']
    totalPercentage += prevSuccessRate
    userEntry['totalPercentage'] = totalPercentage

    pickle.dump(database, open('userData/database.p','wb'))

############### LOCAL CODE (basically main) ###############

HandleDatabase()

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
        HandleState2(frame)
        pygameWindow.DrawDatabaseData(database, userName, countSuccesses, countAttempts, previousPercentage, currUserRank)
    elif programState == 3:
        HandleState3(frame)
        pygameWindow.DrawDatabaseData(database, userName, countSuccesses, countAttempts, previousPercentage, currUserRank)
    elif programState == 4:
        HandleState4(frame)
        pygameWindow.DrawDatabaseData(database, userName, countSuccesses, countAttempts, previousPercentage, currUserRank)

    pygameWindow.Reveal()

atexit.register(exit_handler)
