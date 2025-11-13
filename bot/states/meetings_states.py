from aiogram.fsm.state import State, StatesGroup


class MeetingsStates(StatesGroup):
    waiting_for_meeting_text: State = State()  # Ожидание текста встречи
