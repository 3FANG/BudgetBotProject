import datetime

from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from bot.lexicon import RU_LEXICON
from bot.database import Users
from bot.keyboards import start_keyboard


router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def start_command(message: Message, session: AsyncSession, state: FSMContext):
    print(await state.get_state())
    user = {
        'id': message.from_user.id,
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name,
        'signed': datetime.datetime.now()
    }
    await session.execute(insert(Users).values(user).on_conflict_do_nothing())
    await session.commit()

    await message.answer(text=RU_LEXICON['start_message'], reply_markup=start_keyboard())


@router.callback_query(F.data == 'main_menu')
async def main_menu_callback(callback: CallbackQuery):
    await callback.message.edit_text(text=RU_LEXICON['start_message'], reply_markup=start_keyboard())
