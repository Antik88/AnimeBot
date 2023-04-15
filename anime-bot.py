import asyncio
import aiohttp
import json
from pprint import pprint
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

BASE_URL = "https://shikimori.me/animes/kind/tv"
HEADERS = {"User-Agent": UserAgent().random}

class Title:
    def __init__(self):
        self.name = ""
        self.date = ""
        self.img = ""

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, headers=HEADERS) as response:
            r = await aiohttp.StreamReader.read(response.content)
            soup = BS(r, "html.parser")

            result = {
                "title" : []
            }

            items = soup.find("div", {"class": "cc-entries"}).find_all("article")
            for item in items:
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
            pprint(read('data.json'))
            
               
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