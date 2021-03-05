# failes experiment
from PIL import Image
import numpy as np
import sys
from . import palettes

def main(imgfn, palfn):
    pal = palettes.load_palette(palfn)
    if any(pal[:,3] != 255):
        print('Warning: ignoring alpha values from palette')
    pal = pal[:,:3]
    imgp = Image.open(imgfn).convert('RGBA')
    imga = np.array(imgp)
    src_alpha = imga[:,:,3]
    imga = imga[:,:,:3]
    h, w, c = imga.shape
    assert c == 3
    tmp = imga.astype(np.float32).reshape((h, w, 1, 3))
    pal = pal.reshape(1, 1, len(pal), 3)
    tmp = tmp - pal # huge array, differences to all palette entries
    tmp *= tmp
    tmp = tmp.sum(3) # eliminate fourth axis which is rgb channel
    tmp = tmp.argmin(2).astype(np.uint8)
    print(tmp.shape)
    Image.fromarray(tmp, 'L').save(imgfn+'~gray.png')
    imgout = Image.fromarray(tmp, 'P')
    imgout.putpalette(pal.flatten())
    imgout.save(imgfn+'~reconstructed~indexed.png')
    imgout.convert('RGB').save(imgfn+'~reconstructed~rgb.png')
    

if __name__ == '__main__':
    main(*sys.argv[1:])
