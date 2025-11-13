from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType, Message
from keyboards import action_menu, marketing_menu, scenario_menu
from services.ai_service import BackendService
from states.marketing_states import MarketingStates

router = Router()
backend_service = BackendService()


@router.message(F.text == "💬 Маркетинг и контент")
async def marketing_handler(message: Message, state: FSMContext):
    """Обработчик выбора категории маркетинга"""
    await message.answer(
        "🎯 <b>Маркетинг и контент</b>\n\n"
        "Напишите вашу идею или тему для поста в соцсети:",
        reply_markup=marketing_menu,
        parse_mode="HTML",
    )
    await state.set_state(MarketingStates.waiting_for_idea)


@router.message(MarketingStates.waiting_for_idea)
async def process_idea(message: Message, state: FSMContext):
    """Обработка идеи пользователя и генерация постов через бэкенд"""
    user_idea = message.text

    # Показываем что обрабатываем
    processing_msg = await message.answer("🔄 Генерирую варианты постов...")

    try:
        # Вызываем бэкенд для генерации постов
        result = await backend_service.generate_marketing_posts(idea=user_idea)

        # Сохраняем варианты в state для следующего шага
        post_variants = result.get("post_variants", [])
        suggestions = result.get("suggestions", [])

        await state.update_data(
            post_variants=post_variants,
            suggestions=suggestions,
            original_idea=user_idea,
        )

        # Формируем ответ с вариантами постов
        response_text = "✅ <b>Вот варианты постов для вашей идеи:</b>\n\n"

        for i, variant in enumerate(
            post_variants[:3], 1
        ):  # Показываем первые 3 варианта
            response_text += f"<b>Вариант {i}:</b>\n{variant}\n\n"

        if suggestions:
            response_text += "💡 <b>Предложения:</b>\n"
            for suggestion in suggestions:
                response_text += f"• {suggestion}\n"

        response_text += "\nВыберите понравившийся вариант (напишите номер 1, 2 или 3) или создайте новый контент:"

        # Удаляем сообщение "Генерирую..." и отправляем результат
        await processing_msg.delete()
        await message.answer(
            response_text, reply_markup=marketing_menu, parse_mode="HTML"
        )
        await state.set_state(MarketingStates.waiting_for_variant_selection)

    except Exception as e:
        await processing_msg.delete()
        await message.answer(
            "❌ Произошла ошибка при генерации постов. Попробуйте еще раз или обратитесь в поддержку.",
            reply_markup=scenario_menu,
        )
        await state.clear()


@router.message(MarketingStates.waiting_for_variant_selection)
async def process_variant_selection(message: Message, state: FSMContext):
    """Обработка выбора варианта поста"""
    user_input = message.text.strip()

    # Получаем сохраненные данные
    data = await state.get_data()
    post_variants = data.get("post_variants", [])

    # Проверяем, выбрал ли пользователь номер варианта
    if user_input.isdigit() and 1 <= int(user_input) <= len(post_variants):
        selected_index = int(user_input) - 1
        selected_post = post_variants[selected_index]

        await message.answer(
            f"✅ <b>Вы выбрали вариант {user_input}:</b>\n\n{selected_post}\n\n"
            "Что дальше?",
            reply_markup=action_menu,
            parse_mode="HTML",
        )

        # Сохраняем выбранный пост для возможных дальнейших действий
        await state.update_data(selected_post=selected_post)
        await state.clear()

    else:
        # Если пользователь ввел не номер, обрабатываем как новую команду
        await message.answer(
            "Пожалуйста, выберите номер варианта (1, 2 или 3) или используйте меню:"
        )


@router.message(F.text == "🖼 Сторис / Баннер")
async def stories_handler(message: Message, state: FSMContext):
    """Обработчик создания сторис/баннера"""
    await message.answer(
        "🎨 <b>Создание сторис/баннера</b>\n\n" "Опишите идею для сторис или баннера:",
        reply_markup=scenario_menu,
        parse_mode="HTML",
    )
    await state.set_state(MarketingStates.waiting_for_stories_idea)


@router.message(MarketingStates.waiting_for_stories_idea)
async def process_stories_idea(message: Message, state: FSMContext):
    """Обработка идеи для сторис и генерация через бэкенд"""
    idea = message.text

    processing_msg = await message.answer("🔄 Генерирую сторис/баннер...")

    try:
        # Вызываем бэкенд для генерации сторис
        result = await backend_service.generate_stories(idea=idea)
        stories = result.get("stories", [])

        response_text = "🎨 <b>Варианты сторис/баннеров:</b>\n\n"
        for i, story in enumerate(stories, 1):
            response_text += f"<b>Вариант {i}:</b>\n{story}\n\n"

        response_text += "Выберите действие:"

        await processing_msg.delete()
        await message.answer(response_text, reply_markup=action_menu, parse_mode="HTML")
        await state.clear()

    except Exception as e:
        await processing_msg.delete()
        await message.answer(
            "❌ Ошибка при генерации сторис. Попробуйте еще раз.",
            reply_markup=scenario_menu,
        )
        await state.clear()


@router.message(F.text == "📢 Промо пост")
async def promo_post_handler(message: Message, state: FSMContext):
    """Обработчик создания промо поста"""
    await message.answer(
        "📢 <b>Создание промо поста</b>\n\n"
        "Опишите ваше промо-предложение или акцию:",
        reply_markup=scenario_menu,
        parse_mode="HTML",
    )
    await state.set_state(MarketingStates.waiting_for_idea)


@router.message(F.content_type == ContentType.PHOTO)
async def handle_photo(message: Message, state: FSMContext):
    """Обработка загруженного фото"""
    current_state = await state.get_state()

    if current_state == MarketingStates.waiting_for_photo:
        # Если ждем фото для поста
        await message.answer(
            "✅ Фото добавлено к посту! Выберите действие:", reply_markup=action_menu
        )
        await state.clear()
    else:
        await message.answer(
            "📸 Фото получено. Для работы с фото выберите соответствующий сценарий в меню."
        )
