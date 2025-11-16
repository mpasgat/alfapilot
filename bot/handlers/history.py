import logging
import math

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards import get_history_detail_keyboard, get_history_keyboard
from services.history_service import get_history_service

router = Router()
logger = logging.getLogger(__name__)

PAGE_SIZE = 5


@router.message(F.text == "🕓 История")
async def history_handler(message: Message):
    """Показать историю запросов"""
    try:
        history_service = get_history_service()
        user_id = message.from_user.id

        records = await history_service.get_user_history(user_id, limit=PAGE_SIZE)

        if not records:
            await message.answer(
                "📚 История запросов пуста.\n\nСделайте первый запрос в любой категории!"
            )
            return

        total_count = await history_service.get_total_count(user_id)
        total_pages = math.ceil(total_count / PAGE_SIZE)

        # Create the keyboard first to ensure it's valid
        keyboard = get_history_keyboard(
            records, current_page=0, total_pages=total_pages
        )

        # Send message with inline keyboard
        await message.answer(
            "📚 <b>История ваших запросов:</b>\n\n"
            "Выберите запрос для просмотра или повторения:",
            reply_markup=keyboard,
            parse_mode="HTML",
        )

    except Exception as e:
        logger.error(f"Error in history handler: {e}")
        await message.answer(
            "❌ Произошла ошибка при загрузке истории. Попробуйте позже."
        )


@router.callback_query(F.data.startswith("history_page:"))
async def history_page_handler(callback: CallbackQuery):
    """Обработка переключения страниц истории"""
    try:
        page = int(callback.data.split(":")[1])
        user_id = callback.from_user.id
        history_service = get_history_service()

        records = await history_service.get_user_history(
            user_id, limit=PAGE_SIZE, offset=page * PAGE_SIZE
        )

        total_count = await history_service.get_total_count(user_id)
        total_pages = math.ceil(total_count / PAGE_SIZE)

        await callback.message.edit_reply_markup(
            reply_markup=get_history_keyboard(
                records, current_page=page, total_pages=total_pages
            )
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Error in history page handler: {e}")
        await callback.answer("❌ Ошибка при загрузке страницы")


@router.callback_query(F.data.startswith("history_detail:"))
async def history_detail_handler(callback: CallbackQuery):
    """Показать детали записи"""
    try:
        record_id = int(callback.data.split(":")[1])
        user_id = callback.from_user.id
        history_service = get_history_service()

        record = await history_service.get_record(record_id, user_id)

        if not record:
            await callback.answer("Запись не найдена")
            return

        response_text = (
            f"📋 <b>Детали запроса</b>\n\n"
            f"<b>Категория:</b> {record['category']}\n"
            f"<b>Время:</b> {record['created_at'].strftime('%d.%m.%Y %H:%M')}\n"
            f"<b>Запрос:</b>\n{record['request_text']}\n"
        )

        await callback.message.edit_text(
            response_text,
            reply_markup=get_history_detail_keyboard(
                record_id, bool(record.get("response_text"))
            ),
            parse_mode="HTML",
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Error in history detail handler: {e}")
        await callback.answer("❌ Ошибка при загрузке записи")


@router.callback_query(F.data.startswith("history_repeat:"))
async def history_repeat_handler(callback: CallbackQuery, state: FSMContext):
    """Повторить запрос из истории"""
    try:
        record_id = int(callback.data.split(":")[1])
        user_id = callback.from_user.id
        history_service = get_history_service()

        record = await history_service.get_record(record_id, user_id)

        if not record:
            await callback.answer("Запись не найдена")
            return

        # Сохраняем оригинальный запрос для повторения
        await state.update_data(
            history_original_request=record["request_text"],
            history_category=record["category"],
        )

        # Перенаправляем в соответствующую категорию
        category_handlers = {
            "💬 Маркетинг и контент": marketing_repeat,
            "📊 Финансы и аналитика": finance_repeat,
            "📑 Документы и письма": documents_repeat,
            "⚖️ Юридическая помощь": legal_repeat,
            "📝 Краткие итоги встреч": meetings_repeat,
        }

        handler = category_handlers.get(record["category"])
        if handler:
            await handler(callback, record)
        else:
            await callback.answer("❌ Неизвестная категория")

    except Exception as e:
        logger.error(f"Error in history repeat handler: {e}")
        await callback.answer("❌ Ошибка при повторении запроса")


async def marketing_repeat(callback: CallbackQuery, record: dict):
    """Повторение маркетингового запроса"""
    from handlers.categories.marketing import process_idea

    await callback.message.answer(
        f"🔄 Повторяю запрос в категории 'Маркетинг и контент':\n\n"
        f"<i>{record['request_text']}</i>",
        parse_mode="HTML",
    )

    # Создаем fake message для вызова обработчика
    class FakeMessage:
        def __init__(self, text, user_id):
            self.text = text
            self.from_user = type("User", (), {"id": user_id})()
            self.answer = callback.message.answer
            self.reply_markup = None

    fake_msg = FakeMessage(record["request_text"], callback.from_user.id)
    await process_idea(fake_msg, callback.message._bot.current_state())
    await callback.answer()


async def finance_repeat(callback: CallbackQuery, record: dict):
    """Повторение финансового запроса"""
    from handlers.categories.finance import process_finance_data

    await callback.message.answer(
        f"🔄 Повторяю запрос в категории 'Финансы и аналитика':\n\n"
        f"<i>{record['request_text']}</i>",
        parse_mode="HTML",
    )

    class FakeMessage:
        def __init__(self, text, user_id):
            self.text = text
            self.from_user = type("User", (), {"id": user_id})()
            self.answer = callback.message.answer

    fake_msg = FakeMessage(record["request_text"], callback.from_user.id)
    await process_finance_data(fake_msg, callback.message._bot.current_state())
    await callback.answer()


# Аналогичные функции для других категорий...
async def documents_repeat(callback: CallbackQuery, record: dict):
    from keyboards import document_types_menu

    await callback.message.answer(
        "🔄 Для повторения создания документа выберите тип документа:",
        reply_markup=document_types_menu,
    )
    await callback.answer()


async def legal_repeat(callback: CallbackQuery, record: dict):
    from handlers.categories.legal import process_contract_text

    await callback.message.answer(
        f"🔄 Повторяю анализ договора:\n\n<i>{record['request_text'][:500]}...</i>",
        parse_mode="HTML",
    )

    class FakeMessage:
        def __init__(self, text, user_id):
            self.text = text
            self.from_user = type("User", (), {"id": user_id})()
            self.answer = callback.message.answer

    fake_msg = FakeMessage(record["request_text"], callback.from_user.id)
    await process_contract_text(fake_msg, callback.message._bot.current_state())
    await callback.answer()


async def meetings_repeat(callback: CallbackQuery, record: dict):
    from handlers.categories.meetings import process_meeting_text

    await callback.message.answer(
        f"🔄 Повторяю создание резюме встречи:\n\n<i>{record['request_text']}</i>",
        parse_mode="HTML",
    )

    class FakeMessage:
        def __init__(self, text, user_id):
            self.text = text
            self.from_user = type("User", (), {"id": user_id})()
            self.answer = callback.message.answer

    fake_msg = FakeMessage(record["request_text"], callback.from_user.id)
    await process_meeting_text(fake_msg, callback.message._bot.current_state())
    await callback.answer()


@router.callback_query(F.data.startswith("history_show:"))
async def history_show_handler(callback: CallbackQuery):
    """Показать полный ответ из истории"""
    try:
        record_id = int(callback.data.split(":")[1])
        user_id = callback.from_user.id
        history_service = get_history_service()

        record = await history_service.get_record(record_id, user_id)

        if not record or not record.get("response_text"):
            await callback.answer("Ответ не найден")
            return

        response_text = record["response_text"]
        if len(response_text) > 4000:
            response_text = response_text[:4000] + "\n\n... (ответ сокращен)"

        full_response = (
            f"📋 <b>Полный ответ</b>\n\n"
            f"<b>Запрос:</b>\n{record['request_text']}\n\n"
            f"<b>Ответ:</b>\n{response_text}"
        )

        await callback.message.answer(full_response, parse_mode="HTML")
        await callback.answer()
    except Exception as e:
        logger.error(f"Error in history show handler: {e}")
        await callback.answer("❌ Ошибка при загрузке ответа")


@router.callback_query(F.data == "history_back")
async def history_back_handler(callback: CallbackQuery):
    """Вернуться к списку истории"""
    await history_handler(callback.message)
    await callback.answer()


@router.callback_query(F.data.startswith("history_delete:"))
async def history_delete_handler(callback: CallbackQuery):
    """Удалить запись из истории"""
    try:
        record_id = int(callback.data.split(":")[1])
        user_id = callback.from_user.id
        history_service = get_history_service()

        success = await history_service.delete_record(record_id, user_id)

        if success:
            await callback.answer("Запись удалена")
            await history_handler(callback.message)
        else:
            await callback.answer("Ошибка удаления")
    except Exception as e:
        logger.error(f"Error in history delete handler: {e}")
        await callback.answer("❌ Ошибка при удалении")


@router.callback_query(F.data == "history_close")
async def history_close_handler(callback: CallbackQuery):
    """Закрыть историю"""
    await callback.message.delete()
    await callback.answer()
