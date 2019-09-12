from __future__ import division
import sys
sys.path.insert(0, '..')
import Leap
from pygameWindow_Del03 import PYGAME_WINDOW
import random
import constants
import Deliverable

class DELIVERABLE:

    def __init__(self, controller, pygameWindow, x, y, xMin, xMax, yMin, yMax):
        self.controller = controller
        self.pygameWindow = pygameWindow
        self.x = x
        self.y = y
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax
        pass

    def Run_Forever(self):
        while True:
            self.Run_Once()

    def Run_Once(self):
        self.pygameWindow.Prepare()
        frame = self.controller.frame()
        self.numberOfHands = len(frame.hands)
        if (self.numberOfHands > 0):
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

    def Handle_Bone(self, bone):
        base = bone.prev_joint
        tip = bone.next_joint
        baseX, baseY = self.Handle_Vector_From_Leap(base)
        tipX, tipY = self.Handle_Vector_From_Leap(tip)
        self.pygameWindow.Draw_Black_Line(baseX, baseY, tipX, tipY, 3 - bone.type)

    def Handle_Finger(self, finger):
        for b in range(0,4):
            self.Handle_Bone(finger.bone(b))

    def Handle_Frame(self, frame):
        global x, y, xMin, xMax, yMin, yMax
        hand = frame.hands[0]
        fingers = hand.fingers
        for finger in fingers:
            self.Handle_Finger(finger)
        pass

    def ScaleCoordinates(self, value, rangeOneLow, rangeOneHigh, rangeTwoLow, rangeTwoHigh):
        rangeOne = abs(rangeOneHigh - rangeOneLow)
        if(rangeOne == 0):
            return rangeTwoLow
        else:
            rangeTwo = abs(rangeTwoHigh - rangeTwoLow)
            return int((((value - rangeOneLow) * rangeTwo) / rangeOne) + rangeTwoLow)
