from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import CHANNELS


def show_channels():
    keyboard = InlineKeyboardMarkup(row_width=1)

    for channel in CHANNELS:
        btn = InlineKeyboardButton(channel[0], url=channel[2])
        keyboard.insert(btn)

    btn_done_sub = InlineKeyboardButton(text="✅ Я подписался", callback_data="subdone")
    keyboard.insert(btn_done_sub)
    return keyboard


