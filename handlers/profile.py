from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from states.profile_states import ProfileStates
from utils.database import get_user_data, update_user_data
from keyboards.reply import get_main_menu_keyboard
import re

profile_router = Router()

@profile_router.message(F.text == "Профиль")
async def show_profile(message: Message, state: FSMContext):
    user_data = get_user_data(message.from_user.id)
    if user_data:
        name, email = user_data
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Изменить имя")],
                [KeyboardButton(text="Изменить email")],
                [KeyboardButton(text="Назад")],
            ],
            resize_keyboard=True,
        )
        await message.answer(f"Ваш профиль:\nИмя: {name}\nEmail: {email}", reply_markup=keyboard)
        await state.set_state(ProfileStates.waiting_for_action)
    else:
        await message.answer("Профиль не найден. Пожалуйста, зарегистрируйтесь с помощью команды /start.")

@profile_router.message(ProfileStates.waiting_for_action)
async def process_profile_action(message: Message, state: FSMContext):
    if message.text == "Изменить имя":
        await message.answer("Введите новое имя:")
        await state.set_state(ProfileStates.waiting_for_new_name)
    elif message.text == "Изменить email":
        await message.answer("Введите новый email:")
        await state.set_state(ProfileStates.waiting_for_new_email)
    elif message.text == "Назад":
        await message.answer("Возвращаемся в главное меню.", reply_markup=get_main_menu_keyboard())
        await state.clear()
    else:
        await message.answer("Пожалуйста, выберите одно из действий.")

@profile_router.message(ProfileStates.waiting_for_new_name)
async def process_new_name(message: Message, state: FSMContext):
    new_name = message.text
    update_user_data(message.from_user.id, name=new_name)
    await message.answer("Имя успешно изменено!", reply_markup=get_main_menu_keyboard())
    await state.clear()

@profile_router.message(ProfileStates.waiting_for_new_email)
async def process_new_email(message: Message, state: FSMContext):
    new_email = message.text
    if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
        await message.answer("Пожалуйста, введите корректный email.")
        return

    update_user_data(message.from_user.id, email=new_email)
    await message.answer("Email успешно изменен!", reply_markup=get_main_menu_keyboard())
    await state.clear()