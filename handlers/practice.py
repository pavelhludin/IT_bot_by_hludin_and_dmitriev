from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import MATERIALS_PATH
import os

practice_router = Router()

# Курсы для практики
COURSES = {
    "python_basics": "Основы Python",
    "telegram_bot": "Разработка Telegram-бота",
    "django": "Разработка на Django"
}

# Состояния для выбора курса, задания и просмотра ответа
class PracticeStates(StatesGroup):
    waiting_for_course = State()  # Ожидание выбора курса
    waiting_for_task = State()    # Ожидание выбора задания
    waiting_for_answer = State()  # Ожидание выбора: посмотреть ответ или вернуться назад

# Обработчик для кнопки "Практика"
@practice_router.message(F.text == "Практика")
async def choose_course(message: Message, state: FSMContext):
    # Показываем пользователю список курсов
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=course_name) for course_name in COURSES.values()],
            [KeyboardButton(text="Назад")]  # Кнопка "Назад"
        ],
        resize_keyboard=True,
    )
    await message.answer("Выберите курс для практики:", reply_markup=keyboard)
    await state.set_state(PracticeStates.waiting_for_course)

# Обработчик для выбора курса
@practice_router.message(PracticeStates.waiting_for_course)
async def choose_task(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.clear()
        # Возвращаем пользователя в главное меню
        await message.answer("Возвращаемся в главное меню.", reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Практика")]],
            resize_keyboard=True,
        ))
        await state.clear()
        return

    # Ищем выбранный курс
    selected_course = None
    for course_key, course_name in COURSES.items():
        if course_name == message.text:
            selected_course = course_key
            break

    if selected_course:
        # Сохраняем выбранный курс в состоянии
        await state.update_data(course=selected_course)

        # Получаем список заданий для выбранного курса
        tasks = get_tasks(selected_course)

        if tasks:
            # Создаем клавиатуру с заданиями и кнопкой "Назад"
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text=task)] for task in tasks
                ] + [[KeyboardButton(text="Назад")]],  # Добавляем кнопку "Назад"
                resize_keyboard=True,
            )
            await message.answer(f"Выберите задание для курса '{COURSES[selected_course]}':", reply_markup=keyboard)
            await state.set_state(PracticeStates.waiting_for_task)
        else:
            await message.answer("Задания для этого курса пока отсутствуют.")
    else:
        await message.answer("Пожалуйста, выберите курс из предложенных.")

# Обработчик для выбора задания
@practice_router.message(PracticeStates.waiting_for_task)
async def send_task_material(message: Message, state: FSMContext):
    if message.text == "Назад":
        await state.clear()
        # Возвращаем пользователя к выбору курса
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=course_name) for course_name in COURSES.values()],
                [KeyboardButton(text="Назад")]  # Кнопка "Назад"
            ],
            resize_keyboard=True,
        )
        await message.answer("Выберите курс для практики:", reply_markup=keyboard)
        await state.set_state(PracticeStates.waiting_for_course)
        return

    task = message.text
    course_data = await state.get_data()
    selected_course = course_data.get("course")

    if selected_course:
        # Получаем материал задания
        material = get_task_material(selected_course, task)

        if material:
            # Сохраняем выбранное задание в состоянии
            await state.update_data(task=task)

            # Создаем клавиатуру с кнопками "Посмотреть правильный ответ" и "Назад"
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Посмотреть правильный ответ")],
                    [KeyboardButton(text="Назад")]
                ],
                resize_keyboard=True,
            )
            await message.answer(material, reply_markup=keyboard)
            await state.set_state(PracticeStates.waiting_for_answer)
        else:
            await message.answer("Материал для этого задания отсутствует.")
    else:
        await message.answer("Произошла ошибка. Пожалуйста, начните заново.")
    await state.clear()

# Обработчик для кнопки "Посмотреть правильный ответ"
@practice_router.message(PracticeStates.waiting_for_answer)
async def show_correct_answer(message: Message, state: FSMContext):
    if message.text == "Посмотреть правильный ответ":
        course_data = await state.get_data()
        selected_course = course_data.get("course")
        task = course_data.get("task")

        # Получаем правильный ответ для задания
        answer = get_task_answer(selected_course, task)

        if answer:
            await message.answer(f"Правильный ответ:\n{answer}")
        else:
            await message.answer("Правильный ответ для этого задания отсутствует.")
    elif message.text == "Назад":
        await state.clear()
        # Возвращаем пользователя к выбору задания
        course_data = await state.get_data()
        selected_course = course_data.get("course")
        tasks = get_tasks(selected_course)

        if tasks:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text=task)] for task in tasks
                ] + [[KeyboardButton(text="Назад")]],
                resize_keyboard=True,
            )
            await message.answer(f"Выберите задание для курса '{COURSES[selected_course]}':", reply_markup=keyboard)
            await state.set_state(PracticeStates.waiting_for_task)
        else:
            await message.answer("Задания для этого курса пока отсутствуют.")
    else:
        await message.answer("Пожалуйста, выберите одно из действий.")

# Функция для получения списка заданий по курсу
def get_tasks(course: str) -> list:
    tasks_dir = os.path.join("data", "practice", course)
    if os.path.exists(tasks_dir):
        files = os.listdir(tasks_dir)
        # Возвращаем список заданий (например, "Задание 1", "Задание 2" и т.д.)
        return [f"Задание {i + 1}" for i in range(len(files))]
    return []

# Функция для получения материала задания
def get_task_material(course: str, task: str) -> str:
    task_number = task.replace("Задание ", "")
    task_file = os.path.join("data", "practice", course, f"task{task_number}.txt")
    if os.path.exists(task_file):
        with open(task_file, "r", encoding="utf-8") as file:
            return file.read()
    return ""

# Функция для получения правильного ответа на задание
def get_task_answer(course: str, task: str) -> str:
    task_number = task.replace("Задание ", "")
    answer_file = os.path.join("data", "practice", course, f"answer{task_number}.txt")
    if os.path.exists(answer_file):
        with open(answer_file, "r", encoding="utf-8") as file:
            return file.read()
    return ""