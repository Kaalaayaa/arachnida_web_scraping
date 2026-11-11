from bs4 import BeautifulSoup
import requests
import argparse
import sys
import os
from urllib.parse import urlparse, urljoin
import signal
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}

def handle_exit(sig, frame):
    print("\nStopped.")
    sys.exit(0)
signal.signal(signal.SIGINT, handle_exit)

parser = argparse.ArgumentParser()
parser.add_argument("-r", action="store_true", help="Enable recursive downlaod")
parser.add_argument("-l", type=int, default=5, help="Maximum depth level of the the recursive download")
parser.add_argument("-p", default="./data/", help="Path where the download files will be saved")
parser.add_argument("URL", help="URL to download from")

args = parser.parse_args()
if "-l" in sys.argv and "-r" not in sys.argv:
    parser.error("-l requires -r")

recursive = args.r
level = args.l
path = args.p
url = args.URL #"http://books.toscrape.com/"
visited = set()
allowed_hostname = urlparse(url).hostname

def download_img(page_url, img_url):
    full_url = urljoin(page_url, img_url)# get full url of img
    
    image_path = urlparse(full_url).path
    extension = os.path.splitext(image_path)[1].lower() #get the extension of the image file
    if extension not in ALLOWED_EXTENSIONS:
        print(f"Skipped: unsupported extension!!!")
        return
    
    filename = os.path.basename(urlparse(full_url).path) or "image.jpg" #get file name from the address
    filepath = os.path.join(path, filename) #build the path where we want to save

    try:
        response = requests.get(full_url)
        response.raise_for_status() # raise error for for http errors
        with open(filepath, 'wb') as f: #open local file as f and write img inside it
            f.write(response.content)
        print(f"Saved: {filepath}")
    except Exception as e:
        print(f"Failed: {full_url} ({e})")

def spider(level, url):
    if url in visited or level < 0:
        return
    visited.add(url)

    print("Level left to go:", level)

    os.makedirs(path, exist_ok=True) #create directory (if it exist do nothing(exist_ok = True))
    try:
        result = requests.get(url)
        result.raise_for_status()
    except requests.RequestException as error:
        print(f"Failed to access page: {url} ({error})")
        return
    html_doc = BeautifulSoup(result.text, "html.parser") #parse the response text using BeautifulSoup

    print("DOWNLOADING IMAGES FROM PAGE:", url)
    images = html_doc.find_all("img")
    if not images:
        print(f"No downloadable images found in the HTML of: {url}")
    for img in images:
        img_url = img.get("src") or img.get("data-src")  #get the value of the src attribute of the first image tag (data-lazy-src, data-original, or srcset)????
        if img_url:
            download_img(url, img_url)

    links = html_doc.find_all("a", href=True)
    if recursive and level > 0:
        for link in links:
            href = link.get("href")
            if href:
                full_url = urljoin(url, href)
                if urlparse(full_url).hostname != allowed_hostname:
                    continue
                spider(level - 1, full_url) #recursive that goes into the links

spider(level, url)