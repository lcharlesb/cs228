import pickle
import numpy as nm

class READER:

    def __init__(self):
        file = open("./userData/gesture1.p", "rb")
        gestureData = pickle.load(file)
        file.close()

        print(gestureData)
