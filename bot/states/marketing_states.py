from aiogram.fsm.state import State, StatesGroup


class MarketingStates(StatesGroup):
    waiting_for_idea: State = State()  # Ожидание идеи для поста
    waiting_for_variant_selection: State = State()  # Ожидание выбора варианта поста
    waiting_for_photo: State = State()  # Ожидание фото для поста
    waiting_for_stories_idea: State = State()  # Ожидание идеи для сторис
