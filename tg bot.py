import json
from requests import get
from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup
from random import randint
import urllib
import requests as req


API_TOKEN = '5895388434:AAFU5YmXYp2CHTh6y5btPHuXg6DX7G4cvXo'
user_full_name = None

bot = Bot(token = API_TOKEN)
dp = Dispatcher(bot)

def search_picture(animal):
    url = 'https://yandex.ru/images/search?rpt=simage&noreask=1&source=qa&text={0}&stype=image&lr=117363'.format(animal)
    req = urllib.request.urlopen(url)
    soup = BeautifulSoup(req,features="html.parser")
    rand = randint(1, 20)
    number = "serp-item_pos_" + str(rand)
    url_2 = soup.find("div",class_=number).find("a").get("href")
    url_2 = "https://yandex.ru" + url_2
    #print(yandex_json)
    return url_2

@dp.message_handler(commands=['start'])

async def send_welcome(message: types.Message):
    global user_full_name
    user_full_name = message.from_user.full_name
    await message.answer("Привет! Я могу отправлять тебе фотографии котиков и собачек, напиши /help, что бы узнать подробнее".format(user_full_name))

@dp.message_handler(commands=['help'])

async def send_info(message):
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    item_dog = types.InlineKeyboardButton(text = 'Собака', callback_data = 'dog')
    item_cat = types.InlineKeyboardButton(text = 'Кошка', callback_data = 'cat')

    markup_inline.add(item_dog, item_cat)
    await message.answer("Выберите животное которое хотите увидеть:", reply_markup = markup_inline)


@dp.callback_query_handler(lambda call:True)

async def callback(call):
    if call.message:
        await bot.answer_callback_query(call.id)
        await dp.bot.send_photo(call.message.chat.id, photo= search_picture(call.data))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)
