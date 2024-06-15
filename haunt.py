#!/usr/bin/env python3
from PIL import Image, ExifTags, TiffImagePlugin
import random
import sys

def scramble(a, b, c=100):
    return TiffImagePlugin.IFDRational(random.randint(a*c, b*c) / c)

fname = sys.argv[1]
img = Image.open(fname)

exif = img.getexif()
gps = exif.get_ifd(ExifTags.IFD.GPSInfo)
gps[1] = random.choice(["N", "S"])
gps[2] = (scramble(0, 90, 1), scramble(0, 60), scramble(0, 60))
gps[3] = random.choice(["W", "E"])
gps[4] = (scramble(0, 180, 1), scramble(0, 60), scramble(0, 60))
print(gps)
print(exif)

for k, v in exif.items():
    print(f"Tag: {ExifTags.TAGS[k]}, Value: {v}")

img.save(f"_{fname}", exif=exif)
