#!/usr/bin/env python3
"""
Haunts the exif data of an image,
poisoning and anonymizing it with random values to protect against doxing.
"""
from PIL import Image, ExifTags, TiffImagePlugin
import csv
import datetime
import random
import math
import sys

def scramble(a, b, c=0):
    """
    Returns a random number in a range, rounded to c decimal places
    and formatted to PIL's IFDRational data type.
    """
    return TiffImagePlugin.IFDRational(round(random.uniform(a, b), c))

def warp():
    """
    Time travel! Returns a random date stamp.
    """
    a = datetime.datetime(2020, 1, 1)
    b = datetime.datetime.now()
    c = b - a
    return (a + datetime.timedelta(random.randrange(c.days))).strftime("%Y:%m:%d")

if __name__ == "__main__":
    for fname in sys.argv[1:]:
        print(f"O{''.join(random.choice(['O', 'o']) for i in range(random.randint(5, 25)))}! Haunting {fname}!")
        img = Image.open(fname)

        exif = img.getexif()
        exif2 = exif.get_ifd(ExifTags.IFD.Exif)
        gps = exif.get_ifd(ExifTags.IFD.GPSInfo)

        # generate time and GPS values from scratch
        date = warp()
        time = (scramble(0, 23), scramble(0, 59), scramble(0, 59))
        _datetime = "%s %02d:%02d:%02d" % (date, *time)

        exif[ExifTags.Base.DateTime.value] = _datetime
        exif2[ExifTags.Base.DateTimeOriginal.value] = _datetime
        exif2[ExifTags.Base.DateTimeDigitized.value] = _datetime

        gps[ExifTags.GPS.GPSLatitudeRef] = random.choice(["N", "S"])
        gps[ExifTags.GPS.GPSLatitude] = (scramble(0, 90), scramble(0, 59), scramble(0, 59, 2))
        gps[ExifTags.GPS.GPSLongitudeRef] = random.choice(["W", "E"])
        gps[ExifTags.GPS.GPSLongitude] = (scramble(0, 180), scramble(0, 59), scramble(0, 59, 2))
        gps[ExifTags.GPS.GPSAltitudeRef] = random.choice([b'\x00', b'\x01']) # above or below sea level
        gps[ExifTags.GPS.GPSAltitude] = scramble(0, 100, 2)
        gps[ExifTags.GPS.GPSImgDirectionRef] = random.choice(["T", "M"]) # true north or magnetic north
        gps[ExifTags.GPS.GPSImgDirection] = scramble(0, 360, 2)
        gps[ExifTags.GPS.GPSDestBearingRef] = gps[ExifTags.GPS.GPSImgDirectionRef]
        gps[ExifTags.GPS.GPSDestBearing] = gps[ExifTags.GPS.GPSImgDirection]
        gps[ExifTags.GPS.GPSTimeStamp] = time
        gps[ExifTags.GPS.GPSDateStamp] = date
        gps[ExifTags.GPS.GPSHPositioningError] = scramble(0, 50, 2)

        # drop MakerNote completely because it contains
        # a significant amount of identifying information
        if ExifTags.Base.MakerNote in exif2:
            del exif2[ExifTags.Base.MakerNote]

        # replace other fields with a random set of existing known values
        with open("data.csv", mode='r', encoding='ISO-8859-1') as f:
            reader = csv.DictReader(f, dialect='unix')
            data = random.choice([r for r in reader])
            for k, v in data.items():
                _k = ExifTags.Base[k].value
                if v != "":
                    exif[_k] = v
                    exif2[_k] = v
                else:
                    if _k in exif:
                        del exif[_k]
                    if _k in exif2:
                        del exif2[_k]

        # printouts for inspection by the user
        for k, v in gps.items():
            for i in ExifTags.GPS:
                if i.value == k:
                    print(i, v)

        for k, v in exif2.items():
            for i in ExifTags.Base:
                if i.value == k:
                    print(i, v)

        for k, v in exif.items():
            if k in ExifTags.TAGS:
                print(f"{ExifTags.TAGS[k]}: {v}")

        img.save(f"_{fname}", exif=exif)
