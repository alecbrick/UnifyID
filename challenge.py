# UnifyID coding challenge.
# Author: Alec Brickner

import os
import sys
import urllib

# Gets num random RGB pixels.
# num should be an integer from 1 to 3333.
def get_random(num):
    url = "https://www.random.org/integers/"
    query = "?num=%s&min=0&max=255&col=128&base=10&format=plain&md=new" % \
        (num * 3)
    ret = []
    nums = urllib.urlopen(url + query)
    # Check if quota reached
    if nums.getcode() == 503:
        raise Exception(nums.readline())
    for line in nums.readlines():
        ret += map(int, line.split())
    return ret

# Creates the header for a 128x128 BMP file.
def bmp_header():
    header = []
    header += [0x42, 0x4D]       # ID
    header += [0x36, 0xc0, 0, 0] # Size. 0x36 header bytes, 0xc000 data bytes
    header += [0, 0, 0, 0]       # Unused
    header += [0x36, 0, 0, 0]    # Data offset

    header += [0x28, 0, 0, 0]    # Bytes in this section
    header += [0x80, 0, 0, 0]    # Image width
    header += [0x80, 0, 0, 0]    # Image height
    header += [0x01, 0]          # Color planes
    header += [0x18, 0]          # Bits per pixel
    header += [0, 0, 0, 0]       # Compression
    header += [0, 0xc0, 0, 0]    # Data size. 0xc000 data bytes
    header += [0x13, 0x0B, 0, 0] # PPM width.
    header += [0x13, 0x0B, 0, 0] # PPM height.
    header += [0, 0, 0, 0]       # Palette.
    header += [0, 0, 0, 0]       # Important colors.

    return bytearray(header)

# Creates a random 128 x 128 image.
def create_random_image():
    num_bytes = 128 * 128
    output = open("image.bmp", "wb")
    output.write(bmp_header())
    # Query 3333 RGB pixels at a time.
    while num_bytes > 0:
        num_to_get = min(3333, num_bytes)
        num_bytes -= num_to_get
        print "Fetching data..."
        try:
            data = get_random(num_to_get)
        except Exception as err:
            # Quota reached - delete the unfinished image.
            print err
            output.close()
            os.remove("image.bmp")
            sys.exit(1)

        print "Data received!"
        output.write(bytearray(data))
    output.close()

if __name__ == "__main__":
    create_random_image()
