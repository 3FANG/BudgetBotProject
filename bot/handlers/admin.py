from aiogram import Router
from aiogram.types import Message

from bot.filters import AdminFilter
from bot.config.config import load_config


CFG = load_config()

router = Router()


@router.message(AdminFilter(CFG.admins))
async def admin_command(message: Message):
    await message.answer(text='Hello, Admin!')
