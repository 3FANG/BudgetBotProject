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
from bot.services import ParsedMessage, StatisticsMessage, _parse_message, get_month_statistics, converting_statistics_result_into_str

from sqlalchemy.engine import MappingResult


router = Router()


@router.callback_query(F.data == 'statistics')
async def statistics_callback(callback: CallbackQuery):
    await callback.message.edit_text(text=RU_LEXICON['statistics_message'], reply_markup=statistics_keyboard())


@router.callback_query(F.data == 'current_month_statistics')
async def current_month_statistics_callback(callback: CallbackQuery, session: AsyncSession):
    data: MappingResult = await get_month_statistics(session, callback.from_user.id)
    statistics: StatisticsMessage = converting_statistics_result_into_str(data)
    await callback.message.edit_text(RU_LEXICON['current_month_statistics_message'].format(
        period=statistics.period,
        expenses_by_categories=statistics.expenses_by_categories,
        total_expenses_amount=statistics.total_expenses_amount), reply_markup=None)
