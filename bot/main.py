import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from bot.handlers import menu, start

_ = load_dotenv()

TOKEN = os.getenv("TOKEN", "1234:token")

bot = Bot(TOKEN)
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(menu.router)


async def main():
    print("Bot started...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
