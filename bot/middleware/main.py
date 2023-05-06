from typing import Callable, Dict, Any, Awaitable, Union
from dataclasses import dataclass

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, Message, Update, CallbackQuery
from asyncpg import Pool

from bot.database import Database
from bot.config import load_environment
from bot.keyboards import channel_subscription_keyboard
from bot.lexicon import RU_LEXICON

@dataclass
class DBMiddleware(BaseMiddleware):
    pool: Pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: dict[str, Any]
    ) -> Any:

        # connection = await self.pool.acquire()
        # data['connection'] = connection
        # db = Database(connection)
        # data['db'] = db

        result = await handler(event, data)

        # if connection:
        #     await self.pool.release(connection)

        return result


@dataclass
class OuterMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:

        # bot: Bot = data['bot']

        return await handler(event, data)
