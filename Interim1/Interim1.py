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

seed(randint(0,100))

############### HAND POSITION VARIABLES ###############

# The controller object itself.
controller = Leap.Controller()
# The window used to display to the user. Set to none originally so window does not show until user enters their name.
pygameWindow = None
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
# lastDigitShown holds the previous digit shown to the user.
lastDigitShown = 0
#numCounter is used to track when to display that the user has failed the current digit (if it is greater than timeAllowedPerNumber).
numCounter = 0
# timeAllowedPerNumber holds the amount of iterations before a failure.
timeAllowedPerNumber = 40
# counterForSuccessDisplay iterates every time success is displayed to the user, up until 20, then a new digit is shown to the user.
counterForSuccessDisplay = 0
# counterForFailureDisplay iterates every time failure is displayed to the user, up until 20, then a new digit is shown to the user.
counterForFailureDisplay = 0
# iterationsForSuccess stores the number of times iterated through HandleState3 that the success should be displayed until going back to a different program state.
iterationsForSuccess = 20
# iterationsForFailure stores the number of times iterated through HandleState4 that the failure should be displayed until going back to a different program state.
iterationsForFailure = 20

############### SCAFFOLDING VARIABLES ###############

# successCounterForScaffolding is first used to add another digit to display to the user every 5 successes,
# and then used to decrease the time allowed every 20 successes.
successCounterForScaffolding = 0
# digitsToDisplay determines the pool from which the random digit will be chosen from.
# Incremented once every time successCounterForScaffolding reaches 5, until all 9 digits are presented to the user.
digitsToDisplay = 3
# digitsThatHaveBeenDisplayed is a list of the digits that the user has seen.
digitsThatHaveBeenDisplayed = []
# allDigitsDisplayedAndSucceeded is a boolean of whether the user has seen all the digits or not.
allDigitsDisplayedAndSucceeded = False
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

############### ARITHMATIC SECTION ###############
# arithmaticStage tracks whether the user has made it to the arithmatic stage or not.
arithmaticStage = False
# correctAnswerForArithmatic stores the current value that the user should sign to answer the arithmatic shown.
correctAnswerForArithmatic = 0
# additionOrSubtraction tracks which operator to use for the arithmatic stage (0 = addition, 1 = subtraction).
additionOrSubtraction = 0
# firstNumForArithmatic stores the first value of the equation.
firstNumForArithmatic = 0
# secondNumForArithmatic stores the seconds value of the equation.
secondNumForArithmatic = 0

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
    global allDigitsDisplayedAndSucceeded, pygameWindow
    if(num == 0):
        pygameWindow.Draw0()
        if(allDigitsDisplayedAndSucceeded == False):
            pygameWindow.Draw0Num()
    elif(num == 1):
        pygameWindow.Draw1()
        if(allDigitsDisplayedAndSucceeded == False):
            pygameWindow.Draw1Num()
    elif(num == 2):
        pygameWindow.Draw2()
        if(allDigitsDisplayedAndSucceeded == False):
            pygameWindow.Draw2Num()
    elif(num == 3):
        pygameWindow.Draw3()
        if(allDigitsDisplayedAndSucceeded == False):
            pygameWindow.Draw3Num()
    elif(num == 4):
        pygameWindow.Draw4()
        if(allDigitsDisplayedAndSucceeded == False):
            pygameWindow.Draw4Num()
    elif(num == 5):
        pygameWindow.Draw5()
        if(allDigitsDisplayedAndSucceeded == False):
            pygameWindow.Draw5Num()
    elif(num == 6):
        pygameWindow.Draw6()
        if(allDigitsDisplayedAndSucceeded == False):
            pygameWindow.Draw6Num()
    elif(num == 7):
        pygameWindow.Draw7()
        if(allDigitsDisplayedAndSucceeded == False):
            pygameWindow.Draw7Num()
    elif(num == 8):
        pygameWindow.Draw8()
        if(allDigitsDisplayedAndSucceeded == False):
            pygameWindow.Draw8Num()
    elif(num == 9):
        pygameWindow.Draw9()
        if(allDigitsDisplayedAndSucceeded == False):
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
    global programState, countForHandPos, arithmaticStage
    Handle_Frame(frame)
    # If hand is correctly over the device for a count of 150, move on to the signing portion of the program.
    if(countForHandPos >= 150):
        if(arithmaticStage == True):
            programState = 5
        else:
            programState = 2
    Handle_Hand_Position(frame)
    # If hand is not over device, show instruction to put hand over device.
    if not HandOverDevice(frame):
        programState = 0

# HandleState2 displays a digit for the user to sign, and uses counts to decide whether the user signs the digit correctly or not.
def HandleState2(frame):
    global testData, clf, countForCorrectSign, displayNewDigit, programState, digitsToDisplay, toggleHandColor, successCounterForScaffolding, reducedTimeStage, timeAllowedPerNumber, numCounter, digitToSign, database, counterForFailureDisplay, counterForSuccessDisplay, allDigitsDisplayedAndSucceeded, digitsThatHaveBeenDisplayed, arithmaticStage, lastDigitShown

    if(allDigitsDisplayedAndSucceeded == False and successCounterForScaffolding >= 5 and reducedTimeStage == False):
        if(digitsToDisplay == 3 and 1 in digitsThatHaveBeenDisplayed and 2 in digitsThatHaveBeenDisplayed and 3 in digitsThatHaveBeenDisplayed):
            digitsToDisplay = 4
            digitToSign = 4
            IncrementDatabaseNumber(digitToSign)
            displayNewDigit = False
            countForCorrectSign = 0
        elif(digitsToDisplay == 4 and 4 in digitsThatHaveBeenDisplayed):
            digitsToDisplay = 5
            digitToSign = 5
            IncrementDatabaseNumber(digitToSign)
            displayNewDigit = False
            countForCorrectSign = 0
        elif(digitsToDisplay == 5 and 5 in digitsThatHaveBeenDisplayed):
            digitsToDisplay = 6
            digitToSign = 6
            IncrementDatabaseNumber(digitToSign)
            displayNewDigit = False
            countForCorrectSign = 0
        elif(digitsToDisplay == 6 and 6 in digitsThatHaveBeenDisplayed):
            digitsToDisplay = 7
            digitToSign = 7
            IncrementDatabaseNumber(digitToSign)
            displayNewDigit = False
            countForCorrectSign = 0
        elif(digitsToDisplay == 7 and 7 in digitsThatHaveBeenDisplayed):
            digitsToDisplay = 8
            digitToSign = 8
            IncrementDatabaseNumber(digitToSign)
            displayNewDigit = False
            countForCorrectSign = 0
        elif(digitsToDisplay == 8 and 8 in digitsThatHaveBeenDisplayed):
            digitsToDisplay = 9
            digitToSign = 9
            IncrementDatabaseNumber(digitToSign)
            displayNewDigit = False
            countForCorrectSign = 0
        elif(digitsToDisplay == 9 and 9 in digitsThatHaveBeenDisplayed):
            allDigitsDisplayedAndSucceeded = True
        successCounterForScaffolding = 0

    if(allDigitsDisplayedAndSucceeded == True and reducedTimeStage == False and successCounterForScaffolding >= 15):
        successCounterForScaffolding = 0
        reducedTimeStage = True
        print("All digits succeeded: Reduced time stage begins.")

    if(successCounterForScaffolding >= 8 and reducedTimeStage == True):
        if(timeAllowedPerNumber == 40):
            print("Reducing time to 35.")
            timeAllowedPerNumber = 35
        elif(timeAllowedPerNumber == 35):
            print("Reducing time to 30.")
            timeAllowedPerNumber = 30
        elif(timeAllowedPerNumber == 30):
            print("Reducing time to 25.")
            timeAllowedPerNumber = 25
        elif(timeAllowedPerNumber == 25):
            print("Reduced time stage passed. Arithmatic stage begins.")
            arithmaticStage = True
            programState = 5
            timeAllowedPerNumber = 40
        successCounterForScaffolding = 0

    if(displayNewDigit == True):
        numCounter = 0
        if(digitsToDisplay not in digitsThatHaveBeenDisplayed and lastDigitShown != digitsToDisplay):
            digitToSign = digitsToDisplay
        else:
            lastDigitShown = digitToSign
            while(digitToSign == lastDigitShown):
                digitToSign = randint(0,digitsToDisplay)
        displayNewDigit = False
        countForCorrectSign = 0
        IncrementDatabaseNumber(digitToSign)

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

    # Display success if numCounter is greater than or equal to timeAllowedPerNumber
    if(numCounter >= timeAllowedPerNumber):
        if(predictedClass != digitToSign):
            numCounter = 0
            programState = 4

    # Display success if sign is correct for a count of 10
    if(countForCorrectSign >= 10):
        toggleHandColor = False
        displayNewDigit = True
        programState = 3

        if digitToSign not in digitsThatHaveBeenDisplayed:
            digitsThatHaveBeenDisplayed.append(digitToSign)

    numCounter += 1

    pickle.dump(database, open('userData/database.p','wb'))

# HandleState3 draws success on screen for a count of 20
def HandleState3(frame):
    global programState, counterForSuccessDisplay, successCounterForScaffolding, countAttempts, countSuccesses, arithmaticStage, iterationsForSuccess
    pygameWindow.Draw_Instruction_Success()
    if(counterForSuccessDisplay >= iterationsForSuccess):
        successCounterForScaffolding += 1
        if(arithmaticStage == True):
            programState = 5
        else:
            programState = 2
        countAttempts += 1
        countSuccesses += 1
        counterForSuccessDisplay = 0
    counterForSuccessDisplay += 1

# HandleState4 draws failure on the screen for a count of 20
def HandleState4(frame):
    global programState, counterForFailureDisplay, displayNewDigit, countAttempts, arithmaticStage, iterationsForFailure
    if(counterForFailureDisplay >= iterationsForFailure):
        if(arithmaticStage == True):
            programState = 5
        else:
            programState = 2
        displayNewDigit = True
        counterForFailureDisplay = 0
        countAttempts += 1
    counterForFailureDisplay += 1
    pygameWindow.Draw_Instruction_Failure()

# HandleState5 begins to display basic arithmatic on the screen for the user to solve.
def HandleState5(frame):
    global testData, clf, arithmaticStage, countForCorrectSign, programState, toggleHandColor, displayNewDigit, correctAnswerForArithmatic, additionOrSubtraction, firstNumForArithmatic, secondNumForArithmatic, numCounter, timeAllowedPerNumber

    if(displayNewDigit == True):
        additionOrSubtraction = randint(0,1)

        firstNumForArithmatic = 0
        secondNumForArithmatic = 0
        correctAnswerForArithmatic = 0

        if (additionOrSubtraction == 0):
            firstNumForArithmatic = randint(0,4)
            secondNumForArithmatic = randint(0,5)
            correctAnswerForArithmatic = firstNumForArithmatic + secondNumForArithmatic

        elif (additionOrSubtraction == 1):
            firstNumForArithmatic = randint(4,9)
            secondNumForArithmatic = randint(0,4)
            correctAnswerForArithmatic = firstNumForArithmatic - secondNumForArithmatic

        countForCorrectSign = 0
        displayNewDigit = False
        numCounter = 0
        IncrementDatabaseNumber(correctAnswerForArithmatic)

    pygameWindow.DrawArithmatic(additionOrSubtraction, firstNumForArithmatic, secondNumForArithmatic)
    Handle_Frame(frame)

    testData = CenterData(testData)
    predictedClass = clf.Predict(testData)

    # Show hand color as green if sign is correct, black if sign is incorrect.
    if(predictedClass == correctAnswerForArithmatic):
        toggleHandColor = True
        countForCorrectSign += 1
    else:
        toggleHandColor = False
        countForCorrectSign = 0

    # Display success if sign is correct for a count of 10.
    if(countForCorrectSign >= 10):
        toggleHandColor = False
        displayNewDigit = True
        programState = 3

    # Display failure if sign is incorrect for the amount of time allowed per number.
    if(numCounter >= timeAllowedPerNumber):
        if(predictedClass != correctAnswerForArithmatic):
            numCounter = 0
            programState = 4

    numCounter += 1


# HandOverDevice determines whether a hand is over the device (true, false)
def HandOverDevice(frame):
    if(len(frame.hands) > 0):
        return True
    return False

def IncrementDatabaseNumber(digitToSign):
    global database, userName

    userEntry = database[userName]
    numToIncrement = userEntry['digit'+str(digitToSign)+'attempted']
    numToIncrement += 1
    userEntry['digit'+str(digitToSign)+'attempted'] = numToIncrement

def HandleDatabase():
    global database, userName, countUsers, currUserRank, arithmaticStage, digitsToDisplay, digitsThatHaveBeenDisplayed, allDigitsDisplayedAndSucceeded, reducedTimeStage

    userName = raw_input('Please enter your name: ')

    if userName in database:
        print('welcome back ' + userName + '.')
        userEntry = database[userName]
        incrementMe = userEntry['logins']
        incrementMe += 1
        userEntry['logins'] = incrementMe
        previousPercentage = userEntry['percentSuccess']
        arithmaticStage = userEntry['arithmaticStage']
        digitsToDisplay = userEntry['digitsToDisplay']
        digitsThatHaveBeenDisplayed = userEntry['digitsThatHaveBeenDisplayed']
        allDigitsDisplayedAndSucceeded = userEntry['allDigitsDisplayedAndSucceeded']
        reducedTimeStage = userEntry['reducedTimeStage']
    else:
        database[userName] = {'logins': 1}
        print('welcome ' + userName + '.')
        userEntry = database[userName]
        for i in range(0,10):
            userEntry['digit'+str(i)+'attempted'] = 0
        userEntry['totalPercentage'] = 0.0
        userEntry['arithmaticStage'] = False
        userEntry['digitsToDisplay'] = digitsToDisplay
        userEntry['digitsThatHaveBeenDisplayed'] = digitsThatHaveBeenDisplayed
        userEntry['allDigitsDisplayedAndSucceeded'] = allDigitsDisplayedAndSucceeded
        userEntry['reducedTimeStage'] = reducedTimeStage

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
    global database, userName, countAttempts, countSuccesses, arithmaticStage, digitsToDisplay, digitsThatHaveBeenDisplayed, allDigitsDisplayedAndSucceeded, reducedTimeStage
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
    userEntry['arithmaticStage'] = arithmaticStage
    userEntry['digitsToDisplay'] = digitsToDisplay
    userEntry['digitsThatHaveBeenDisplayed'] = digitsThatHaveBeenDisplayed
    userEntry['allDigitsDisplayedAndSucceeded'] = allDigitsDisplayedAndSucceeded
    userEntry['reducedTimeStage'] = reducedTimeStage

    pickle.dump(database, open('userData/database.p','wb'))

atexit.register(exit_handler)

############### LOCAL CODE (basically main) ###############

HandleDatabase()

pygameWindow = PYGAME_WINDOW()

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
    elif programState == 5:
        HandleState5(frame)
        pygameWindow.DrawDatabaseData(database, userName, countSuccesses, countAttempts, previousPercentage, currUserRank)

    pygameWindow.Reveal()
