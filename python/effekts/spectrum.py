import config
import numpy as np
import dsp
from scipy.ndimage.filters import gaussian_filter1d

from misc.interpolate import interpolate

class visualize_spectrum:
    def __init__(self,id):
            self.id = id
            # self.p = None
            self.r_filt = None
            self.b_filt = None
            self.common_mode = None
            self._prev_spectrum = None
    def run(self, y,stripSize,gain: dsp.ExpFilter):
        """Effect that maps the Mel filterbank frequencies onto the LED strip"""
        if(self.r_filt is None):
            self._prev_spectrum = np.tile(0.01, config.N_PIXELS // 2)
            self.r_filt = dsp.ExpFilter(np.tile(0.01, config.N_PIXELS // 2),
                       alpha_decay=0.2, alpha_rise=0.99)

            self.b_filt = dsp.ExpFilter(np.tile(0.01, config.N_PIXELS // 2),
                                alpha_decay=0.1, alpha_rise=0.5)

            # self.p = np.tile(1.0, (3, config.N_PIXELS // 2))
            self.common_mode = dsp.ExpFilter(np.tile(0.01, config.N_PIXELS // 2),
                                alpha_decay=0.99, alpha_rise=0.01)


        y = np.copy(interpolate(y, config.N_PIXELS // 2))
        self.common_mode.update(y)
        y = y ** 0.9
        diff = y - self._prev_spectrum
        self._prev_spectrum = np.copy(y)
        # Color channel mappings
        r = self.r_filt.update(y - self.common_mode.value)
        g = np.abs(diff)
        b = self.b_filt.update(np.copy(y))
        # Mirror the color channels for symmetric output
        r = np.concatenate((r[::-1], r))
        g = np.concatenate((g[::-1], g))
        b = np.concatenate((b[::-1], b))

        # r = [i for i in r if i > 1]
        # g = [i for i in g if i > 1]
        # b = [i for i in b if i > 1]
        # if(len(r) < 1):
        #     r = np.tile(0, config.N_PIXELS)
        # if(len(g) < 1):
        #     g = np.tile(0, config.N_PIXELS)
        # if(len(b) < 1):
        #     b = np.tile(0, config.N_PIXELS)

        # r = interpolate(r, stripSize)
        # g = interpolate(g, stripSize)
        # b = interpolate(b, stripSize)

        output = np.array([r, g,b]) * 255
        return output