from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards import action_menu, scenario_menu
from services.ai_service import BackendService
from services.history_service import get_history_service
from states.finance_states import FinanceStates

router = Router()
backend_service = BackendService()


@router.message(F.text == "📊 Финансы и аналитика")
async def finance_handler(message: Message, state: FSMContext):
    """Обработчик выбора категории финансов"""
    await message.answer(
        "💰 <b>Финансы и аналитика</b>\n\n"
        "Отправьте финансовые данные для анализа (цифры, таблицы, текстовое описание):",
        reply_markup=scenario_menu,
        parse_mode="HTML",
    )
    await state.set_state(FinanceStates.waiting_for_data)


@router.message(FinanceStates.waiting_for_data)
async def process_finance_data(message: Message, state: FSMContext):
    """Обработка финансовых данных и анализ через бэкенд"""
    financial_data = message.text

    current_state = await state.get_state()
    if current_state:
        await state.clear()

    processing_msg = await message.answer("🔄 Анализирую финансовые данные...")

    try:
        # Вызываем бэкенд для анализа данных
        result = await backend_service.analyze_finance_data(
            data=financial_data, analysis_type="summary"
        )

        history_service = get_history_service()
        await history_service.add_record(
            user_id=message.from_user.id,
            category="📊 Финансы и аналитика",
            request_text=financial_data,
            response_text="\n\n".join(result.get("analysis", [])[:3]),
            response_data=result,
            message_id=message.message_id,
        )

        # Сохраняем данные для возможных дальнейших анализов
        await state.set_data(
            {"financial_data": financial_data, "initial_analysis": result}
        )

        # Формируем ответ
        analysis = result.get("analysis", "")
        insights = result.get("insights", [])
        recommendations = result.get("recommendations", [])

        response_text = "📈 <b>Финансовый анализ:</b>\n\n"
        response_text += f"{analysis}\n\n"

        if insights:
            response_text += "💡 <b>Ключевые инсайты:</b>\n"
            for insight in insights:
                response_text += f"• {insight}\n"
            response_text += "\n"

        if recommendations:
            response_text += "🎯 <b>Рекомендации:</b>\n"
            for recommendation in recommendations:
                response_text += f"• {recommendation}\n"

        response_text += (
            "\nХотите получить сравнение с предыдущим периодом или прогноз?"
        )

        await processing_msg.delete()
        await message.answer(
            response_text, reply_markup=scenario_menu, parse_mode="HTML"
        )
        await state.set_state(FinanceStates.waiting_for_comparison)

    except Exception as e:
        await processing_msg.delete()
        await message.answer(
            f"❌ Ошибка при анализе данных: {str(e)}\nПопробуйте еще раз.",
            reply_markup=scenario_menu,
        )
        await state.clear()


@router.message(FinanceStates.waiting_for_comparison)
async def process_comparison_choice(message: Message, state: FSMContext):
    """Обработка выбора типа дополнительного анализа"""
    user_choice = message.text.lower()
    data = await state.get_data()
    financial_data = data.get("financial_data", "")

    processing_msg = await message.answer("🔄 Формирую отчет...")

    try:
        if "сравнен" in user_choice:
            analysis_type = "comparison"
            result = await backend_service.analyze_finance_data(
                data=financial_data, analysis_type=analysis_type
            )

            response_text = "📊 <b>Сравнительный анализ:</b>\n\n"
            response_text += result.get("analysis", "")

        elif "прогноз" in user_choice:
            analysis_type = "forecast"
            result = await backend_service.analyze_finance_data(
                data=financial_data, analysis_type=analysis_type
            )

            response_text = "🔮 <b>Прогноз и тренды:</b>\n\n"
            response_text += result.get("analysis", "")

            forecast = result.get("forecast", {})
            if forecast:
                response_text += (
                    f"\n📈 <b>Тренд:</b> {forecast.get('trend', 'не определен')}"
                )
                response_text += f"\n📊 <b>Ожидаемый рост:</b> {forecast.get('growth', 'не определен')}"

        else:
            await processing_msg.delete()
            await message.answer("Пожалуйста, выберите 'сравнение' или 'прогноз':")
            return

        await processing_msg.delete()
        await message.answer(response_text, reply_markup=action_menu, parse_mode="HTML")
        await state.clear()

    except Exception as e:
        await processing_msg.delete()
        await message.answer(
            "❌ Ошибка при формировании отчета. Попробуйте еще раз.",
            reply_markup=scenario_menu,
        )
        await state.clear()
