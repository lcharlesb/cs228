from __future__ import division
import sys
sys.path.insert(0, '..')
import Leap
from pygameWindow_Del03 import PYGAME_WINDOW
import random
import constants
import Recorder

obj = Recorder.RECORDER()
obj.Run_Forever()
