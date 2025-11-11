from aiogram import Router, types
from aiogram.filters import CommandStart

from bot.keyboards import categories_menu, main_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Добро пожаловать в Alfapilot AI Assistant!\n\n"
        "Я ваш AI-помощник для бизнеса. Выберите категорию:",
        reply_markup=categories_menu,
    )


@router.message(lambda message: message.text == "🏠 Главное меню")
async def main_menu_handler(message: types.Message):
    await message.answer("Главное меню:", reply_markup=main_menu)


@router.message(lambda message: message.text == "📂 Категории")
async def categories_handler(message: types.Message):
    await message.answer("Выберите категорию:", reply_markup=categories_menu)
