#!/usr/bin/env python3
"""
Haunts the exif data of an image,
poisoning and anonimizing it with random values to protect against doxing.
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

# time travel! generates a random date stamp
def warp():
    """
    Time travel! Returns a random date stamp.
    """
    a = datetime.datetime(1970, 1, 1)
    b = datetime.datetime.now()
    c = b - a
    return (a + datetime.timedelta(random.randrange(c.days))).strftime("%Y:%m:%d")

if __name__ == "__main__":
    for fname in sys.argv[1:]:
        print(f"O{''.join(random.choice(['O', 'o']) for i in range(random.randint(5, 25)))}! Haunting {fname}!")
        img = Image.open(fname)

        date = warp()
        time = (scramble(0, 24), scramble(0, 60), scramble(0, 60))

        exif = img.getexif()
        gps = exif.get_ifd(ExifTags.IFD.GPSInfo)
        gps[ExifTags.GPS.GPSLatitudeRef] = random.choice(["N", "S"])
        gps[ExifTags.GPS.GPSLatitude] = (scramble(0, 90), scramble(0, 60), scramble(0, 60, 2))
        gps[ExifTags.GPS.GPSLongitudeRef] = random.choice(["W", "E"])
        gps[ExifTags.GPS.GPSLongitude] = (scramble(0, 180), scramble(0, 60), scramble(0, 60, 2))
        gps[ExifTags.GPS.GPSAltitudeRef] = random.choice([b'\x00', b'\x01'])
        gps[ExifTags.GPS.GPSAltitude] = scramble(0, 100, 2)
        gps[ExifTags.GPS.GPSImgDirectionRef] = random.choice(["T", "M"])
        gps[ExifTags.GPS.GPSImgDirection] = scramble(0, 360, 2)
        gps[ExifTags.GPS.GPSDestBearingRef] = gps[ExifTags.GPS.GPSImgDirectionRef]
        gps[ExifTags.GPS.GPSDestBearing] = gps[ExifTags.GPS.GPSImgDirection]
        gps[ExifTags.GPS.GPSTimeStamp] = time
        gps[ExifTags.GPS.GPSDateStamp] = date
        gps[ExifTags.GPS.GPSHPositioningError] = scramble(0, 50, 2)
        exif[ExifTags.Base.DateTime.value] = "%s %02d:%02d:%02d" % (date, *time)

        for k, v in gps.items():
            for i in ExifTags.GPS:
                if i.value == k:
                    print(i,v)

        with open("data.csv", mode='r', encoding='ISO-8859-1') as f:
            reader = csv.DictReader(f, dialect='unix')
            data = random.choice([r for r in reader])
            for k, v in data.items():
                _k = ExifTags.Base[k].value
                if v != "":
                    exif[_k] = v
                elif _k in exif:
                    del exif[_k]

        for k, v in exif.items():
            print(f"{ExifTags.TAGS[k]}: {v}")

        img.save(f"_{fname}", exif=exif)
