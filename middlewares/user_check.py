from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from utils.database import is_user_registered
from aiogram.fsm.context import FSMContext
from states.registration_states import RegistrationStates


class UserCheckMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        # Получаем состояние пользователя
        state: FSMContext = data.get("state")

        # Если пользователь находится в процессе регистрации, пропускаем проверку
        current_state = await state.get_state()
        if current_state in [
            RegistrationStates.waiting_for_name_choice,
            RegistrationStates.waiting_for_name,
            RegistrationStates.waiting_for_email
        ]:
            return await handler(event, data)

        # Пропускаем команду /start
        if event.text == "/start":
            return await handler(event, data)

        # Проверяем, зарегистрирован ли пользователь
        if not is_user_registered(event.from_user.id):
            await event.answer("Пожалуйста, зарегистрируйтесь с помощью команды /start.")
            return

        # Продолжаем обработку сообщения
        return await handler(event, data)