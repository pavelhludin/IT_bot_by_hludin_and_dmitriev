from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from states.registration_states import RegistrationStates
from utils.database import save_user
from aiogram.filters import Command
from keyboards.reply import get_main_menu_keyboard
import logging
import re

registration_router = Router()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@registration_router.message(Command("start"))
async def start_registration(message: Message, state: FSMContext):
    await message.answer("Давайте начнем регистрацию. Введите ваше имя:")
    await state.set_state(RegistrationStates.waiting_for_name)

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
