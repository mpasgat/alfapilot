import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from handlers import menu, start
from handlers.categories import documents, finance, legal, marketing, meetings

_ = load_dotenv()

TOKEN = os.getenv("TOKEN", "1234:token")

# Используем MemoryStorage для состояний
storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(storage=storage)

# Регистрируем все роутеры
dp.include_router(start.router)
dp.include_router(menu.router)
dp.include_router(marketing.router)
dp.include_router(finance.router)
dp.include_router(documents.router)
dp.include_router(legal.router)
dp.include_router(meetings.router)


async def main():
    print("🤖 Alfapilot Bot started...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
