import re
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from states.registration_states import RegistrationStates
from utils.database import save_user, is_user_registered
from aiogram.filters import Command
from keyboards.reply import get_main_menu_keyboard
import logging

registration_router = Router()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@registration_router.message(Command("start"))
async def start_registration(message: Message, state: FSMContext):
    # Приветственное сообщение
    await message.answer("Привет! Я бот для обучения программированию. Давайте начнем с регистрации.")

    # Проверяем, зарегистрирован ли пользователь
    if is_user_registered(message.from_user.id):
        await message.answer("Вы уже зарегистрированы. Переходим в главное меню.", reply_markup=get_main_menu_keyboard())
        return

    # Если пользователь не зарегистрирован, начинаем процесс регистрации
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Использовать имя из профиля")],
            [KeyboardButton(text="Ввести новое имя")],
        ],
        resize_keyboard=True,  # Клавиатура автоматически подстраивается под размер экрана
    )
    await message.answer("Выберите, как вы хотите указать ваше имя:", reply_markup=keyboard)
    await state.set_state(RegistrationStates.waiting_for_name_choice)

@registration_router.message(RegistrationStates.waiting_for_name_choice)
async def process_name_choice(message: Message, state: FSMContext):
    if message.text == "Использовать имя из профиля":
        name = message.from_user.first_name
        if message.from_user.last_name:
            name += " " + message.from_user.last_name
        await state.update_data(name=name)
        await message.answer(f"Ваше имя: {name}. Введите ваш email:")
        await state.set_state(RegistrationStates.waiting_for_email)
    elif message.text == "Ввести новое имя":
        await message.answer("Введите ваше имя:")
        await state.set_state(RegistrationStates.waiting_for_name)
    else:
        await message.answer("Пожалуйста, выберите один из вариантов.")

@registration_router.message(RegistrationStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ваш email:")
    await state.set_state(RegistrationStates.waiting_for_email)

@registration_router.message(RegistrationStates.waiting_for_email)
async def process_email(message: Message, state: FSMContext):
    email = message.text
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        await message.answer("Пожалуйста, введите корректный email.")
        return

    await state.update_data(email=email)
    user_data = await state.get_data()
    save_user(message.from_user.id, user_data['name'], user_data['email'])
    await message.answer("Регистрация завершена!", reply_markup=get_main_menu_keyboard())
    await state.clear()