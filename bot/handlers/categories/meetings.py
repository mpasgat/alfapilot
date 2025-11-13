from aiogram import F, Router, types

router = Router()


@router.message(F.text == "📝 Краткие итоги встреч")
async def meetings_handler(message: types.Message):
    await message.answer(
        "📝 Краткие итоги встреч\n\nОтправьте текст или аудио встречи для анализа:",
        reply_markup=scenario_menu,
    )
    # TODO: Реализовать обработку текста/аудио и генерацию резюме
