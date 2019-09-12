from __future__ import division
import sys
sys.path.insert(0, '..')
import Leap
from pygameWindow import PYGAME_WINDOW
import random
import constants
import Deliverable

obj = Deliverable.DELIVERABLE(Leap.Controller(), PYGAME_WINDOW(), 250, 250, -100, 100, -100, 100)
obj.Run_Forever()
