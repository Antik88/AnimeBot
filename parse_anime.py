import asyncio
import aiohttp
import json
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
from random import randint as rand


HEADERS = {"User-Agent": UserAgent().random}

class Title:
    def __init__(self):
        self.id = ""
        self.url = ""
        self.name_ru = ""
        self.name_en = ""
        self.date = ""
        self.img = ""
        self.episodes = ""
        self.description = ""
        self.genre = []
        self.rating = ""
        self.screenshots = []

async def main():
    async with aiohttp.ClientSession() as session:
        result = {
            "title" : []
            }
        for page in range(1,5):
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
                    names_ru = item.find("span", {"class": "name-ru"})
                    names_en = item.find("span", {"class": "name-en"})
                    for name in names_ru:
                        title.name_ru = name.text
                    for name in names_en:
                        title.name_en = name.text
            
                    dates = item.find("span", {"class": "right"})
                    for date in dates:
                        title.date = date.text

                    urls = item.find_all("a")
                    for url in urls:
                        title.url = url.get("href")
                    
                    imgs = item.find_all("img")
                    for img in imgs:
                        title.img = img.get("src")
                        title.id = img.get("src").split('/')[6]

                    result["title"].append(title.__dict__)  

        write(result, 'data.json')

async def add_more_info():
    async with aiohttp.ClientSession() as session:
        data = read('data.json')
        for title in data['title']:
            async with session.get(title['url'], headers=HEADERS) as response:
                r = await aiohttp.StreamReader.read(response.content)
                soup = BS(r, "html.parser")

                info = soup.find_all("div", {"class": "value"})
                description = soup.find("div", {"class": "text"})
                genres = soup.find_all("span", {"class": "genre-ru"})
                rating = soup.find("div", {"class": "score-value score-9"})

                for genre in genres:
                    title['genre'].append(genre.text)
                title['rating'] = rating.text
                title['episodes'] = info[1].text
                title['description'] = description.text

        write(data, 'data.json')

async def add_screenshots():
    async with aiohttp.ClientSession() as session:
        data = read('data.json')
        for title in data['title']:
             async with session.get(title['url'] + "/resources", headers=HEADERS) as response:
                r = await aiohttp.StreamReader.read(response.content)
                soup = BS(r, "html.parser")

                div = soup.find("div", {"class": "c-screenshots"})

                for i in range(1,6): 
                    imgs = div.find_all("a", {"class": "c-screenshot b-image entry-" + f"{i}"})
                    for item in imgs:
                        title['screenshots'].append(item.get("href"))
        
    write(data, 'data.json')



def getRandAnime(data, used):
    title = Title()
    title_data = data['title']
    id = rand(0,len(title_data)-1)

    if id in used:
        id = rand(0,len(title_data)-1)+1

    title.name_ru = title_data[id]["name_ru"]
    title.date = title_data[id]["date"]
    title.img = title_data[id]["img"]
    title.episodes = title_data[id]["episodes"]
    title.description = title_data[id]["description"]
    title.genre = title_data[id]["genre"]
    title.rating = title_data[id]["rating"]

    # del data['title'][id]
    used.append(id)

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
    #loop.run_until_complete(main())
    #loop.run_until_complete(add_more_info())
    loop.run_until_complete(add_screenshots())