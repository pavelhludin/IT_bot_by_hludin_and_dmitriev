from aiogram import Router, types  # Импортируем types
from aiogram.filters import Command  # Импортируем Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import BOT_TOKEN
from aiogram import Bot

# Создаем роутер для напоминаний
reminders_router = Router()

# Обработчики для напоминаний
@reminders_router.message(Command("remind"))
async def cmd_remind(message: types.Message):
    await message.answer("Напоминание настроено!")

# Инициализация бота
bot = Bot(token=BOT_TOKEN)

# Инициализация планировщика
scheduler = AsyncIOScheduler()

# Функция для отправки напоминания
async def send_reminder(user_id: int, message: str):
    await bot.send_message(user_id, message)

# Функция для настройки напоминания
def setup_reminder(user_id: int, message: str, time: int):
    scheduler.add_job(send_reminder, 'interval', minutes=time, args=(user_id, message))
