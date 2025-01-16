import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GIGACHAT_API_KEY = os.getenv("GIGACHAT_API_KEY") # Добавляем API-ключ OpenAssistant

# Путь к папке с учебными материалами
MATERIALS_PATH = os.path.join("data", "materials")

# Проверка, что переменные загружены
if not BOT_TOKEN:
    raise ValueError("Не удалось загрузить переменные окружения из .env файла.")