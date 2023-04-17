import time
import logging
import parse_anime as parser

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

import asyncio
import aiohttp
import json
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent

HEADERS = {"User-Agent": UserAgent().random}
TOKEN = "6197474322:AAEWCPB5AG2uDOR6KjmP3xwONOg4xetIuvA"
MSG = "Смотрел ли ты аниме сегодя, {}?"
HELP_COMMAND = """
/start - начать работу с ботом
👍 anime - как-то аниме
🤓 help - список команд
"""
data = parser.read('data.json')

kb = ReplyKeyboardMarkup(resize_keyboard=True)
get_btn = KeyboardButton('',)

kb.add(KeyboardButton('🤓 help')).insert(KeyboardButton('👍 anime'))

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

@dp.message_handler(commands=['start'])
async def start_hendler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    await message.answer(f"Смотрел ли ты аниме сегодя, {user_name}?", reply_markup=kb)

@dp.message_handler(text='🤓 help')
async def help_command(message: types.Message):
    await message.answer(text=HELP_COMMAND)
  
@dp.message_handler(text='👍 anime') 
async def send_img(message: types.Message):
    title = parser.getRandAnime(data)
    description = title.description.split('.')[0] + title.description.split('.')[1]
    caption = f"""{title.name_ru}
Год: {title.date}
Эпизодов: {title.episodes}
Рейтинг: {title.rating}
Описание: {description}
    """  
    await bot.send_photo(message.from_user.id, title.img, caption=caption)

# @dp.message_handler(text='➡️ next')
# async def next(message: types.Message):
#     data = parser.read('data.json')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)