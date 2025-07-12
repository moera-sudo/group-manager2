from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from ..core.settings import settings

WEB_APP_URL = settings.WEB_APP_URL


app_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Open Group Manager",
                web_app=WebAppInfo(url=WEB_APP_URL)
            )
        ]
    ]
)