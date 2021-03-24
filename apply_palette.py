# failes experiment
from PIL import Image
import numpy as np
import sys
import pathlib
from . import palettes

@np.vectorize
def _mul(a, b):
    return np.uint16(a)*b//255

color_warned = False

def load_base_image(filename):
    global color_warned
    filename = pathlib.Path(filename)
    "Returns a tuple of two numpy arrays representing the gray and alpha channels."
    imgp = Image.open(filename)
    alpha = None # np.uint8(255)
    # scalar will be broadcast when used in final calculation
    grays = None
    if imgp.mode in ('RGBA', 'RGB', 'P'):
        print(f'Warning: converting color image {filename.stem} to grayscale.')
        if not color_warned:
            color_warned = True
            print(f'Warning: The meaning of color pixels might change in the future.')
    imgp = imgp.convert('LA')
    imga = np.array(imgp)
    grays = imga[:,:,0]
    alpha = imga[:,:,1]
    return grays, alpha

def apply_palette(srcvalue, srcalpha, palette):
    result = palette[srcvalue]
    if srcalpha is not None:
        result[...,3] = _mul(result[...,3], srcalpha)
    return Image.fromarray(result, 'RGBA')

def main(imgfn, palfn, dstfn):
    grays, alpha = load_base_image(imgfn)
    pal = palettes.load_palette(palfn)
    dstimg = apply_palette(grays, alpha, pal)
    dstimg.save(dstfn)

if __name__ == '__main__':
    main(*sys.argv[1:])
