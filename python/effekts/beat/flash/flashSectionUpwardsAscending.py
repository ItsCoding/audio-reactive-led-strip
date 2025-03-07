import random
import time
from config import config
import numpy as np
import dsp
from scipy.ndimage.filters import gaussian_filter1d



class visualize_flashSectionUpwardsAscending:
    def __init__(self,id):
        self.id = id
        self.p = None
        self.p_filt = None
        
        self.lastFlash = 0
        self.position = 0
        self.description = {
            "name": "Flash Section Upwards ascending",
            "description": "A effekt that flash a section when beat changes",
            "effektSystemName": "visualize_flashSectionUpwardsAscending",
            "group": "beat-flash",
            "groupColor": "#FFFEE",
            "bpmSensitive": True,
            "supports": ["color","intensity"],
        }

    def run(self, y,stripSize,gain: dsp.ExpFilter,instanceData: dict = {}):
        """Effect that expands from the center with increasing sound energy"""
        # global p, p_filt
        self.rgbColor = instanceData["colorDict"][0]
        if(self.p is None):
            self.p = np.tile(0, (3, stripSize // 2))
            self.p_filt =  dsp.ExpFilter(np.tile(1, (3, stripSize // 2)),
                        alpha_decay=0.1, alpha_rise=0.99)

        if "color" in instanceData:
            self.rgbColor = instanceData["color"]

        if "beatChanged" in instanceData:
            if instanceData["beatChanged"]:
                self.p = np.tile(0, (3, stripSize//2))
                self.lastFlash = int(round(time.time() * 1000))
                randPos = self.position
                randEnd = int(((stripSize // 2) / 8) * randPos)
                self.p[0][0: randEnd] = self.rgbColor[0]
                self.p[1][0: randEnd] = self.rgbColor[1]
                self.p[2][0: randEnd] = self.rgbColor[2]
                self.p[0, :] = gaussian_filter1d(self.p[0, :], sigma=4.0)
                self.p[1, :] = gaussian_filter1d(self.p[1, :], sigma=4.0)
                self.p[2, :] = gaussian_filter1d(self.p[2, :], sigma=4.0)
                self.position = self.position + 1
                if(self.position >= 8):
                    self.position = 0
                # print(self.p)
        if self.lastFlash + (60000/((instanceData["bpm"]+1))) - 250 < int(round(time.time() * 1000)):
            self.p = np.tile(0, (3, stripSize//2))
        output = np.concatenate((self.p,self.p[:, ::-1]), axis=1)
        return output
