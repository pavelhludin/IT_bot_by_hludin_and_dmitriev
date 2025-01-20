from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Профиль")],
            [KeyboardButton(text="Курсы")],
            [KeyboardButton(text="Практика")],
            [KeyboardButton(text="AI-помощник")],  # Кнопка для AI-помощника
            [KeyboardButton(text="Обратная связь")],
        ],
        resize_keyboard=True,
    )
    return keyboard

def get_ai_assistant_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Генерация кода")],
            [KeyboardButton(text="Анализ кода")],
            [KeyboardButton(text="AI-диалог")],
            [KeyboardButton(text="Назад")],  # Кнопка для возврата в главное меню
        ],
        resize_keyboard=True,
    )
    return keyboard