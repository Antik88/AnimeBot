import time
import logging
import parse_anime as paeser

from random import randint as rand
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

TOKEN = "6197474322:AAEWCPB5AG2uDOR6KjmP3xwONOg4xetIuvA"
MSG = "Смотрел ли ты аниме сегодя, {}?"
HELP_COMMAND = """
/start - начать работу с ботом
👍 anime - как-то аниме
➡️ next - следующее анмие
🤓 help - список команд
"""

kb = ReplyKeyboardMarkup(resize_keyboard=True)
get_btn = KeyboardButton('',)

kb.add(KeyboardButton('🤓 help')).insert(KeyboardButton('👍 anime')).insert(KeyboardButton('➡️ next'))

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
    data = paeser.read('data.json')

    title_id = rand(0,10)
    title_name = data['title'][title_id]["name"]
    date = data['title'][title_id]["date"]
    img_url = data['title'][title_id]["img"]
    
    caption = f'{title_name}\nГод: {date}'
    await bot.send_photo(message.from_user.id, img_url, caption=caption)

@dp.message_handler(text='➡️ next')
async def send_img(message: types.Message):
    data = paeser.read('data.json')
    

def getRandAnime(filename):
    title = paeser.Title
    
    # return все данные про аниме (нужно сделать класс аниме или импортировать его из тругого файла (parse_anime.py))
    pass




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)