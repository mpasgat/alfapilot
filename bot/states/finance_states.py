from aiogram.fsm.state import State, StatesGroup


class FinanceStates(StatesGroup):
    waiting_for_data: State = State()  # Ожидание финансовых данных
    waiting_for_analysis_type: State = State()  # Ожидание типа анализа
    waiting_for_comparison: State = State()  # Ожидание выбора сравнения/прогноза
