from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile  # Для отправки файлов
from config import MATERIALS_PATH  # Путь к папке с материалами
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем роутер для команды /shrek
shrek_router = Router()

# Обработчик для команды /shrek
@shrek_router.message(Command("shrek"))
async def send_shrek(message: types.Message):
    # Путь к изображению Shrek в папке data/materials/beginner
    shrek_image_path = os.path.join(MATERIALS_PATH, "beginner", "shrek.jpg")

    try:
        # Отправляем изображение
        photo = FSInputFile(shrek_image_path)
        await message.answer_photo(photo, caption="Это Шрек!")
        logger.info(f"Пользователь {message.from_user.id} запросил Shrek.")
    except FileNotFoundError:
        logger.error("Изображение Shrek не найдено.")
        await message.answer("Изображение Shrek не найдено.")
    except Exception as e:
        logger.error(f"Ошибка при отправке Shrek: {str(e)}")
        await message.answer(f"Произошла ошибка: {str(e)}")