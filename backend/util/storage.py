from PIL import Image, ImageOps, ImageFilter, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
import os, sys
import io
from urllib.request import urlopen
from flask import jsonify

def main():
    
    # Open the image
    img = Image.open('backend/util/thumbnail_stripped_exif.jpg')
    img = ImageOps.exif_transpose(img)
    # Save the image with a quality of 85 and optimize it
    exif = img.getexif()
    print(exif)
    img.show()

if __name__ == "__main__":
    main()