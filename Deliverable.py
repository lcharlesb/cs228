from __future__ import division
import sys
sys.path.insert(0, '..')
import Leap
from pygameWindow_Del03 import PYGAME_WINDOW
import random
import constants
import Deliverable
import numpy as np

class DELIVERABLE:

    def __init__(self):
        self.controller = Leap.Controller()
        self.pygameWindow = PYGAME_WINDOW()
        self.x = 250
        self.y = 250
        self.xMin = -100.0
        self.xMax = 100.0
        self.yMin = -100.0
        self.yMax = 100.0
        self.previousNumberOfHands = 0
        self.currentNumberOfHands = 0
        self.gestureData = np.zeros((5,4,6),dtype='f')
        pass

    def Run_Forever(self):
        while True:
            self.Run_Once()
            self.previousNumberOfHands = self.currentNumberOfHands

    def Run_Once(self):
        self.pygameWindow.Prepare()
        frame = self.controller.frame()
        self.currentNumberOfHands = len(frame.hands)
        if (self.currentNumberOfHands > 0):
            self.Handle_Frame(frame)
        #     pygameX = ScaleCoordinates(x, xMin, xMax, 0, constants.pygameWindowWidth)
        #     pygameY = ScaleCoordinates(y, yMin, yMax, 0, constants.pygameWindowDepth)
        # pygameWindow.Draw_Black_Circle(pygameX,(constants.pygameWindowDepth - pygameY))
        self.pygameWindow.Reveal()

    def Handle_Vector_From_Leap(self, v):
        x = self.ScaleCoordinates(int(v[0]), self.xMin, self.xMax, 0, constants.pygameWindowWidth)
        y = self.ScaleCoordinates(int(v[2]), self.yMin, self.yMax, 0, constants.pygameWindowDepth)
        if(x < self.xMin):
            self.xMin = x
        if(x > self.xMax):
            self.xMax = x
        if(y < self.yMin):
            self.yMin = y
        if(y > self.yMax):
            self.yMax = y
        return x, y

    def Handle_Bone(self, bone, finger):
        base = bone.prev_joint
        tip = bone.next_joint
        baseX, baseY = self.Handle_Vector_From_Leap(base)
        tipX, tipY = self.Handle_Vector_From_Leap(tip)
        color = (0,0,0)
        if(self.currentNumberOfHands == 1):
            color = (0,255,0)
        elif(self.currentNumberOfHands == 2):
            color = (255,0,0)
        self.pygameWindow.Draw_Line(color, baseX, baseY, tipX, tipY, 3 - bone.type)
        if self.Recording_Is_Ending():
            self.gestureData[finger, bone.type, 0] = base[0]
            self.gestureData[finger, bone.type, 1] = base[1]
            self.gestureData[finger, bone.type, 2] = base[2]
            self.gestureData[finger, bone.type, 3] = tip[0]
            self.gestureData[finger, bone.type, 4] = tip[1]
            self.gestureData[finger, bone.type, 5] = tip[2]

    def Handle_Finger(self, finger):
        for b in range(0,4):
            self.Handle_Bone(finger.bone(b), finger.type)

    def Handle_Frame(self, frame):
        global x, y, xMin, xMax, yMin, yMax
        hand = frame.hands[0]
        fingers = hand.fingers
        for finger in fingers:
            self.Handle_Finger(finger)
        if self.Recording_Is_Ending():
            print(self.gestureData)
        pass

    def ScaleCoordinates(self, value, rangeOneLow, rangeOneHigh, rangeTwoLow, rangeTwoHigh):
        rangeOne = abs(rangeOneHigh - rangeOneLow)
        if(rangeOne == 0):
            return rangeTwoLow
        else:
            rangeTwo = abs(rangeTwoHigh - rangeTwoLow)
            return int((((value - rangeOneLow) * rangeTwo) / rangeOne) + rangeTwoLow)

    def Recording_Is_Ending(self):
        if(self.currentNumberOfHands == 1 and self.previousNumberOfHands == 2):
            return True
        return False
