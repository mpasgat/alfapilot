from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.states.finance_states import FinanceStates

router = Router()


@router.message(F.text == "📊 Финансы и аналитика")
async def finance_handler(message: types.Message, state: FSMContext):
    await message.answer(
        "💰 Финансы и аналитика\n\nОтправьте финансовые данные для анализа:",
        reply_markup=scenario_menu,
    )
    await state.set_state(FinanceStates.waiting_for_data)


@router.message(FinanceStates.waiting_for_data)
async def process_finance_data(message: types.Message, state: FSMContext):
    data = message.text
    # TODO: Проанализировать данные через AI
    await message.answer(
        "📈 Анализ данных:\n\n"
        "[Здесь будет анализ и сводка]\n\n"
        "Хотите сравнение или прогноз?",
        reply_markup=scenario_menu,
    )
    await state.clear()
