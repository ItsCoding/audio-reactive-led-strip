import numpy as np


class StripFrame:
    def __init__(self, stripIndex: int, stripLength: int):
        self.stripIndex = stripIndex
        self.stripLength = stripLength
        self.leds = np.array([np.tile(0, stripLength), np.tile(0, stripLength), np.tile(0, stripLength)])
    
    def addFrame(self, frame, startIndex: int,endIndex: int):
        # loop trough the three colors and add the frame to the leds array starting at the startIndex
        for i in range(3):
            if endIndex > self.stripLength:
                endIndex = self.stripLength
            np.put(self.leds[i], range(startIndex, endIndex), frame[i][startIndex:endIndex])

    def getLEDS(self):
        return self.leds
