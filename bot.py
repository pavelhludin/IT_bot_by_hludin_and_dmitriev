from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN

from utils.reminders import reminders_router, scheduler # Импортируем роутер из utils

# Создаем экземпляр бота с использованием DefaultBotProperties
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

# Подключение роутеров
from handlers import (start, registration, menu, learning, practice, ai_functions, feedback)
from utils import reminders
from middlewares import user_check, logging

dp.include_router(start.start_router)
dp.include_router(registration.registration_router)
dp.include_router(menu.menu_router)
dp.include_router(learning.learning_router)
dp.include_router(practice.practice_router)
dp.include_router(ai_functions.ai_router)
dp.include_router(feedback.feedback_router)
dp.include_router(reminders.reminders_router)

# Подключение middleware
dp.message.middleware(user_check.UserCheckMiddleware())
dp.message.middleware(logging.LoggingMiddleware())

# Запуск бота
if __name__ == "__main__":
    dp.run_polling(bot, skip_updates=True)