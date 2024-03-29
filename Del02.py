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
xMin = -100.0
xMax = 100.0
yMin = -100.0
yMax = 100.0

def Handle_Vector_From_Leap(v):
    global xMin, xMax, yMin, yMax

    x = int(v[0])
    y = int(v[2])

    if(x < xMin):
        xMin = x
    if(x > xMax):
        xMax = x
    if(y < yMin):
        yMin = y
    if(y > yMax):
        yMax = y

    x = ScaleCoordinates(x, xMin, xMax, 0, constants.pygameWindowWidth)
    y = ScaleCoordinates(y, yMin, yMax, 0, constants.pygameWindowDepth)
    return x, y

def Handle_Bone(bone):
    base = bone.prev_joint
    tip = bone.next_joint
    baseX, baseY = Handle_Vector_From_Leap(base)
    tipX, tipY = Handle_Vector_From_Leap(tip)
    pygameWindow.Draw_Black_Line(baseX, baseY, tipX, tipY, 3 - bone.type)

def Handle_Finger(finger):
    for b in range(0,4):
        Handle_Bone(finger.bone(b))

def Handle_Frame(frame):
    global x, y, xMin, xMax, yMin, yMax
    hand = frame.hands[0]
    fingers = hand.fingers
    for finger in fingers:
        Handle_Finger(finger)
    pass

def ScaleCoordinates(value, rangeOneLow, rangeOneHigh, rangeTwoLow, rangeTwoHigh):
    diff = value - rangeOneLow
    oldRange = rangeOneHigh - rangeOneLow
    newRange = rangeTwoHigh - rangeTwoLow
    if(oldRange == 0):
        return value
    oldFraction = diff / oldRange
    newValue = oldFraction * newRange
    return newValue

controller = Leap.Controller()

pygameX = 0
pygameY = 0

while True:
    pygameWindow.Prepare()
    frame = controller.frame()
    if (len(frame.hands) > 0):
        Handle_Frame(frame)
    #     pygameX = ScaleCoordinates(x, xMin, xMax, 0, constants.pygameWindowWidth)
    #     pygameY = ScaleCoordinates(y, yMin, yMax, 0, constants.pygameWindowDepth)
    # pygameWindow.Draw_Black_Circle(pygameX,(constants.pygameWindowDepth - pygameY))
    pygameWindow.Reveal()
