import requests
from bs4 import BeautifulSoup
import json
import time
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)




# Set up logger
logger = logging.getLogger(__name__)

baseurl = "https://albumoftheyear.org"


useragent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

allalbums = []
currentpage = 1
firstpagesoup = None

logger.info("starting to scrape")
print("Sstarting to scrape")

while True:
    print(f"Scraping page {currentpage}...", end=" ")
    
    # get
    if currentpage == 1:
        pageurl = f"{baseurl}/upcoming/"
    else:
        pageurl = f"{baseurl}/upcoming/{currentpage}/"
    
    try:
        logger.info(f"scraping {currentpage}: {pageurl}")
        response = requests.get(pageurl, headers=useragent)
        response.raise_for_status()
        pagesoup = BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as requesterror:
        logger.error(requesterror)
        print(requesterror)
        pagesoup = None
    
    if not pagesoup:
        logger.error(f"page unaccessable {currentpage}")
        print(currentpage)
        break
    
    if currentpage == 1:
        firstpagesoup = pagesoup
        logger.info(f"first page done")

        print("done")
    else:
        # check
        firstpageblocks = firstpagesoup.find_all("div", class_="albumBlock")[:3]
        currentpageblocks = pagesoup.find_all("div", class_="albumBlock")[:3]
        
        titlesfromfirst = []
        titlesfromcurrent = []
        
        for albumblock in firstpageblocks:
            titleelement = albumblock.find("div", class_="albumTitle")
            if titleelement:
                titlesfromfirst.append(titleelement.get_text().strip())
        
        for albumblock in currentpageblocks:
            titleelement = albumblock.find("div", class_="albumTitle")
            if titleelement:
                titlesfromcurrent.append(titleelement.get_text().strip())
        
        if titlesfromfirst == titlesfromcurrent:
            logger.info("Repeats, stopping")
            print("finished")
            break
        print("finished")
    
    albumblocks = pagesoup.find_all("div", class_="albumBlock")
    albumsfromthispage = []
    
    for albumblock in albumblocks:
        try:
            artistdiv = albumblock.find("div", class_="artistTitle")
            albumdiv = albumblock.find("div", class_="albumTitle")
            datediv = albumblock.find("div", class_="type")
            
            if artistdiv:
                artistname = artistdiv.get_text().strip()
            else:
                artistname = "Unknown Artist"
            
            if albumdiv:
                albumtitle = albumdiv.get_text().strip()
            else:
                albumtitle = "Unknown Album"
            
            if datediv:
                releasedate = datediv.get_text().strip()
            else:
                releasedate = "TBA"
            
            imageelement = None
            linkelement = None
            
            imagecontainer = albumblock.find("div", class_="image")
            if imagecontainer:
                imageelement = imagecontainer.find("img")
                linkelement = imagecontainer.find("a")
            
            imageurl = None
            if imageelement:
                if imageelement.get("data-src"):
                    imageurl = imageelement["data-src"]
            
            albumurl = "#"
            if linkelement:
                if linkelement.get("href"):
                    linkhref = linkelement["href"]
                    if linkhref.startswith("/"):
                        albumurl = baseurl + linkhref
                    else:
                        albumurl = linkhref
            
            albuminfo = {
                "artist": artistname,
                "album": albumtitle,
                "date": releasedate,
                "link": albumurl,
                "image": imageurl
            }
            albumsfromthispage.append(albuminfo)
        except Exception as error:
            ## remmebr to add logger
            logger.error(error)
            print(error)
    
    allalbums.extend(albumsfromthispage)
    logger.info(f"Found {len(albumsfromthispage)} albums on page {currentpage}")
    print(len(albumsfromthispage))
    
    currentpage += 1
    time.sleep(0.3)


logger.info(f"total albums found: {len(allalbums)}")
print(len(allalbums))

### TRY EXCEPT BLOCK HERE

try:
    with open("kaggle/data/upcoming_albums.json", "w") as jsonfile:
        json.dump(allalbums, jsonfile, indent=2)
    
    logger.info("data saved to kaggle/data/ directory")
    print("data saved to kaggle/data/directory")
except Exception as saveerror:
    logger.error(saveerror)
    print(saveerror)



## now doing current releases 

currentalbums = []
currentpage = 1
firstpagehtml = None

logger.info("starting current releases scrape")
print("starting current")

while currentpage <= 50:
    print(f"Scraping current page {currentpage}...", end=" ")
    
    # get current releases page
    if currentpage == 1:
        pageurl = f"{baseurl}/releases/"
    else:
        pageurl = f"{baseurl}/releases/{currentpage}/"
    
    try:
        logger.info(f"scraping current {currentpage}: {pageurl}")
        response = requests.get(pageurl, headers=useragent)
        response.raise_for_status()
        pagesoup = BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as requesterror:
        logger.error(requesterror)
        print(requesterror)
        pagesoup = None
    
    if not pagesoup:
        logger.error(f"current page unaccessable {currentpage}")
        print(currentpage)
        break
    
    if currentpage == 1:
        firstpagehtml = pagesoup
        logger.info(f"first current page done")

        print("done")
    else:
        # check for repeats
        firstpageblocks = firstpagehtml.find_all("div", class_="albumBlock")[:3]
        currentpageblocks = pagesoup.find_all("div", class_="albumBlock")[:3]
        
        titlesfromfirst = []
        titlesfromcurrent = []
        
        for albumblock in firstpageblocks:
            titleelement = albumblock.find("div", class_="albumTitle")
            if titleelement:
                titlesfromfirst.append(titleelement.get_text().strip())
        
        for albumblock in currentpageblocks:
            titleelement = albumblock.find("div", class_="albumTitle")
            if titleelement:
                titlesfromcurrent.append(titleelement.get_text().strip())
        
        if titlesfromfirst == titlesfromcurrent:
            logger.info("Current repeats, stopping")
            print("finished current")
            break
        print("finished")
    
    albumblocks = pagesoup.find_all("div", class_="albumBlock")
    albumsfromthispage = []
    
    for albumblock in albumblocks:
        try:
            artistdiv = albumblock.find("div", class_="artistTitle")
            albumdiv = albumblock.find("div", class_="albumTitle")
            datediv = albumblock.find("div", class_="type")
            
            if artistdiv:
                artistname = artistdiv.get_text().strip()
            else:
                artistname = "Unknown Artist"
            
            if albumdiv:
                albumtitle = albumdiv.get_text().strip()
            else:
                albumtitle = "Unknown Album"
            
            if datediv:
                releasedate = datediv.get_text().strip()
            else:
                releasedate = "TBA"
            
            imageelement = None
            linkelement = None
            
            imagecontainer = albumblock.find("div", class_="image")
            if imagecontainer:
                imageelement = imagecontainer.find("img")
                linkelement = imagecontainer.find("a")
            
            imageurl = None
            if imageelement:
                if imageelement.get("data-src"):
                    imageurl = imageelement["data-src"]
            
            albumurl = "#"
            if linkelement:
                if linkelement.get("href"):
                    linkhref = linkelement["href"]
                    if linkhref.startswith("/"):
                        albumurl = baseurl + linkhref
                    else:
                        albumurl = linkhref
            
            albuminfo = {
                "artist": artistname,
                "album": albumtitle,
                "date": releasedate,
                "link": albumurl,
                "image": imageurl
            }
            albumsfromthispage.append(albuminfo)
        except Exception as error:
            logger.error(error)
            print(error)
    
    currentalbums.extend(albumsfromthispage)
    logger.info(f"Found {len(albumsfromthispage)} current albums on page {currentpage}")
    print(len(albumsfromthispage))
    
    currentpage += 1
    time.sleep(0.3)


logger.info(f"total current albums found: {len(currentalbums)}")
print(len(currentalbums))

### SAVE CURRENT RELEASES

try:
    with open("kaggle/data/current_albums.json", "w") as jsonfile:
        json.dump(currentalbums, jsonfile, indent=2)
    
    logger.info("current data saved to kaggle/data/ directory")
    print("current data saved")
except Exception as saveerror:
    logger.error(saveerror)
    print(saveerror)
