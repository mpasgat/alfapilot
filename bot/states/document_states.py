from aiogram.fsm.state import State, StatesGroup


class DocumentStates(StatesGroup):
    choosing_type = State()
    waiting_for_content = State()
    waiting_for_corrections = State()
