import datetime
from collections import namedtuple

from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select

from bot.lexicon import RU_LEXICON
from bot.database import Users, Category, Aliases, Expense
from bot.keyboards import statistics_keyboard

from bot.states import ExpensesStates
from bot.services import ParsedMessage, _parse_message


router = Router()


@router.callback_query(F.data == 'statistics')
async def statistics_callback(callback: CallbackQuery):
    await callback.message.edit_text(text=RU_LEXICON['statistics_message'], reply_markup=statistics_keyboard())
