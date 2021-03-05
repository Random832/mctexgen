# failes experiment
from PIL import Image
import numpy as np
import sys
from . import palettes

@np.vectorize
def _mul(a, b):
    return np.uint16(a)*b//255

def load_base_image(filename):
    "Returns a tuple of two numpy arrays representing the gray and alpha channels."
    imgp = Image.open(filename)
    imga = np.array(imgp)
    alpha = None # np.uint8(255)
    # scalar will be broadcast when used in final calculation
    grays = None
    if imgp.mode in ('RGBA', 'LA'):
        alpha = imga[:,:,-1]
    if imgp.mode in ('RGBA', 'RGB'):
        print(f'Warning: Using green channel of RGB source image {filename!r}. This may change in the future.')
        grays = imga[:,:,1]
    elif imgp.mode == 'LA':
        print('Grayscale source image ^_^')
        grays = imga[:,:,0]
    elif imgp.mode == 'L':
        print('Grayscale source image ^_^')
        grays = imga[:,:]
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
