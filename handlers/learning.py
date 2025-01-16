from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import MATERIALS_PATH

learning_router = Router()

# Уровни обучения
LEVELS = {
    "beginner": "Начальный",
    "intermediate": "Средний",
    "advanced": "Продвинутый",
}


# Состояния для выбора уровня и урока
class LearningStates(StatesGroup):
    waiting_for_level = State()  # Ожидание выбора уровня
    waiting_for_lesson = State()  # Ожидание выбора урока


# Обработчик для кнопки "Курсы"
@learning_router.message(F.text == "Курсы")
async def choose_level(message: Message, state: FSMContext):
    # Показываем пользователю уровни обучения
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=level_name) for level_name in LEVELS.values()],
            [KeyboardButton(text="Назад")]  # Кнопка "Назад"
        ],
        resize_keyboard=True,
    )
    await message.answer("Выберите уровень обучения:", reply_markup=keyboard)
    await state.set_state(LearningStates.waiting_for_level)


# Обработчик для выбора уровня
@learning_router.message(LearningStates.waiting_for_level)
async def send_lessons(message: Message, state: FSMContext):
    if message.text == "Назад":
        # Возвращаем пользователя в главное меню
        await message.answer("Возвращаемся в главное меню.", reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Курсы")]],
            resize_keyboard=True,
        ))
        await state.clear()
        return

    level = message.text
    if level in LEVELS.values():
        # Сохраняем выбранный уровень в состоянии
        await state.update_data(level=level)

        # Получаем ключ уровня (например, "beginner" для "Начальный")
        level_key = next(key for key, value in LEVELS.items() if value == level)
        lessons = get_lessons(level_key)

        if lessons:
            # Создаем клавиатуру с уроками и кнопкой "Назад"
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                             [KeyboardButton(text=lesson)] for lesson in lessons
                         ] + [[KeyboardButton(text="Назад")]],  # Добавляем кнопку "Назад"
                resize_keyboard=True,
            )
            await message.answer(f"Курс: Программирование на Python\nУровень: {level}", reply_markup=keyboard)
            await state.set_state(LearningStates.waiting_for_lesson)
        else:
            await message.answer("Материалы для этого уровня пока отсутствуют.")
    else:
        await message.answer("Пожалуйста, выберите уровень из предложенных.")


# Обработчик для выбора урока
@learning_router.message(LearningStates.waiting_for_lesson)
async def send_lesson_material(message: Message, state: FSMContext):
    if message.text == "Назад":
        # Возвращаем пользователя к выбору уровня
        await message.answer("Возвращаемся к выбору уровня.", reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=level_name) for level_name in LEVELS.values()],
                [KeyboardButton(text="Назад")]  # Кнопка "Назад"
            ],
            resize_keyboard=True,
        ))
        await state.set_state(LearningStates.waiting_for_level)
        return

    lesson = message.text
    level_data = await state.get_data()
    level = level_data.get("level")

    if level:
        # Получаем ключ уровня (например, "beginner" для "Начальный")
        level_key = next(key for key, value in LEVELS.items() if value == level)
        material = get_lesson_material(level_key, lesson)

        if material:
            await message.answer(material)
        else:
            await message.answer("Материал для этого урока отсутствует.")
    else:
        await message.answer("Произошла ошибка. Пожалуйста, начните заново.")


# Функция для получения списка уроков по уровню
def get_lessons(level: str) -> list:
    import os
    lessons_dir = os.path.join(MATERIALS_PATH, level)
    print(f"Ищем уроки в папке: {lessons_dir}")  # Логируем путь
    if os.path.exists(lessons_dir):
        files = os.listdir(lessons_dir)
        print(f"Найдены файлы: {files}")  # Логируем найденные файлы
        # Возвращаем список уроков (например, "Урок №1", "Урок №2" и т.д.)
        return [f"Урок №{i + 1}" for i in range(len(files))]
    return []


# Функция для получения материала урока
def get_lesson_material(level: str, lesson: str) -> str:
    import os
    lesson_number = lesson.replace("Урок №", "")
    lesson_file = os.path.join(MATERIALS_PATH, level, f"lesson{lesson_number}.txt")
    print(f"Ищем файл урока: {lesson_file}")  # Логируем путь к файлу
    if os.path.exists(lesson_file):
        with open(lesson_file, "r", encoding="utf-8") as file:
            return file.read()
    return ""