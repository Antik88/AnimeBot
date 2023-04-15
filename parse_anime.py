import asyncio
import aiohttp
import json
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
from random import randint as rand


HEADERS = {"User-Agent": UserAgent().random}

class Title:
    def __init__(self):
        self.name = ""
        self.date = ""
        self.img = ""

async def main():
    async with aiohttp.ClientSession() as session:
        result = {
            "title" : []
            }
        for page in range(0,15):
            BASE_URL = "https://shikimori.me/animes/kind/tv/page/" + format(page)
            async with session.get(BASE_URL, headers=HEADERS) as response:
                r = await aiohttp.StreamReader.read(response.content)
                soup = BS(r, "html.parser")

                try:
                    main = soup.find("section", {"class": "l-content b-search-results"}).find_all("article")
                except: 
                    pass

                for item in main:
                    title = Title()
                    names = item.find("span", {"class": "name-ru"})
                    for name in names:
                        title.name = name.text
            
                    dates = item.find("span", {"class": "right"})
                    for date in dates:
                        title.date = date.text

                    imgs = item.find_all("img")
                    for img in imgs:
                        title.img = img.get("src")

                    result["title"].append(title.__dict__)

            write(result, 'data.json')            
            
def getRandAnime(data):
    title = Title()
    title_data = data['title']
    id = rand(0,len(title_data)-1)

    title.name = title_data[id]["name"]
    title.date = title_data[id]["date"]
    title.img = title_data[id]["img"]

    del data['title'][id]

    return title

def write(data, filename):
    data = json.dumps(data)
    data = json.loads(str(data))
    with open(filename, 'w', encoding = 'UTF-8') as file:
        json.dump(data, file, indent = 4)

def read(filename):
    with open(filename, 'r', encoding = 'UTF-8') as file:
        return json.load(file)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())