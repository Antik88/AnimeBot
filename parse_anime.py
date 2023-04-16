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

        # for anime in result['title']:
        #     url = anime['url']
        #     async with session.get(url, headers=HEADERS) as response:
        #         r = await aiohttp.StreamReader.read(response.content)
        #         soup = BS(r, "html.parser")

        #         info = soup.find_all("div", {"class": "value"})
                
        #         # anime['episodes'] = info[1].text

        #         print(info[1].text)
        
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

                # print(description.text)

                title['episodes'] = info[1].text
                title['description'] = description.text

                # print(info[1].text +" "+ format(conuter))
                # conuter+= 1

        write(data, 'data.json')


def getRandAnime(data):
    title = Title()
    title_data = data['title']
    id = rand(0,len(title_data)-1)

    title.name_ru = title_data[id]["name_ru"]
    title.date = title_data[id]["date"]
    title.img = title_data[id]["img"]
    title.episodes = title_data[id]["episodes"]
    title.description = title_data[id]["description"]

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
    # loop.run_until_complete(main())
    loop.run_until_complete(add_more_info())