from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import MATERIALS_PATH

learning_router = Router()

# Уровни обучения и соответствующие курсы
LEVELS = {
    "beginner": {
        "name": "Начальный",
        "course": "Программирование на Python"
    },
    "intermediate": {
        "name": "Средний",
        "course": "Разработка telegram-бота"
    },
    "advanced": {
        "name": "Продвинутый",
        "course": "Разработка на Django 3"
    }
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
            [KeyboardButton(text=LEVELS[level]["name"]) for level in LEVELS],
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
        await state.clear()
        # Возвращаем пользователя в главное меню
        await message.answer("Возвращаемся в главное меню.", reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Курсы")]],
            resize_keyboard=True,
        ))
        await state.clear()
        return

    # Ищем выбранный уровень
    selected_level = None
    for level, data in LEVELS.items():
        if data["name"] == message.text:
            selected_level = level
            break

    if selected_level:
        # Сохраняем выбранный уровень в состоянии
        await state.update_data(level=selected_level)

        # Получаем уроки для выбранного уровня
        lessons = get_lessons(selected_level)

        if lessons:
            # Создаем клавиатуру с уроками и кнопкой "Назад"
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text=lesson)] for lesson in lessons
                ] + [[KeyboardButton(text="Назад")]],  # Добавляем кнопку "Назад"
                resize_keyboard=True,
            )
            # Показываем название курса и уровень
            course_name = LEVELS[selected_level]["course"]
            level_name = LEVELS[selected_level]["name"]
            await message.answer(f"Курс: {course_name}\nУровень: {level_name}", reply_markup=keyboard)
            await state.set_state(LearningStates.waiting_for_lesson)
        else:
            await message.answer("Материалы для этого уровня пока отсутствуют.")
    else:
        await message.answer("Пожалуйста, выберите уровень из предложенных.")
    
    

# Обработчик для выбора урока
@learning_router.message(LearningStates.waiting_for_lesson)
async def send_lesson_material(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.clear()
        # Возвращаем пользователя к выбору уровня
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=LEVELS[level]["name"]) for level in LEVELS],
                [KeyboardButton(text="Назад")]
            ],
            resize_keyboard=True,
        )
        await message.answer("Выберите уровень обучения:", reply_markup=keyboard)
        await state.set_state(LearningStates.waiting_for_level)
        return

    lesson = message.text
    level_data = await state.get_data()
    selected_level = level_data.get("level")

    if selected_level:
        # Получаем материал урока
        material = get_lesson_material(selected_level, lesson)

        if material:
            await message.answer(material)
        else:
            await message.answer("Материал для этого урока отсутствует.")
    else:
        await message.answer("Произошла ошибка. Пожалуйста, начните заново.")
    await state.clear()

# Функция для получения списка уроков по уровню
def get_lessons(level: str) -> list:
    import os
    lessons_dir = os.path.join(MATERIALS_PATH, level)
    if os.path.exists(lessons_dir):
        files = os.listdir(lessons_dir)
        # Возвращаем список уроков (например, "Урок №1", "Урок №2" и т.д.)
        return [f"Урок №{i + 1}" for i in range(len(files))]
    return []

# Функция для получения материала урока
def get_lesson_material(level: str, lesson: str) -> str:
    import os
    lesson_number = lesson.replace("Урок №", "")
    lesson_file = os.path.join(MATERIALS_PATH, level, f"lesson{lesson_number}.txt")
    if os.path.exists(lesson_file):
        with open(lesson_file, "r", encoding="utf-8") as file:
            return file.read()
    return ""