from aiogram import Router, types

router = Router()


@router.message(lambda message: message.text == "🕓 История")
async def history_handler(message: types.Message):
    await message.answer("📚 История ваших запросов:\n\n[Здесь будет история]")


@router.message(lambda message: message.text == "⚙️ Настройки")
async def settings_handler(message: types.Message):
    await message.answer(
        "⚙️ Настройки:\n\n"
        "• Язык и тон общения\n"
        "• Уведомления\n"
        "• Интеграции\n\n"
        "[Функционал в разработке]"
    )
