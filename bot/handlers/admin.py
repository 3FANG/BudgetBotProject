from aiogram import Router
from aiogram.types import Message

from bot.filters import AdminFilter
from bot.config.config_reader import config

router = Router()


@router.message(AdminFilter(config.admin_ids))
async def admin_command(message: Message):
    await message.answer(text='Hello, Admin!')
