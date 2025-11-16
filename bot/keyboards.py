from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🕓 История"), KeyboardButton(text="⚙️ Настройки")],
        [KeyboardButton(text="📂 Категории")],
    ],
    resize_keyboard=True,
)

# Меню категорий
categories_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💬 Маркетинг и контент")],
        [KeyboardButton(text="📊 Финансы и аналитика")],
        [KeyboardButton(text="📑 Документы и письма")],
        [KeyboardButton(text="⚖️ Юридическая помощь")],
        [KeyboardButton(text="📝 Краткие итоги встреч")],
        [KeyboardButton(text="🏠 Главное меню")],
    ],
    resize_keyboard=True,
)

# Меню сценария
scenario_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏠 Главное меню")],
        [KeyboardButton(text="📂 Категории")],
        [KeyboardButton(text="🔄 Новый сценарий")],
    ],
    resize_keyboard=True,
)

# Меню для маркетинга
marketing_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🖼 Сторис / Баннер")],
        [KeyboardButton(text="📢 Промо пост")],
        [KeyboardButton(text="📂 Категории")],
        [KeyboardButton(text="🏠 Главное меню")],
    ],
    resize_keyboard=True,
)

# Меню для документов
document_types_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📄 Договор"), KeyboardButton(text="📝 Письмо")],
        [KeyboardButton(text="💼 Коммерческое предложение")],
        [KeyboardButton(text="📂 Категории")],
        [KeyboardButton(text="🏠 Главное меню")],
    ],
    resize_keyboard=True,
)

# Меню действий после анализа
action_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Сохранить"), KeyboardButton(text="📤 Отправить")],
        [KeyboardButton(text="🔄 Новый сценарий")],
        [KeyboardButton(text="🏠 Главное меню")],
    ],
    resize_keyboard=True,
)

post_actions_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Сохранить"), KeyboardButton(text="📤 Опубликовать")],
        [
            KeyboardButton(text="🖼 Добавить фото"),
            KeyboardButton(text="📢 Создать промо"),
        ],
        [KeyboardButton(text="🔄 Новый пост"), KeyboardButton(text="🏠 Главное меню")],
    ],
    resize_keyboard=True,
)

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Клавиатура для истории
def get_history_keyboard(history_records, current_page=0, total_pages=1):
    """Клавиатура для навигации по истории"""
    keyboard = []

    for record in history_records:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{record['category']} - {record['created_at']}",
                    callback_data=f"history_detail:{record['id']}",
                )
            ]
        )

    # Навигация
    nav_buttons = []
    if current_page > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text="⬅️ Назад", callback_data=f"history_page:{current_page - 1}"
            )
        )

    nav_buttons.append(
        InlineKeyboardButton(
            text=f"{current_page + 1}/{total_pages}", callback_data="history_info"
        )
    )

    if current_page < total_pages - 1:
        nav_buttons.append(
            InlineKeyboardButton(
                text="Вперед ➡️", callback_data=f"history_page:{current_page + 1}"
            )
        )

    if nav_buttons:
        keyboard.append(nav_buttons)

    keyboard.append(
        [InlineKeyboardButton(text="❌ Закрыть", callback_data="history_close")]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Клавиатура для детального просмотра записи
def get_history_detail_keyboard(record_id, has_response=True):
    """Клавиатура для работы с конкретной записью"""
    keyboard = []

    if has_response:
        keyboard.extend(
            [
                [
                    InlineKeyboardButton(
                        text="🔄 Повторить запрос",
                        callback_data=f"history_repeat:{record_id}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📋 Показать ответ",
                        callback_data=f"history_show:{record_id}",
                    )
                ],
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="🗑 Удалить", callback_data=f"history_delete:{record_id}"
            ),
            InlineKeyboardButton(
                text="📚 Назад к истории", callback_data="history_back"
            ),
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
