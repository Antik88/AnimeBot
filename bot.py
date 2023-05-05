import time
import logging
import parse_anime as parser

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData


TOKEN = "6197474322:AAEWCPB5AG2uDOR6KjmP3xwONOg4xetIuvA"
MSG = "Смотрел ли ты аниме сегодя, {}?"
HELP_COMMAND = """
/start - начать работу с ботом
👍 anime - какое-то аниме
🤓 help - список команд
"""
data = parser.read('data.json')

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton('🤓 help')).insert(KeyboardButton('👍 anime'))

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

title_back = CallbackData("pref","title_id")

@dp.callback_query_handler(title_back.filter())
async def button_press(call: types.CallbackQuery, callback_data: dict):
    id = callback_data.get('title_id')
    media = types.MediaGroup()
    for title in data['title']:
        if title['id'] == id:
            for i in range(0,5):
                media.attach_photo(title['screenshots'][i])
    await call.bot.send_media_group(call.message.chat.id, media=media)


@dp.message_handler(commands=['start'])
async def start_hendler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    await message.answer(f"Смотрел ли ты аниме сегодня, {user_name}?", reply_markup=kb)
        
@dp.message_handler(text='🤓 help')
async def help_command(message: types.Message):
    await message.answer(text=HELP_COMMAND)
  
used = []
@dp.message_handler(text='👍 anime') 
async def send_img(message: types.Message):
    title = parser.getRandAnime(data, used)
    description = title.description.split('.')[0] + title.description.split('.')[1]
    genres = ""
    
    title.name_ru = title.name_ru.replace(':','')

    for i in title.genre:
        genres += i.lower() + ' '
    
    caption = f"""{title.name_ru}
Жанры: {genres}
Год: {title.date}
Эпизодов: {title.episodes}
Рейтинг: {title.rating}
Описание: {description}
    """  
    ilkb = InlineKeyboardMarkup(row_width=1)
    line_btn1 = InlineKeyboardButton(text="👀 смотреть", url=f"https://www.google.com/search?q={title.name_ru}")
    get_imgs = InlineKeyboardButton(f"🖼 кадры из аниме",
                             callback_data=title_back.new(title_id=title.id))
    ilkb.add(line_btn1).add(get_imgs)
    await bot.send_photo(message.from_user.id, title.img, caption=caption, reply_markup=ilkb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)