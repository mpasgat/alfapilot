from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.states.legal_states import LegalStates

router = Router()


@router.message(F.text == "⚖️ Юридическая помощь")
async def legal_handler(message: types.Message, state: FSMContext):
    await message.answer(
        "⚖️ Юридическая помощь\n\nЗагрузите договор для анализа:",
        reply_markup=scenario_menu,
    )
    await state.set_state(LegalStates.waiting_for_contract)


@router.message(LegalStates.waiting_for_contract)
async def process_contract(message: types.Message, state: FSMContext):
    # TODO: Обработать загруженный документ
    await message.answer(
        "📑 Анализ договора:\n\n"
        "📋 Краткое содержание:\n"
        "[Здесь будет краткое содержание]\n\n"
        "⚠️ Рисковые пункты:\n"
        "[Здесь будут выделенные риски]\n\n"
        "Хотите добавить напоминание или синхронизировать с календарем?"
    )
    await state.clear()
