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
gps[ExifTags.GPS.GPSLatitudeRef] = random.choice(["N", "S"])
gps[ExifTags.GPS.GPSLatitude] = (scramble(0, 90, 1), scramble(0, 60), scramble(0, 60))
gps[ExifTags.GPS.GPSLongitudeRef] = random.choice(["W", "E"])
gps[ExifTags.GPS.GPSLongitude] = (scramble(0, 180, 1), scramble(0, 60), scramble(0, 60))
print(gps)
print(exif)
print(ExifTags.Base.Make.value)

for k, v in exif.items():
    print(f"Tag: {ExifTags.TAGS[k]}, Value: {v}")

img.save(f"_{fname}", exif=exif)
