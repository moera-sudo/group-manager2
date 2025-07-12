from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def start(message: types.Message):

    text = (
        "Hello and welcome to GroupManager Bot – your assistant for creating and managing groups right in Telegram. To get started, simply type /app."
    )

    await message.answer(text)