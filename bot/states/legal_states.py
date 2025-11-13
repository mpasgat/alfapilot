from aiogram.fsm.state import State, StatesGroup


class LegalStates(StatesGroup):
    waiting_for_contract: State = State()  # Ожидание договора
    waiting_for_reminder: State = State()  # Ожидание решения о напоминании
    waiting_for_sync: State = State()  # Ожидание решения о синхронизации
