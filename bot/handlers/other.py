from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter


router = Router()


@router.message(StateFilter(default_state))
async def start_command(message: Message):
    await message.answer(text='Other message')
