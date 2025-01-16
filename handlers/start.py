from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.registration_states import RegistrationStates

# Создаем роутер
start_router = Router()

# Обработчик команды /start
@start_router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    await message.answer("Привет! Я бот для обучения программированию. Давайте начнем с регистрации.")
    await message.answer("Пожалуйста, введите ваше имя:")
    await state.set_state(RegistrationStates.waiting_for_name)