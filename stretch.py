import numpy as np
from PIL import Image
from .common import TextureReader
import sys
import os
# untested
# for two-frame inputs this should be done with an mcmeta like mojang's lava texture    

def do_convert(srcf, nframe, dstf):
    src = TextureReader(srcf)
    w = src.size
    nframe = int(nframe)

    dsta = np.ndarray((nframe, w, w, src.nchan), np.uint8)
    for iframe in range(nframe):
        fr = src.get_frame(iframe / nframe * src.nframe)
        fr = np.tile(fr, (2, 2, 1))
        dsta[iframe] = fr

    if src.mode == 'L':
        dsta = dsta.reshape((w*nframe, w))
    else:
        dsta = dsta.reshape((w*nframe, w, src.nchan))
    dstp = Image.fromarray(dsta, src.mode)
    dstp.save(dstf)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage:", os.path.basename(sys.argv[0]), "src.png nframes dst.png")
        sys.exit(1)
    do_convert(*sys.argv[1:])

