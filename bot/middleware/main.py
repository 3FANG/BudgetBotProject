from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, Message, Update, CallbackQuery
from sqlalchemy.orm import sessionmaker


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        with self.session_pool() as session:
            data["session"] = session
            return await handler(event, data)
