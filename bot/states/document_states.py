from aiogram.fsm.state import State, StatesGroup


class DocumentStates(StatesGroup):
    choosing_type: State = State()  # Выбор типа документа
    waiting_for_content: State = State()  # Ожидание содержания
    waiting_for_corrections: State = State()  # Ожидание подтверждения исправлений
