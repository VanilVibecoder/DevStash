import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

import sys
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")


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
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped by user.")