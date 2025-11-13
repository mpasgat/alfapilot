from aiogram.fsm.state import State, StatesGroup


class LegalStates(StatesGroup):
    waiting_for_contract = State()
    waiting_for_reminder_choice = State()
