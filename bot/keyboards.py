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
