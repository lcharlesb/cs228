import pickle
import numpy as nm
import os
from pygameWindow_Del03 import PYGAME_WINDOW
import constants
import time


class READER:

    def __init__(self):
        self.pygameWindow = PYGAME_WINDOW()
        self.Get_Num_Gestures()
        self.Draw_Gestures()

    def Get_Num_Gestures(self):
        path, dirs, files = next(os.walk('userData'))
        self.numGestures = len(files)

    def Print_Gestures(self):
        for i in range(self.numGestures):
            file = open("./userData/gesture" + str(i) + ".p", "rb")
            gestureData = pickle.load(file)
            file.close()
            print(gestureData)

    def Draw_Gestures(self):
        while(True):
            self.Draw_Each_Gesture_Once()

    def Draw_Each_Gesture_Once(self):
        for i in range(self.numGestures):
            self.Draw_Gesture(i)

    def Draw_Gesture(self, g):
        self.pygameWindow.Prepare()
        file = open("./userData/gesture" + str(g) + ".p", "rb")
        gestureData = pickle.load(file)
        file.close()
        for i in range(0,5):
            for j in range(0,4):
                currentBone = gestureData[i, j, 0:6]
                xBaseNotYetScaled = currentBone[0]
                yBaseNotYetScaled = currentBone[2]
                xTipNotYetScaled = currentBone[3]
                yTipNotYetScaled = currentBone[5]
                xBase = self.ScaleCoordinates(xBaseNotYetScaled, constants.xMin, constants.xMax, 0, constants.pygameWindowWidth)
                yBase = self.ScaleCoordinates(yBaseNotYetScaled, constants.yMin, constants.yMax, 0, constants.pygameWindowDepth)
                xTip = self.ScaleCoordinates(xTipNotYetScaled, constants.xMin, constants.xMax, 0, constants.pygameWindowWidth)
                yTip = self.ScaleCoordinates(yTipNotYetScaled, constants.yMin, constants.yMax, 0, constants.pygameWindowDepth)
                self.pygameWindow.Draw_Line((0,0,255), xBase, yBase, xTip, yTip, 2)
        time.sleep(0.5)
        self.pygameWindow.Reveal()

    def ScaleCoordinates(self, value, rangeOneLow, rangeOneHigh, rangeTwoLow, rangeTwoHigh):
        rangeOne = abs(rangeOneHigh - rangeOneLow)
        if(rangeOne == 0):
            return rangeTwoLow
        else:
            rangeTwo = abs(rangeTwoHigh - rangeTwoLow)
            return int((((value - rangeOneLow) * rangeTwo) / rangeOne) + rangeTwoLow)
