from aiogram import Router
from aiogram.types import Message


router = Router()


@router.message()
async def start_command(message: Message):
    await message.answer(text='Other message')
