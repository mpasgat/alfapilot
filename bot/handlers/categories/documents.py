from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards import action_menu, document_types_menu, scenario_menu
from services.ai_service import BackendService
from services.history_service import get_history_service
from states.document_states import DocumentStates

router = Router()
backend_service = BackendService()


@router.message(F.text == "📑 Документы и письма")
async def documents_handler(message: Message, state: FSMContext):
    """Обработчик выбора категории документов"""
    await message.answer(
        "📄 <b>Документы и письма</b>\n\n" "Выберите тип документа:",
        reply_markup=document_types_menu,
        parse_mode="HTML",
    )
    await state.set_state(DocumentStates.choosing_type)


@router.message(DocumentStates.choosing_type)
async def process_document_type(message: Message, state: FSMContext):
    """Обработка выбора типа документа"""
    doc_type = message.text

    # Сохраняем тип документа
    await state.update_data(doc_type=doc_type)

    await message.answer(
        f"📝 <b>Создание {doc_type}</b>\n\n"
        "Опишите, что должно быть в документе (основные пункты, ключевые моменты):",
        reply_markup=scenario_menu,
        parse_mode="HTML",
    )
    await state.set_state(DocumentStates.waiting_for_content)


@router.message(DocumentStates.waiting_for_content)
async def process_document_content(message: Message, state: FSMContext):
    """Обработка содержания документа и генерация через бэкенд"""
    content = message.text
    data = await state.get_data()
    doc_type = data.get("doc_type", "документа")

    processing_msg = await message.answer("🔄 Создаю документ...")

    try:
        # Вызываем бэкенд для генерации документа
        result = await backend_service.generate_document(
            doc_type=doc_type, content=content
        )

        history_service = get_history_service()
        await history_service.add_record(
            user_id=message.from_user.id,
            category="📑 Документы и письма",
            request_text=content,
            response_text="\n\n".join(result.get("document", [])[:3]),
            response_data=result,
            message_id=message.message_id,
        )

        document_text = result.get("document", "")
        corrections = result.get("corrections", [])
        suggestions = result.get("suggestions", [])

        # Сохраняем сгенерированный документ для возможных исправлений
        await state.update_data(
            generated_document=document_text, corrections=corrections
        )

        # Формируем ответ
        response_text = f"✅ <b>{doc_type} создан!</b>\n\n"
        response_text += f"{document_text}\n\n"

        if corrections:
            response_text += "⚠️ <b>Предлагаемые исправления:</b>\n"
            for correction in corrections:
                response_text += f"• {correction}\n"
            response_text += "\nПрименить исправления?"

        elif suggestions:
            response_text += "💡 <b>Предложения по улучшению:</b>\n"
            for suggestion in suggestions:
                response_text += f"• {suggestion}\n"

        await processing_msg.delete()
        await message.answer(response_text, reply_markup=action_menu, parse_mode="HTML")

        if corrections:
            await state.set_state(DocumentStates.waiting_for_corrections)
        else:
            await state.clear()

    except Exception as e:
        await processing_msg.delete()
        await message.answer(
            "❌ Ошибка при создании документа. Попробуйте еще раз.",
            reply_markup=scenario_menu,
        )
        await state.clear()


@router.message(DocumentStates.waiting_for_corrections)
async def process_corrections_choice(message: Message, state: FSMContext):
    """Обработка решения по исправлениям"""
    user_response = message.text.lower()

    if "да" in user_response or "примен" in user_response:
        # TODO: Реализовать применение исправлений
        await message.answer(
            "✅ Исправления применены! Документ сохранен.", reply_markup=action_menu
        )
    else:
        await message.answer(
            "❌ Исправления отклонены. Документ сохранен в исходном виде.",
            reply_markup=action_menu,
        )

    await state.clear()
