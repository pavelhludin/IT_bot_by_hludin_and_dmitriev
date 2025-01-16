from aiogram import F, Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command

practice_router = Router()

# Уровни сложности задач
DIFFICULTIES = {
    "easy": "Легкий",
    "medium": "Средний",
    "hard": "Сложный",
}

# Обработчик для кнопки "Практика"
@practice_router.message(F.text == "Практика")
async def choose_difficulty(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=difficulty_name, callback_data=difficulty_key)]
        for difficulty_key, difficulty_name in DIFFICULTIES.items()
    ])
    await message.answer("Выберите уровень сложности задач:", reply_markup=keyboard)

# Обработка выбора уровня сложности
@practice_router.callback_query(F.data.in_(DIFFICULTIES.keys()))
async def send_task(callback_query: CallbackQuery):
    difficulty = callback_query.data
    task = get_task(difficulty)
    if task:
        await callback_query.message.answer(task)
    else:
        await callback_query.message.answer("Задачи для этого уровня сложности пока отсутствуют.")
    await callback_query.answer()

# Функция для получения задачи по уровню сложности
def get_task(difficulty: str) -> str:
    tasks = {
        "easy": "Напишите программу, которая выводит 'Hello, World!'.",
        "medium": "Напишите программу, которая находит сумму всех чисел от 1 до 100.",
        "hard": "Напишите программу, которая реализует алгоритм сортировки слиянием.",
    }
    return tasks.get(difficulty, "")