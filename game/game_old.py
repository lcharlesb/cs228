from __future__ import division
from pygameWindow import PYGAME_WINDOW
from random import seed
from random import randint

import atexit
import constants
import numpy as np
import pickle
import pygame.image
import random
import sys
import time
import xlsxwriter

sys.path.insert(0, '../..')

import Leap

#################### HAND POSITION VARIABLES ####################

# The controller object itself.
controller = Leap.Controller()
# The window used to display to the user. Set to none originally so window does not show until user enters their name.
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

################### DATABASE/KNN VARIABLES ####################

# database loaded in from file.
database = pickle.load(open('userData/database.p','rb'))
# userName set to current user's name (raw_input).
userName = ""
# userEntry holds the current user's entry in the database
userEntry = ""
# gold is used to store the users best score
gold = -1
# silver is used to store the users second best score
silver = -1
# bronze is used to store the users third best score
bronze = -1
# k is used for handling the user's hand location.
k = 0
# clf is our classifier for our machine learning algorithm (knn).
clf = pickle.load(open('userData/classifier.p','rb'))
# testData is our test data for the knn algorithm.
testData = np.zeros((1,30),dtype='f')

################### PROGRAM LOGIC VARIABLES ###################

# programState is used to transition between stages of the program.
programState = 0
# countForHandPos is used to track the hand position during program state 1.
countForHandPos = 0
# toggleHandColor: True = green, False = black.
toggleHandColor = False
# countForCorrectSign increments when the user's sign matches the displayed sign, and is reset when it reaches 10 (switches to programState 3).
countForCorrectSign = 0
# displayNewDigit is used within HandleState2 to decide whether or not to display a new digit to the user.
displayNewDigit = True
# digitToSign is set randomly to a digit for the user to sign.
digitToSign = -1
# displayInstructions is a boolean of whether or not to display the instructional image in DrawNumber.
displayInstructions = True
# tempDisplayInstructions is used to show user the image when they are struggling to sign it while images are not being shown.
tempDisplayInstructions = False
#numCounter is used to track when to display that the user has failed the current digit (if it is greater than timeAllowedPerNumber).
numCounter = 0
# timeAllowedPerNumber holds the amount of iterations before a failure.
timeAllowedPerNumber = 160
# counterForSuccessDisplay iterates every time success is displayed to the user, up until 20, then a new digit is shown to the user.
counterForSuccessDisplay = 0
# counterForFailureDisplay iterates every time failure is displayed to the user, up until 20, then a new digit is shown to the user.
counterForFailureDisplay = 0
# iterationsForSuccess stores the number of times iterated through HandleState3 that the success should be displayed until going back to a different program state.
iterationsForSuccess = 20
# iterationsForFailure stores the number of times iterated through HandleState4 that the failure should be displayed until going back to a different program state.
iterationsForFailure = 20
# iterationsThroughAllDigits tracks how many times the user has gone through each digit. After 2 iterations, instructions stop showing. After one more iteration, PS 5.
iterationsThroughAllDigits = 0
# iterationsThroughTutorial tracks how many times the user has gone through the tutorial.
iterationsThroughTutorial = 0
# iterationsThroughTutorialWithImage is compared with iterationsThroughAllDigits to decide how many times the user has to go through the digits in the tutorial with images.
iterationsThroughTutorialWithImage = 2
# iterationsThroughTutorialWithoutImage is compared with iterationsThroughAllDigits to decide how many times the user has to go through the digits in the tutorial without images.
iterationsThroughTutorialWithoutImage = 3
# initialTutorialLoop is set to True when it is the first program loop through programState 5.
initialTutorialLoop = True

# countForTutorial keeps a count of iterations before program goes to the tutorial
countForTutorial = 0
# countForGame keeps a count of iterations before program goes to the game
countForGame = 0

# countForClockBeforeGame is an integer value used to hold the countdown value.
countForClockBeforeGame = 5
# beforeGameCountDownFirstIteration tracks whether it is the first iteration through programState 5.
beforeGameCountDownFirstIteration = True
# startTickForCountDown is the beginning tick value when program first enters state 5.
startTickForCountDown = pygame.time.get_ticks()
# previousSeconds holds the last integer seconds value for the countDown.
previousSeconds = 0

# countForClockDuringGame is an integer value used to hold the countdown value during the game.
countForClockDuringGame = 60
# duringGameCountDownFirstIteration tracks whether it is the first iteration through programState 6.
duringGameCountDownFirstIteration = True

# arithmaticStage tracks whether the user has made it to the arithmatic stage or not.
arithmaticStage = False
# correctAnswerForArithmatic stores the current value that the user should sign to answer the arithmatic shown.
correctAnswerForArithmatic = 0
# previousCorrectAnswerForArithmatic stores the previous value that the user had to sign to answer the arithmatic shown.
previousCorrectAnswerForArithmatic = 0
# arithmaticMaxNumber holds the maximum number that will be displayed to the user for the current game.
arithmaticMaxNumber = 5
# additionOrSubtraction tracks which operator to use for the arithmatic stage (0 = addition, 1 = subtraction).
additionOrSubtraction = 0
# firstNumForArithmatic stores the first value of the equation.
firstNumForArithmatic = 0
# secondNumForArithmatic stores the seconds value of the equation.
secondNumForArithmatic = 0
# score holds the score of the current game
score = 0

# countForScoreboard is an integer value used to hold the count for displaying the scoreboard.
countForScoreboard = 0

#################### PERFORMANCE DATA VARIABLES ####################

# programTicker is used to track time spent in each programState.
programTicker = 0
# previousTicks stores the number of ticks up to the previous program state switch.
previousTicks = 0
# previousProgramState stores the last programState the user was in.
previousProgramState = -1

################### FUNCTIONS ####################

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

    pygameWindow.Draw_Line(baseX, baseZ + 150, tipX, tipZ + 150, 3 - bone.type, toggleHandColor)

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
            return
        elif(x > 400):
            pygameWindow.Draw_Instruction_Left()
            countForHandPos = 0
            return

        if(y < 100):
            pygameWindow.Draw_Instruction_Up()
            countForHandPos = 0
            return
        elif(y > 250):
            pygameWindow.Draw_Instruction_Down()
            countForHandPos = 0
            return

        if(z < 0):
            pygameWindow.Draw_Instruction_In()
            countForHandPos = 0
            return
        elif(z > 100):
            pygameWindow.Draw_Instruction_Out()
            countForHandPos = 0
            return
        else:
            pygameWindow.Draw_Instruction_Success()
            countForHandPos += 1

# HandOverDevice determines whether a hand is over the device (True, False)
def HandOverDevice(frame):
    if(len(frame.hands) > 0):
        return True
    return False

def DrawNumber(num):
    global pygameWindow, displayInstructions

    if(num == 0):
        pygameWindow.Draw0()
        if(displayInstructions == True or tempDisplayInstructions == True):
            pygameWindow.Draw0Num()
    elif(num == 1):
        pygameWindow.Draw1()
        if(displayInstructions == True or tempDisplayInstructions == True):
            pygameWindow.Draw1Num()
    elif(num == 2):
        pygameWindow.Draw2()
        if(displayInstructions == True or tempDisplayInstructions == True):
            pygameWindow.Draw2Num()
    elif(num == 3):
        pygameWindow.Draw3()
        if(displayInstructions == True or tempDisplayInstructions == True):
            pygameWindow.Draw3Num()
    elif(num == 4):
        pygameWindow.Draw4()
        if(displayInstructions == True or tempDisplayInstructions == True):
            pygameWindow.Draw4Num()
    elif(num == 5):
        pygameWindow.Draw5()
        if(displayInstructions == True or tempDisplayInstructions == True):
            pygameWindow.Draw5Num()
    elif(num == 6):
        pygameWindow.Draw6()
        if(displayInstructions == True or tempDisplayInstructions == True):
            pygameWindow.Draw6Num()
    elif(num == 7):
        pygameWindow.Draw7()
        if(displayInstructions == True or tempDisplayInstructions == True):
            pygameWindow.Draw7Num()
    elif(num == 8):
        pygameWindow.Draw8()
        if(displayInstructions == True):
            pygameWindow.Draw8Num()
    elif(num == 9):
        pygameWindow.Draw9()
        if(displayInstructions == True):
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
    Handle_Hand_Position(frame)

    # If hand is correctly over the device for a count of 150, move on to the signing portion of the program.
    if(countForHandPos >= 150):
        if(arithmaticStage == True):
            programState = 5
        else:
            programState = 2

    # If hand is not over device, show instruction to put hand over device.
    if not HandOverDevice(frame):
        programState = 0

# HandleState2 shows the menu and waits for the user to sign
def HandleState2(frame):
    global testData, clf, programState, toggleHandColor, countForTutorial, countForGame

    pygameWindow.Draw_Menu()

    Handle_Frame(frame)

    testData = CenterData(testData)
    predictedClass = clf.Predict(testData)

    if(predictedClass == 1 and HandOverDevice(frame)):
        toggleHandColor = True
        countForTutorial += 1
    elif(predictedClass == 6 and HandOverDevice(frame)):
        toggleHandColor = True
        countForGame += 1
    else:
        toggleHandColor = False
        countForTutorial = 0
        countForGame = 0

    if(countForTutorial >= 10):
        toggleHandColor = False
        countForTutorial = 0
        programState = 5

    if(countForGame >= 10):
        toggleHandColor = False
        countForGame = 0
        programState = 6

# HandleState3 draws success on screen for a count of 20
def HandleState3(frame):
    global programState, counterForSuccessDisplay, iterationsForSuccess, displayInstructions, tempDisplayInstructions

    pygameWindow.Draw_Instruction_Success()
    Handle_Frame(frame)

    if(counterForSuccessDisplay >= iterationsForSuccess):
        programState = 5
        counterForSuccessDisplay = 0

        if(displayInstructions == False):
            tempDisplayInstructions = False

    counterForSuccessDisplay += 1

# HandleState4 draws failure on screen for a count of 20
def HandleState4(frame):
    global programState, counterForFailureDisplay, iterationsForFailure, displayInstructions, tempDisplayInstructions

    pygameWindow.Draw_Instruction_Failure()
    Handle_Frame(frame)

    if(counterForFailureDisplay >= iterationsForFailure):
        programState = 5
        counterForFailureDisplay = 0

        if(displayInstructions == False):
            tempDisplayInstructions = True

    counterForFailureDisplay += 1

# HandleState5 is the tutorial phase of the program
def HandleState5(frame):
    global digitToSign, displayNewDigit, testData, clf, numCounter, timeAllowedPerNumber, countForCorrectSign, programState, toggleHandColor, iterationsThroughAllDigits, iterationsThroughTutorial, iterationsThroughTutorialWithImage, iterationsThroughTutorialWithoutImage, displayInstructions, initialTutorialLoop

    if(initialTutorialLoop == True):
        displayNewDigit = True
        initialTutorialLoop = False

    if(displayNewDigit == True):
        if(digitToSign == 9):
            digitToSign = 0
            iterationsThroughAllDigits += 1
            if(iterationsThroughAllDigits == iterationsThroughTutorialWithImage):
                displayInstructions = False
                Handle_Frame(frame)
                digitToSign = -1
                return
            elif(iterationsThroughAllDigits == iterationsThroughTutorialWithoutImage):
                digitToSign = -1
                displayNewDigit = True
                iterationsThroughAllDigits = 0
                iterationsThroughTutorial += 1
                initialTutorialLoop = True

                if(iterationsThroughTutorialWithImage > 0):
                    iterationsThroughTutorialWithImage -= 1
                    iterationsThroughTutorialWithoutImage -= 1

                if(iterationsThroughTutorialWithImage == 0):
                    displayInstructions = False
                else:
                    displayInstructions = True

                programState = 2
                Handle_Frame(frame)
                return
        else:
            digitToSign += 1
        displayNewDigit = False
        countForCorrectSign = 0
        numCounter = 0

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

    # Display failure if numCounter is greater than or equal to timeAllowedPerNumber
    if(numCounter >= timeAllowedPerNumber and predictedClass != digitToSign):
        numCounter = 0
        programState = 4

    # Display success if sign is correct for a count of 10
    if(countForCorrectSign >= 10):
        toggleHandColor = False
        displayNewDigit = True
        programState = 3

    numCounter += 1

# HandleState6 is the countdown before the game
def HandleState6(frame):
    global countForClockBeforeGame, beforeGameCountDownFirstIteration, startTickForCountDown, previousSeconds, programState, arithmaticStage

    Handle_Frame(frame)

    if(beforeGameCountDownFirstIteration == True):
        startTickForCountDown = pygame.time.get_ticks()
        beforeGameCountDownFirstIteration = False

    if(countForClockBeforeGame >= 1):
        pygameWindow.Display_CountDown(countForClockBeforeGame)
        seconds = int((pygame.time.get_ticks() - startTickForCountDown) / 1000)
        if(seconds != previousSeconds):
            previousSeconds = seconds
            countForClockBeforeGame -= 1
    elif(countForClockBeforeGame == 0):
        pygameWindow.Display_CountDown("Go!")
        seconds = int((pygame.time.get_ticks() - startTickForCountDown) / 1000)
        if(seconds != previousSeconds):
            countForClockBeforeGame -= 1
    else:
        programState = 7
        previousSeconds = 0
        countForClockBeforeGame = 5
        beforeGameCountDownFirstIteration = True
        arithmaticStage = True

# HandleState7 is the actual game
def HandleState7(frame):
    global countForClockDuringGame, duringGameCountDownFirstIteration, startTickForCountDown, previousSeconds, displayNewDigit, correctAnswerForArithmatic, previousCorrectAnswerForArithmatic, additionOrSubtraction, firstNumForArithmatic, secondNumForArithmatic, numCounter, countForCorrectSign, testData, clf, toggleHandColor, programState, timeAllowedPerNumber, arithmaticStage, arithmaticMaxNumber, score

    # Timer part
    if(duringGameCountDownFirstIteration == True):
        startTickForCountDown = pygame.time.get_ticks()
        duringGameCountDownFirstIteration = False

    if(countForClockDuringGame >= 0):
        pygameWindow.Display_Game_CountDown(countForClockDuringGame)
        seconds = int((pygame.time.get_ticks() - startTickForCountDown) / 1000)
        if(seconds != previousSeconds):
            previousSeconds = seconds
            countForClockDuringGame -= 1
    else:
        programState = 8
        previousSeconds = 0
        numCounter = 0
        countForClockDuringGame = 60
        duringGameCountDownFirstIteration = True
        toggleHandColor = False
        LogScore()
        return

    # Arithmatic part
    if(displayNewDigit == True):
        while(correctAnswerForArithmatic == previousCorrectAnswerForArithmatic or correctAnswerForArithmatic > arithmaticMaxNumber):
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

        previousCorrectAnswerForArithmatic = correctAnswerForArithmatic
        countForCorrectSign = 0
        displayNewDigit = False
        numCounter = 0

    pygameWindow.DrawArithmatic(additionOrSubtraction, firstNumForArithmatic, secondNumForArithmatic)
    pygameWindow.Display_Score_During_Game(score)
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
        countForCorrectSign = 0
        score += 100

    # Display failure if sign is incorrect for the amount of time allowed per number.
    if(numCounter >= timeAllowedPerNumber):
        if(predictedClass != correctAnswerForArithmatic):
            numCounter = 0

    numCounter += 1

# HandleState8 displays the scoreboard
def HandleState8(frame):
    global gold, silver, bronze, programState, countForScoreboard, score, arithmaticMaxNumber

    Handle_Frame(frame)
    pygameWindow.Display_Game_End(gold, silver, bronze, score)

    if(countForScoreboard >= 140):

        if(score >= 1600 and arithmaticMaxNumber < 9):
            arithmaticMaxNumber += 1

        programState = 2
        score = 0
        countForScoreboard = 0

    countForScoreboard += 1

# HandleDatabase is called to start the program
def HandleDatabase():
    global database, userName, userEntry, arithmaticMaxNumber, gold, silver, bronze

    userName = raw_input('Please enter your name: ')

    if userName in database:
        print('Welcome back, ' + userName + '.')
        userEntry = database[userName]
        numLogins = userEntry['logins']
        numLogins += 1
        userEntry['logins'] = numLogins

        arithmaticMaxNumber = userEntry['arithmaticMaxNumber']

        gold = userEntry['gold']
        silver = userEntry['silver']
        bronze = userEntry['bronze']

    else:
        print('Welcome, ' + userName + '.')
        database[userName] = {'logins':1}
        userEntry = database[userName]

        userEntry['arithmaticMaxNumber'] = arithmaticMaxNumber

        userEntry['gold'] = -1
        userEntry['silver'] = -1
        userEntry['bronze'] = -1

        userEntry['s0visits'] = 0
        userEntry['s1visits'] = 0
        userEntry['s2visits'] = 0
        userEntry['s5visits'] = 0
        userEntry['s6visits'] = 0
        userEntry['s7visits'] = 0
        userEntry['s8visits'] = 0

        userEntry['s0mean'] = 0
        userEntry['s1mean'] = 0
        userEntry['s2mean'] = 0
        userEntry['s5mean'] = 0
        userEntry['s6mean'] = 0
        userEntry['s7mean'] = 0
        userEntry['s8mean'] = 0

# LogScore logs the user's most recent game score (if it is gold, silver or bronze).
def LogScore():
    global score, userEntry, gold, silver, bronze

    if score > gold:
        bronze = silver
        silver = gold
        gold = score
    elif score > silver:
        bronze = silver
        silver = score
    elif score > bronze:
        bronze = score

    userEntry['gold'] = gold
    userEntry['silver'] = silver
    userEntry['bronze'] = bronze

def LogPerformanceData():
    global programState, previousProgramState, programTicker, previousTicks, userEntry, score

    # Get current ticks since program start
    programTicker = pygame.time.get_ticks()

    # Get time spent in programState
    timeSpent = (programTicker - previousTicks) / 1000

    # If current state is not equal to previous state, set variables and log data
    if programState != previousProgramState and previousProgramState != -1:

        # Get user data from database about number of visits to current state
        stateVisits = userEntry['s' + str(previousProgramState) + 'visits']

        # Get user data from database about mean time spent in previous state and add current time spent
        stateCumulativeMean = userEntry['s' + str(previousProgramState) + 'mean']
        stateCumulativeMean += timeSpent

        # Calculate mean time spent in current state
        meanTime = stateCumulativeMean/(stateVisits + 1)

        # Increment stateVisits and update database with stateVisits and stateCumulativeMean
        stateVisits += 1
        userEntry['s' + str(previousProgramState) + 'visits'] = stateVisits
        userEntry['s' + str(previousProgramState) + 'mean'] = stateCumulativeMean

        # Enter time spent in new entry (state_visit#)
        userEntry['s' + str(previousProgramState) + '_' + str(stateVisits)] = timeSpent

        # If previousProgramState is 7, log score.
        if previousProgramState == 7:

            userEntry['score' + str(stateVisits)] = score

        # Print information to terminal
        currentStateInfo = str('%.2f' % timeSpent) + "s in s" + str(previousProgramState) + "."
        meanStateInfo = "Mean t in s" + str(previousProgramState) + " for curr user: " + str('%.2f' % meanTime) + "s."
        print('%-20s%-40s' % (currentStateInfo, meanStateInfo))

        # Set variables
        previousTicks = programTicker
        previousProgramState = programState

    elif previousProgramState == -1:

        # Set variables
        previousTicks = programTicker
        previousProgramState = programState

    else:

        # Get user data from database about number of visits to current state
        stateVisits = userEntry['s' + str(programState) + 'visits']

        # Get user data from database about mean time spent in previous state and add current time spent
        stateCumulativeMean = userEntry['s' + str(programState) + 'mean']
        stateCumulativeMean += timeSpent

        # Calculate mean time spent in current state
        meanTime = stateCumulativeMean/(stateVisits + 1)

        # Print information to terminal
        currentStateInfo = str('%.2f' % timeSpent) + "s in s" + str(programState) + "."
        meanStateInfo = "Mean t in s" + str(programState) + " for curr user: " + str('%.2f' % meanTime) + "s."
        print('%-20s%-40s' % (currentStateInfo, meanStateInfo))

# exportToExcel is used to write collected performance data to an excel file.
def exportToExcel():
    global userEntry

    logins = userEntry['logins']
    workbookName = 'performanceData/' + str(userName) + str(logins) + '.xlsx'

    workbook = xlsxwriter.Workbook(workbookName)
    bold = workbook.add_format({'bold': True})

    for stateNum in range(0, 9):
        # Do not write data for states 3 and 4 (no data collected)
        if(stateNum != 3 and stateNum != 4):
            # Create necessary variables
            stateTitle = 's' + str(stateNum)
            numVisits = userEntry[stateTitle + 'visits']

            # Create worksheet and headers
            worksheet = workbook.add_worksheet(stateTitle)
            worksheet.write('A1', 'Visit #', bold)
            worksheet.write('B1', 'Time Spent', bold)

            # For every visit to the current state
            for visitNum in range(1, numVisits + 1):
                # Create necessary variables
                dbEntry = stateTitle + '_' + str(visitNum)
                timeSpent = userEntry[dbEntry]

                # Write to the file
                worksheet.write(visitNum, 0, dbEntry)
                worksheet.write(visitNum, 1, timeSpent)

                # Write score if stateNum == 8
                if(stateNum == 8):
                    scoreNum = 'score' + str(visitNum)
                    score = userEntry[scoreNum]
                    worksheet.write(visitNum, 6, scoreNum)
                    worksheet.write(visitNum, 7, score)

            # Handle mean if numVisits != 0
            if(numVisits != 0):
                # Calculate mean
                cumulativeMean = userEntry[stateTitle + 'mean']
                mean = cumulativeMean / numVisits

                # Write mean to file
                worksheet.write('D2', 'Mean Time Spent', bold)
                worksheet.write('D3', mean)




    workbook.close()

# exit_handler is called on exit of program, saves user data (percentSuccess, totalPercentage)
def exit_handler():
    global userEntry, arithmaticMaxNumber

    userEntry['arithmaticMaxNumber'] = arithmaticMaxNumber

    exportToExcel()
    pickle.dump(database, open('userData/database.p','wb'))

atexit.register(exit_handler)

#################### LOCAL CODE ####################

HandleDatabase()

while True:

    pygameWindow.Prepare()
    frame = controller.frame()
    k = 0

    if programState != 3 and programState != 4:
        LogPerformanceData()

    if programState == 0:
        HandleState0(frame)
    elif programState == 1:
        HandleState1(frame)
    elif programState == 2:
        HandleState2(frame)
    elif programState == 3:
        HandleState3(frame)
    elif programState == 4:
        HandleState4(frame)
    elif programState == 5:
        HandleState5(frame)
    elif programState == 6:
        HandleState6(frame)
    elif programState == 7:
        HandleState7(frame)
    elif programState == 8:
        HandleState8(frame)

    pygameWindow.Reveal()

    # Press 'x' key to exit game at any point.
    keys = pygame.key.get_pressed()

    if(keys[pygame.K_x]):
        pygame.display.quit()
        pygame.quit()
        sys.exit()
