from aiogram.fsm.state import StatesGroup, State

class RegistrationStates(StatesGroup):
    waiting_for_name_choice = State()  # Ожидание выбора способа указания имени
    waiting_for_name = State()  # Ожидание ввода имени
    waiting_for_email = State()  # Ожидание ввода email