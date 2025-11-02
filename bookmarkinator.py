import os
import sys
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from pathlib import Path
from datetime import datetime
# List of image URLs

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
now = str(datetime.now().strftime("%Y-%m-%d"))

# File Path Location
saveDir = input('Enter file destination: (Leave Blank for this folder)\nFile Path: ')
if not saveDir:
    curDir = Path.cwd()
    downloads = str(curDir/"Twitter Bookmarks")+"/"
    print(downloads)
    saveDir = downloads+now
else:
    saveDir+=now
os.makedirs(saveDir, exist_ok=True)

# File Format
fmt = input("Enter file format: (default:jpg or png) (Leave Blank for default)\nFormat: ")
if not fmt:
    fmt = "jpg"
if fmt not in ["png","jpg"]:
    clear()
    print("Invalid Input try again:")
    sys.exit()

links = []
try:
    link = open("bookmarks.txt", "r")
    for line in link:
        ## pick high res image
        url = line.strip()
        parsed = urlparse(url)
        queryParams = parse_qs(parsed.query)
        queryParams["name"] = ["large"]
        queryParams["format"] = [str(fmt)]
        newQuery = urlencode(queryParams, doseq=True)
        newUrl = urlunparse(parsed._replace(query=newQuery))
        links.append(newUrl)
    link.close()
    print(f"{len(links)} links will be installed")
    x = ["https://x.com/i/bookmarks"]


    for url in links:
        try:
            ##check for duplicate links
            if (x.__contains__(url)):
                continue
            else:
                try:
                    # Extract filename from URL
                    filename = f"{os.path.basename(urlparse(url).path)}.{fmt}"
                    filepath = os.path.join(saveDir, filename)

                    # Download the image
                    
                    response = requests.get(url)
                    response.raise_for_status()  # Raise an error for bad status

                    # Save the image
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    print(f"Downloaded: 「{filename}」")
                except Exception as e:
                    print(f"Failed to download 「{url}」: {e}")
                x.append(url)
        except KeyboardInterrupt:
            print(f"Stopped at  「{url}」")
            sys.exit()

## Errors m8 you love em
except FileNotFoundError:
    print ("bookmarks.txt file not found. Make sure to move the file to the same folder")
except Exception as e:
    print("An unexpected error occurred:", e)