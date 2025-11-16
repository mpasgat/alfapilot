import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_ = load_dotenv()

TOKEN = os.getenv("TOKEN", "1234:token")

# Используем MemoryStorage для состояний
storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(storage=storage)

# Регистрируем все роутеры
from handlers import history, menu, start
from handlers.categories import documents, finance, legal, marketing, meetings

dp.include_router(start.router)
dp.include_router(menu.router)
dp.include_router(history.router)  # Добавляем историю
dp.include_router(marketing.router)
dp.include_router(finance.router)
dp.include_router(documents.router)
dp.include_router(legal.router)
dp.include_router(meetings.router)


async def main():
    logger.info("🤖 Alfapilot Bot started...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
