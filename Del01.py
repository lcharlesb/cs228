from __future__ import division
import sys
sys.path.insert(0, '..')
import Leap
from pygameWindow import PYGAME_WINDOW
import random
import constants

pygameWindow = PYGAME_WINDOW()

x = 250
y = 250
xMin = 1000.0
xMax = -1000.0
yMin = 1000.0
yMax = -1000.0

def Handle_Frame(frame):
    global x, y, xMin, xMax, yMin, yMax
    hand = frame.hands[0]
    fingers = hand.fingers
    indexFingerList = fingers.finger_type(Leap.Finger.TYPE_INDEX)
    indexFinger = indexFingerList[0]
    distalPhalanx = indexFinger.bone(Leap.Bone.TYPE_DISTAL)
    tip = distalPhalanx.next_joint
    x = int(tip[0])
    y = int(tip[1])
    if(x < xMin):
        xMin = x
    if(x > xMax):
        xMax = x
    if(y < yMin):
        yMin = y
    if(y > yMax):
        yMax = y

def ScaleCoordinates(value, rangeOneLow, rangeOneHigh, rangeTwoLow, rangeTwoHigh):
    rangeOne = abs(rangeOneHigh - rangeOneLow)
    if(rangeOne == 0):
        return rangeTwoLow
    else:
        rangeTwo = abs(rangeTwoHigh - rangeTwoLow)
        return int((((value - rangeOneLow) * rangeTwo) / rangeOne) + rangeTwoLow)

def Perturb_Circle_Position():
    global x, y
    fourSidedDieRoll = random.randint(1,4)
    if(fourSidedDieRoll == 1):
        x -= 1
    elif(fourSidedDieRoll == 2):
        x += 1
    elif(fourSidedDieRoll == 3):
        y -= 1
    else:
        y += 1

controller = Leap.Controller()

pygameX = 0
pygameY = 0

while True:
    #Perturb_Circle_Position()

    pygameWindow.Prepare()
    frame = controller.frame()
    if (len(frame.hands) > 0):
        Handle_Frame(frame)
        pygameX = ScaleCoordinates(x, xMin, xMax, 0, constants.pygameWindowWidth)
        pygameY = ScaleCoordinates(y, yMin, yMax, 0, constants.pygameWindowDepth)
    pygameWindow.Draw_Black_Circle(pygameX,(constants.pygameWindowDepth - pygameY))
    pygameWindow.Reveal()
