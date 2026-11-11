import argparse
import sys
import signal
from datetime import datetime
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

for imagename in files:
    try:
        with Image.open(imagename) as image:
            info_basic = {
                "Filename": image.filename,
                "Image Size": image.size,
                "Image Height": image.height,
                "Image Width": image.width,
                "Image Format": image.format,
                "Image Mode": image.mode,
                "Image is Animated": getattr(image, "is_animated", False),
                "Frames in Image": getattr(image, "n_frames", 1),
            }
            #Print basics metadata
            for label, value in info_basic.items():
                print(f"{label:25}: {value}")

            #read efix data 
            exifdata = image.getexif()
            if not exifdata:
                print("EXIF metadata: none")
                continue
            
            date_taken = exifdata.get(36867) or exifdata.get(36868) or exifdata.get(306) #efix tags IDS orginal, digitized or general date
            if date_taken:
                print(f"{'Date taken':25}: {date_taken}")
            else:
                print(f"{'Date taken':25}: not available")

            for tag_id in exifdata:
                tag = TAGS.get(tag_id, tag_id)
                data = exifdata.get(tag_id)
                #decode byte values to string
                if isinstance(data, bytes):
                    data = data.decode(errors="replace")
                print(f"{tag:25}: {data}")
    except (OSError, ValueError) as error:
        print(f"Error reading {imagename}: {error}")