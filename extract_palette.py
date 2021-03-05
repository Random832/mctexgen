# failed experiment
from PIL import Image
import numpy as np
import sys

fn = sys.argv[1]
imgp = Image.open(fn)
imga = np.array(imgp)
if imgp.mode == 'RGBA':
    imga = imga[:,:,:3]
elif imgp.mode != 'RGB':
    print('Image must be an RGB image')
    sys.exit(1)

w,h,c = imga.shape
colors = np.unique(imga.reshape((w*h, c)), axis=0).copy()
colors.resize(((len(colors)+15)//16, 16, 3))

palimg = Image.fromarray(colors, 'RGB')
palimg.save(fn+'_pal.png')
