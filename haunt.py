#!/usr/bin/env python3
from PIL import Image, ExifTags, TiffImagePlugin
import datetime
import random
import math
import sys

def scramble(a, b, c=0):
    return TiffImagePlugin.IFDRational(round(random.uniform(a, b), c))

def warp():
    a = datetime.datetime(1970, 1, 1)
    b = datetime.datetime.now()
    c = b - a
    return (a + datetime.timedelta(random.randrange(c.days))).strftime("%Y:%m:%d")

fname = sys.argv[1]
img = Image.open(fname)

exif = img.getexif()
gps = exif.get_ifd(ExifTags.IFD.GPSInfo)
gps[ExifTags.GPS.GPSLatitudeRef] = random.choice(["N", "S"])
gps[ExifTags.GPS.GPSLatitude] = (scramble(0, 90), scramble(0, 60, 2), scramble(0, 60, 2))
gps[ExifTags.GPS.GPSLongitudeRef] = random.choice(["W", "E"])
gps[ExifTags.GPS.GPSLongitude] = (scramble(0, 180), scramble(0, 60, 2), scramble(0, 60, 2))
gps[ExifTags.GPS.GPSAltitudeRef] = random.choice([b'\x00', b'\x01'])
gps[ExifTags.GPS.GPSAltitude] = scramble(0, 100, 2)
gps[ExifTags.GPS.GPSImgDirectionRef] = random.choice(["T", "M"])
gps[ExifTags.GPS.GPSImgDirection] = scramble(0, 360, 2)
gps[ExifTags.GPS.GPSDestBearingRef] = gps[ExifTags.GPS.GPSImgDirectionRef]
gps[ExifTags.GPS.GPSDestBearing] = gps[ExifTags.GPS.GPSImgDirection]
gps[ExifTags.GPS.GPSDateStamp] = warp()
gps[ExifTags.GPS.GPSHPositioningError] = scramble(0, 50, 2)

print(gps)
print(exif)

for k, v in gps.items():
    for i in ExifTags.GPS:
        if i.value == k:
            print(i,v)

for k, v in exif.items():
    print(f"Tag: {ExifTags.TAGS[k]}, Value: {v}")

img.save(f"_{fname}", exif=exif)
