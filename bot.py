from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand  # Импортируем BotCommand
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

# Функция для регистрации команд
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать работу с ботом"),
        BotCommand(command="/menu", description="Открыть главное меню"),
    ]
    await bot.set_my_commands(commands)

# Запуск бота
async def main():
    await set_commands(bot)  # Регистрируем команды перед запуском бота
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())  # Запускаем бота