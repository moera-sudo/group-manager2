from aiogram import Router, types
from aiogram.filters import Command

from ..keyboards.app_keyboard import app_keyboard

router = Router()

@router.message(Command("app"))
async def start_web_app(message: types.Message):
    await message.answer(
        "Click the button below to launch the application:",
        reply_markup=app_keyboard
    )