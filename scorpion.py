import argparse
import sys
import signal
from PIL import Image
from PIL.ExifTags import TAGS


def handle_exit(sig, frame):
    print("\nStopped.")
    sys.exit(0)
signal.signal(signal.SIGINT, handle_exit)

parser = argparse.ArgumentParser()
parser.add_argument("file", nargs='+', help="one or more file images to get info from")
args = parser.parse_args()

files = args.file
print(files)

# def extract_exif(img):
#     try:
#         with Image.open(img) as img:
#             exif_data = img.getexif()

#             if exif_data:
#                 print(exif_data)
#             else:
#                 print("no data")
#     except Exception as e:
#         print(f"Error:{e}")

# def parse_img(files):
#     for file in files:
#         print("exctracting files", file)
#         extract_exif(file)

# parse_img(files)

imagename = 