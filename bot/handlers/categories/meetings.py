from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards import action_menu, scenario_menu
from services.ai_service import BackendService
from services.history_service import get_history_service
from states.meetings_states import MeetingsStates

router = Router()
backend_service = BackendService()


@router.message(F.text == "📝 Краткие итоги встреч")
async def meetings_handler(message: Message, state: FSMContext):
    """Обработчик выбора категории итогов встреч"""
    await message.answer(
        "📝 <b>Краткие итоги встреч</b>\n\n"
        "Отправьте текст встречи, обсуждения или переговоров для создания краткого резюме:",
        reply_markup=scenario_menu,
        parse_mode="HTML",
    )
    await state.set_state(MeetingsStates.waiting_for_meeting_text)


@router.message(MeetingsStates.waiting_for_meeting_text)
async def process_meeting_text(message: Message, state: FSMContext):
    """Обработка текста встречи и создание резюме"""
    meeting_text = message.text

    processing_msg = await message.answer("🔄 Создаю краткое резюме встречи...")

    try:
        # Используем сервис документов для создания резюме
        result = await backend_service.generate_document(
            doc_type="краткое резюме встречи", content=meeting_text, style="structured"
        )

        history_service = get_history_service()
        await history_service.add_record(
            user_id=message.from_user.id,
            category="📝 Краткие итоги встреч",
            request_text=meeting_text,
            response_text="\n\n".join(result.get("document", [])[:3]),
            response_data=result,
            message_id=message.message_id,
        )

        summary = result.get("document", "")
        key_points = result.get("suggestions", [])

        # Формируем ответ
        response_text = "📋 <b>Краткие итоги встречи:</b>\n\n"
        response_text += f"{summary}\n\n"

        if key_points:
            response_text += "🎯 <b>Ключевые моменты:</b>\n"
            for point in key_points:
                response_text += f"• {point}\n"

        response_text += (
            "\nРезюме готово! Вы можете сохранить его или отправить участникам."
        )

        await processing_msg.delete()
        await message.answer(response_text, reply_markup=action_menu, parse_mode="HTML")
        await state.clear()

    except Exception as e:
        await message.answer(
            "❌ Ошибка при создании резюме. Проверьте текст и попробуйте еще раз.",
            reply_markup=scenario_menu,
        )
        await state.clear()
