from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
# from sqlalchemy.orm import Session


# session: Session


router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(text='Hello, World!')
