import asyncio
import logging

from aiogram import Bot, Dispatcher

from .core.settings import settings
from .core.config import setup_logging

from .handlers.start import router as start_router
from .handlers.app import router as app_router

setup_logging()

logger = logging.getLogger(__name__)

async def main():

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    logger.info("Starting bot..")

    dp.include_router(start_router)
    dp.include_router(app_router)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.info(f"Bot stopped with an error: {e}")
    finally:
        logger.info("Bot stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped manually.")


