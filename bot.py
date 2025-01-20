from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

# Подключение роутеров
from handlers import (registration, menu, learning, practice, ai_functions, feedback, profile)
from middlewares import user_check, logging
from commands.shrek import shrek_router

dp.include_router(registration.registration_router)  # Подключаем registration_router
dp.include_router(menu.menu_router)
dp.include_router(learning.learning_router)
dp.include_router(practice.practice_router)
dp.include_router(ai_functions.ai_router)
dp.include_router(feedback.feedback_router)
dp.include_router(profile.profile_router)
dp.include_router(shrek_router)

# Подключение middleware
dp.message.middleware(user_check.UserCheckMiddleware())
dp.message.middleware(logging.LoggingMiddleware())

# Запуск бота
if __name__ == "__main__":
    dp.run_polling(bot, skip_updates=True)