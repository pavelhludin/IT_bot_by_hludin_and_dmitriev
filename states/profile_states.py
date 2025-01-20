from aiogram.fsm.state import StatesGroup, State

class ProfileStates(StatesGroup):
    waiting_for_action = State()  # Ожидание выбора действия
    waiting_for_new_name = State()  # Ожидание ввода нового имени
    waiting_for_new_email = State()  # Ожидание ввода нового email