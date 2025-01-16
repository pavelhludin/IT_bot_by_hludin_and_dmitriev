from aiogram import Router, types
from aiogram.filters import Command
from keyboards.reply import get_main_menu_keyboard, get_ai_assistant_keyboard

menu_router = Router()

# Обработчик для команды /menu
@menu_router.message(Command("menu"))
async def cmd_menu(message: types.Message):
    await message.answer("Главное меню:", reply_markup=get_main_menu_keyboard())

# Обработчик для кнопки "AI-помощник"
@menu_router.message(lambda message: message.text == "AI-помощник")
async def ai_assistant(message: types.Message):
    await message.answer("Примечание:\n-Каждый запрос обрабатывается независимо, история диалога не сохраняется.\n-Если что-то пошло не так, начните заново, выбрав нужную функцию.", reply_markup=get_ai_assistant_keyboard())
    await message.answer("Выберите функцию AI-помощника:", reply_markup=get_ai_assistant_keyboard())

# Обработчик для кнопки "Назад"
@menu_router.message(lambda message: message.text == "Назад")
async def back_to_main_menu(message: types.Message):
    await message.answer("Главное меню:", reply_markup=get_main_menu_keyboard())