import numpy as np
from PIL import Image
from .common import TextureReader
import sys
import os

def do_convert(srcf, dstf):
    src = TextureReader(srcf)
    w = src.size
    nframe = 16
    px = 1 # pixels down per 16'th of the animation

    dsta = np.ndarray((nframe, w*2, w*2, src.nchan), np.uint8)
    for iframe in range(nframe):
        fr = src.get_frame(iframe / nframe * src.nframe)
        fr = np.roll(fr, w//2, (0, 1)) # center the original texture
        fr = np.roll(fr, iframe*px*w//nframe, 0) # directional flowing
        fr = np.tile(fr, (2, 2, 1))
        dsta[iframe] = fr

    if src.mode == 'L':
        dsta = dsta.reshape((w*nframe*2, w*2))
    else:
        dsta = dsta.reshape((w*nframe*2, w*2, src.nchan))
    dstp = Image.fromarray(dsta, src.mode)
    dstp.save(dstf)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage:", os.path.basename(sys.argv[0]), "src.png dst.png")
        sys.exit(1)
    do_convert(*sys.argv[1:])

