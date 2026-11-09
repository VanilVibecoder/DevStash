import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

from link_handler import links_router as links_router




import sys
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# check if token is set
if not TOKEN:
    sys.exit("Ошибка: переменная BOT_TOKEN не установлена в .env файле")



# Dispatcher is a central point for handling all incoming updates
dp = Dispatcher()


# /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Hello! I'm your bot.")


# main function
async def main():
    bot = Bot(token=TOKEN)
    dp.include_router(links_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped by user.")