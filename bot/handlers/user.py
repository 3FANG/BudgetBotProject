from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.lexicon import RU_LEXICON
# from sqlalchemy.orm import Session


# session: Session


router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    """Отправляет приветственное сообщение"""
    await message.answer(text=RU_LEXICON['start_message'])
