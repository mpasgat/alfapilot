from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType, Message
from keyboards import action_menu, scenario_menu
from services.ai_service import BackendService
from services.history_service import get_history_service
from states.legal_states import LegalStates

router = Router()
backend_service = BackendService()


@router.message(F.text == "⚖️ Юридическая помощь")
async def legal_handler(message: Message, state: FSMContext):
    """Обработчик выбора категории юридической помощи"""
    await message.answer(
        "⚖️ <b>Юридическая помощь</b>\n\n"
        "Загрузите договор для анализа (текстом или документом):",
        reply_markup=scenario_menu,
        parse_mode="HTML",
    )
    await state.set_state(LegalStates.waiting_for_contract)


@router.message(LegalStates.waiting_for_contract)
async def process_contract_text(message: Message, state: FSMContext):
    """Обработка текста договора"""
    contract_text = message.text

    await _analyze_contract(message, state, contract_text)


@router.message(
    LegalStates.waiting_for_contract, F.content_type == ContentType.DOCUMENT
)
async def process_contract_document(message: Message, state: FSMContext):
    """Обработка загруженного документа договора"""
    # TODO: Реализовать извлечение текста из документа
    await message.answer(
        "📄 Документ получен. В текущей версии поддерживается только текстовый анализ. "
        "Отправьте текст договора сообщением.",
        reply_markup=scenario_menu,
    )


async def _analyze_contract(message: Message, state: FSMContext, contract_text: str):
    """Общая функция анализа договора"""
    processing_msg = await message.answer("🔄 Анализирую договор...")

    try:
        # Вызываем бэкенд для анализа договора
        result = await backend_service.analyze_contract(
            contract_text=contract_text, analyze_risks=True
        )

        history_service = get_history_service()
        await history_service.add_record(
            user_id=message.from_user.id,
            category="⚖️ Юридическая помощь",
            request_text=contract_text,
            response_text="\n\n".join(result.get("summary", [])[:3]),
            response_data=result,
            message_id=message.message_id,
        )

        summary = result.get("summary", "")
        risks = result.get("risks", [])
        recommendations = result.get("recommendations", [])
        todo_items = result.get("todo_items", [])

        # Сохраняем результаты анализа
        await state.update_data(contract_analysis=result, todo_items=todo_items)

        # Формируем ответ
        response_text = "📑 <b>Анализ договора:</b>\n\n"
        response_text += f"<b>Краткое содержание:</b>\n{summary}\n\n"

        if risks:
            response_text += "⚠️ <b>Рисковые пункты:</b>\n"
            for risk in risks:
                response_text += f"• {risk}\n"
            response_text += "\n"

        if recommendations:
            response_text += "🎯 <b>Рекомендации:</b>\n"
            for recommendation in recommendations:
                response_text += f"• {recommendation}\n"
            response_text += "\n"

        if todo_items:
            response_text += "📋 <b>To-Do пункты:</b>\n"
            for item in todo_items:
                response_text += f"• {item}\n"

        response_text += "\nХотите добавить напоминание по срокам?"

        await processing_msg.delete()
        await message.answer(
            response_text, reply_markup=scenario_menu, parse_mode="HTML"
        )
        await state.set_state(LegalStates.waiting_for_reminder)

    except Exception as e:
        await processing_msg.delete()
        await message.answer(
            "❌ Ошибка при анализе договора. Проверьте текст и попробуйте еще раз.",
            reply_markup=scenario_menu,
        )
        await state.clear()


@router.message(LegalStates.waiting_for_reminder)
async def process_reminder_choice(message: Message, state: FSMContext):
    """Обработка решения о напоминании"""
    user_response = message.text.lower()

    if "да" in user_response or "добав" in user_response:
        # TODO: Реализовать добавление напоминания
        await message.answer(
            "⏰ Напоминание добавлено! Хотите синхронизировать с календарем или CRM?",
            reply_markup=scenario_menu,
        )
        await state.set_state(LegalStates.waiting_for_sync)
    else:
        await message.answer(
            "✅ Анализ завершен. Вы можете проверить другой договор или выбрать другую категорию.",
            reply_markup=action_menu,
        )
        await state.clear()


@router.message(LegalStates.waiting_for_sync)
async def process_sync_choice(message: Message, state: FSMContext):
    """Обработка решения о синхронизации"""
    user_response = message.text.lower()

    if (
        "синхрон" in user_response
        or "календар" in user_response
        or "crm" in user_response
    ):
        # TODO: Реализовать синхронизацию
        await message.answer(
            "✅ Синхронизация с календарем/CRM выполнена!", reply_markup=action_menu
        )
    else:
        await message.answer(
            "✅ Работа с договором завершена.", reply_markup=action_menu
        )

    await state.clear()
