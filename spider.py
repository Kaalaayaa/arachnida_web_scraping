from bs4 import BeautifulSoup
import requests
import argparse
import sys

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


def scrape_images()
result = requests.get(url) #send an http get request to the url and store the response  
doc = BeautifulSoup(result.text, "html.parser") #parse the response text using BeautifulSoup

images = doc.find_all("img")

example = images[0] #get the first image tag
image = example.get("src") #get the value of the src attribute of the first image tag

print(example)
print(image)

