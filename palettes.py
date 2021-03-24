import numpy as np
import re

def match_hex(m):
    r = int(m.group(1), 16)
    g = int(m.group(2), 16)
    b = int(m.group(3), 16)
    return r, g, b, 255

def match_rgb(m):
    r = int(m.group(1))
    g = int(m.group(2))
    b = int(m.group(3))
    return r, g, b, 255

def match_rgba(m):
    r = int(m.group(1))
    g = int(m.group(2))
    b = int(m.group(3))
    a = int(m.group(4))
    return r, g, b, a

parsefuncs = [
        ('#([\da-f][\da-f])([\da-f][\da-f])([\da-f][\da-f])', match_hex),
        ('rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', match_rgb),
        ('rgba\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', match_rgba),
        ]

def isempty(s):
    'Returns true if the string contains only whitespace or a comment'
    s = s.strip()
    return s == '' or s.startswith('#')

def build_palette(d):
    if 0 not in d:
        d[0] = (0,0,0,255)
    if 255 not in d:
        d[255] = (255,255,255,255)
    pal = np.ndarray((256, 4), np.uint8)
    pal[:,0]=range(256)
    pal[:,1]=range(256)
    pal[:,2]=range(256)
    pal[:,3]=255
    l = [*d.keys()]
    l.sort()
    for c0, c1 in zip(l, l[1:]):
        r0, g0, b0, a0 = d[c0]
        r1, g1, b1, a1 = d[c1]
        pal[c0:c1+1, 0] = np.linspace(r0, r1, c1-c0+1, dtype=np.uint8)
        pal[c0:c1+1, 1] = np.linspace(g0, g1, c1-c0+1, dtype=np.uint8)
        pal[c0:c1+1, 2] = np.linspace(b0, b1, c1-c0+1, dtype=np.uint8)
        pal[c0:c1+1, 3] = np.linspace(a0, a1, c1-c0+1, dtype=np.uint8)
    return pal

def load_palette_txt(filename):
    d = {}
    for line in open(filename):
        if isempty(line):
            continue
        m = re.match('\s*(\d+|0x[\da-f]+)\s*:\s*', line, re.I)
        if m:
            i = int(m.group(1))
            line = line[m.end(0):]
            for r, f in parsefuncs:
                m = re.match(r, line)
                if m:
                    junk = line[m.end(0):]
                    if not isempty(junk):
                        print(f'Warning: Ignoring junk {junk!r} after end of line in palette file {filename}')
                    rgba = f(m)
                    #print(f'{i}: rgba{rgba}')
                    d[i] = rgba
                    continue
        else:
            print(f'Warning: Ignoring unknown line {line!r} in palette file {filename}')
    return build_palette(d)
