import numpy as np
from PIL import Image
import json

def interpolate(frame1, frame2, t):
    if frame1 is frame2: return frame1
    fr = frame1 * (1-t) + frame2 * t
    return np.clip(fr, 0, 255, np.ndarray(fr.shape, np.uint8))

class TextureReader:
    def __init__(self, filename):
        srcp = Image.open(filename)
        array = np.array(srcp)
        if srcp.mode == 'L':
            h, w = array.shape
            c = 1
        else:
            h, w, c = array.shape
        nframe = h//w
        self.array = array.reshape((nframe, w, w, c)) # np.split?
        self.size = w
        self.nchan = c
        self.mode = srcp.mode
        self.metaframes = range(nframe)
        self.interpolate = True
        try:
            meta = json.load(open(filename+'.mcmeta'))
            if 'animation' in meta:
                if 'frames' in meta['animation']:
                    self.metaframes = meta['animation']['frames']
                self.interpolate = meta['animation'].get('interpolate', False)
        except FileNotFoundError:
            pass

    @property
    def nframe(self):
        return len(self.metaframes)

    def get_frame(self, x):
        n, t = divmod(x, 1)
        n = int(n)
        if not t or not self.interpolate:
            return self.array[self.metaframes[n]]
        else:
            n1 = (n+1)%self.nframe
            return interpolate(self.get_frame(n), self.get_frame(n1), t)
