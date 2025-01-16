from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging
import requests
from config import GIGACHAT_API_KEY

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем роутер для AI-функций
ai_router = Router()

# URL для аутентификации и запросов к GigaChat API
AUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
API_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

# Функция для получения токена доступа
def get_access_token():
    try:
        headers = {
            "Authorization": f"Bearer {GIGACHAT_API_KEY}",
            "RqUID": "7dc8cc07-7054-4cb2-96d5-9271bb95adcd",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "scope": "GIGACHAT_API_PERS"
        }
        response = requests.post(AUTH_URL, headers=headers, data=data, verify=False)
        response.raise_for_status()
        return response.json().get("access_token")
    except Exception as e:
        logger.error(f"Ошибка при получении токена: {str(e)}")
        raise Exception(f"Ошибка аутентификации: {str(e)}")

# Функция для генерации текста с помощью GigaChat API
async def generate_text(messages):
    try:
        access_token = get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            'Accept': 'application/json'
        }
        payload = {
            "model": "GigaChat",
            "messages": messages,
            "temperature": 0.5,
            "top_p": 0.1,
            "n": 1,
            "stream": False,
            "max_tokens": 512,
            "repetition_penalty": 1,
        }
        response = requests.post(API_URL, headers=headers, json=payload, verify=False)
        response.raise_for_status()
        response_data = response.json()

        if response_data.get("choices") and len(response_data["choices"]) > 0:
            return response_data["choices"][0]["message"]["content"]
        else:
            raise Exception("Ответ API не содержит 'choices'.")
    except Exception as e:
        logger.error(f"Ошибка при генерации текста: {str(e)}")
        raise Exception(f"Ошибка API: {str(e)}")

# Определяем состояния для AI-функций
class AIStates(StatesGroup):
    waiting_for_task_description = State()
    waiting_for_code = State()
    waiting_for_question = State()



# Обработчик для кнопки "Генерация кода"
@ai_router.message(lambda message: message.text == "Генерация кода")
async def generate_code(message: types.Message, state: FSMContext):
    await message.answer("Опишите задачу, для которой нужно сгенерировать код:")
    await state.set_state(AIStates.waiting_for_task_description)

# Обработчик для генерации кода на основе описания задачи
@ai_router.message(AIStates.waiting_for_task_description)
async def process_code_generation(message: types.Message, state: FSMContext):
    try:
        messages = [
            {"role": "system", "content": "Ты помогаешь генерировать код на Python."},
            {"role": "user", "content": message.text}
        ]
        generated_text = await generate_text(messages)
        await message.answer(f"{generated_text}")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")
    finally:
        await state.clear()



# Обработчик для кнопки "Анализ кода"
@ai_router.message(lambda message: message.text == "Анализ кода")
async def analyze_code(message: types.Message, state: FSMContext):
    await message.answer("Отправьте код для анализа:")
    await state.set_state(AIStates.waiting_for_code)

# Обработчик для анализа кода
@ai_router.message(AIStates.waiting_for_code)
async def process_code_analysis(message: types.Message, state: FSMContext):
    try:
        messages = [
            {"role": "system", "content": "Ты помогаешь анализировать код на Python."},
            {"role": "user", "content": message.text}
        ]
        generated_text = await generate_text(messages)
        await message.answer(f"{generated_text}")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")
    finally:
        await state.clear()



# Обработчик для кнопки "AI-диалог"
@ai_router.message(lambda message: message.text == "AI-диалог")
async def ai_dialog(message: types.Message, state: FSMContext):
    await message.answer("Задайте ваш вопрос:")
    await state.set_state(AIStates.waiting_for_question)

# Обработчик для AI-диалога
@ai_router.message(AIStates.waiting_for_question)
async def process_ai_dialog(message: types.Message, state: FSMContext):
    try:
        messages = [
            {"role": "system", "content": "Ты помогаешь пользователю с вопросами."},
            {"role": "user", "content": message.text}
        ]
        answer = await generate_text(messages)
        await message.answer(f"{answer}")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")
    finally:
        await state.clear()