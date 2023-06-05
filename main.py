import logging
import pyshorteners
from dotenv import load_dotenv
import os
import config as cfg
import markups as nav

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot)


async def check_sub(channels, user_id):
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=channel[1], user_id=user_id)
        if chat_member['status'] == 'left':
            return False
    return True


def shorten_link(url):
    s = pyshorteners.Shortener(api_key=cfg.api_key, timeout=600)
    return s.bitly.short(url)  # Возвращаем сокращенный URL


@dp.callback_query_handler(text="subdone")
async def subdone(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    if await check_sub(cfg.CHANNELS, callback_query.from_user.id):
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="👋🏻 Привет! Я бот по сокращению ссылок\nОтправь мне ссылку, а я сделаю ее короче")
    else:
        await bot.send_message(chat_id=callback_query.from_user.id, text=cfg.NOT_SUB_MESSAGE,
                               reply_markup=nav.show_channels())


# Ответ на команду старт
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == 'private':
        if await check_sub(cfg.CHANNELS, message.from_user.id):
            await message.answer(f"👋🏻 Привет! Я бот по сокращению ссылок\nОтправь мне ссылку, а я сделаю ее короче")
        else:
            await message.answer(cfg.NOT_SUB_MESSAGE, reply_markup=nav.show_channels())


@dp.message_handler()
async def process_message(message: types.Message):
    if message.chat.type == 'private':
        if await check_sub(cfg.CHANNELS, message.from_user.id):
            if message.text:  # Проверка, что сообщение содержит текст
                text = message.text.strip()
                if text.startswith('http') or text.startswith(
                        'https'):  # Проверка, что текст начинается с http или https
                    shortened_url = shorten_link(text)
                    await message.answer(f"Твоя ссылка\n🔗{shortened_url}",
                                         disable_web_page_preview=True)  # Отправляем сокращенную ссылку в ответ на сообщение
                else:
                    await message.answer('Сообщение не содержит ссылки')
            else:
                await message.answer('Сообщение не содержит текста')
        else:
            await message.answer(cfg.NOT_SUB_MESSAGE, reply_markup=nav.show_channels())


# Запуск Бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
