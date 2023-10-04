import datetime

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.lexicon import RU_LEXICON
from bot.database import Users
# from sqlalchemy.orm import Session


# session: Session


router = Router()


@router.message(CommandStart())
async def start_command(message: Message, session: AsyncSession):
    """Отправляет приветственное сообщение"""
    print(message.from_user)
    session.add(
        Users(
            id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            signed=datetime.datetime.now()
            )
        )
    await session.commit()

    await message.answer(text=RU_LEXICON['start_message'])
