import numpy as np
from PIL import Image
from .common import TextureReader
import sys
import os

def do_convert(srcf, dstf):
    "Generates a simple four-frame animation from a static texture"
    src = TextureReader(srcf)
    w = src.size

    dsta = np.ndarray((4, w, w, src.nchan), np.uint8)
    fr = src.get_frame(0)
    dsta[0] = fr
    dsta[1] = np.rot90(dsta[0], 2)
    dsta[2] = np.roll(dsta[1], w//2, (0, 1))
    dsta[3] = np.rot90(dsta[2], 2)

    dsta = dsta.reshape((w*4, w, src.nchan))
    dstp = Image.fromarray(dsta, src.mode)
    dstp.save(dstf)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage:", os.path.basename(sys.argv[0]), "src.png dst.png")
        sys.exit(1)
    do_convert(*sys.argv[1:])

