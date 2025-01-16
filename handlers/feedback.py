from aiogram import F, Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.feedback_states import FeedbackStates

feedback_router = Router()

# Обработчик для кнопки "Обратная связь"
@feedback_router.message(F.text == "Обратная связь")
async def start_feedback(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, оцените бота по шкале от 1 до 5:")
    await state.set_state(FeedbackStates.waiting_for_rating)

# Команда для начала опроса
@feedback_router.message(Command("feedback"))
async def start_feedback(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, оцените бота по шкале от 1 до 5:")
    await state.set_state(FeedbackStates.waiting_for_rating)

# Обработка оценки
@feedback_router.message(FeedbackStates.waiting_for_rating)
async def process_rating(message: Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 5:
        await state.update_data(rating=int(message.text))
        await message.answer("Спасибо! Напишите ваш отзыв:")
        await state.set_state(FeedbackStates.waiting_for_comment)
    else:
        await message.answer("Пожалуйста, введите число от 1 до 5.")

# Обработка отзыва
@feedback_router.message(FeedbackStates.waiting_for_comment)
async def process_comment(message: Message, state: FSMContext):
    feedback_data = await state.get_data()
    rating = feedback_data.get("rating")
    comment = message.text
    save_feedback(message.from_user.id, rating, comment)
    await message.answer("Спасибо за ваш отзыв!")
    await state.clear()

# Функция для сохранения отзыва
def save_feedback(user_id: int, rating: int, comment: str):
    import csv
    with open("data/feedback.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow([user_id, rating, comment])