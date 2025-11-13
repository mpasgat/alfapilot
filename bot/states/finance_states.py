from aiogram.fsm.state import State, StatesGroup


class FinanceStates(StatesGroup):
    waiting_for_data = State()
    waiting_for_comparison_choice = State()
