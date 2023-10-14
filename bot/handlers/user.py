import datetime
import asyncio

from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select

from bot.lexicon import RU_LEXICON
from bot.database import Users, Category
from bot.keyboards import (
    start_keyboard,
    expenses_keyboard,
    statistics_keyboard,
    cancel_add_category_keyboard,
    confirm_category_keyboard
)
from bot.states import ExpensesStates


router = Router()


@router.message(CommandStart())
async def start_command(message: Message, session: AsyncSession):
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


@router.callback_query(F.data == 'add_category_cancel')
@router.callback_query(F.data == 'expenses')
async def expenses_callback(callback: CallbackQuery, state: FSMContext):
    if state:
        await state.clear()
        '''Можно сделать не редактирование сообщения, а удаление для улучшения UX'''

    await callback.message.edit_text(text=RU_LEXICON['expenses_message'], reply_markup=expenses_keyboard())


@router.callback_query(F.data == 'statistics')
async def statistics_callback(callback: CallbackQuery):
    await callback.message.edit_text(text=RU_LEXICON['statistics_message'], reply_markup=statistics_keyboard())


@router.callback_query(F.data == "add_category")
async def add_category_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ExpensesStates.confirm_adding_category)
    await callback.message.edit_text(text=RU_LEXICON['add_category_message'], reply_markup=cancel_add_category_keyboard)


@router.message(StateFilter(ExpensesStates.confirm_adding_category))
async def confirm_category_name_state(message: Message, session: AsyncSession, state: FSMContext):

    ''' Add a validation input data '''

    await state.update_data(name_of_category=message.text)
    await state.set_state(ExpensesStates.add_category)
    await message.answer(
        text=RU_LEXICON['confirm_adding_category_message'].format(message.text),
        reply_markup=confirm_category_keyboard
    )


@router.callback_query(StateFilter(ExpensesStates.add_category))
async def add_category_state(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    await state.clear()
    name_of_category = data['name_of_category'].lower()

    result = await session.execute(
        select(Category.name)\
            .where(Category.user_id == callback.from_user.id)\
                .where(Category.name == name_of_category)
    )
    result = result.fetchone()

    if result and result[0].lower() == name_of_category:
        await callback.message.edit_text(text=RU_LEXICON['unsuccessful_category_addition_message'].format(name_of_category))
    else:
        session.add(Category(name=name_of_category, user_id=callback.from_user.id))
        await session.commit()

        await callback.message.delete()
        await callback.message.answer(text=RU_LEXICON['successful_category_addition_message'])

    # '''Нужно ли для UX?'''
    # #await asyncio.sleep(1)

    await callback.message.answer(text=RU_LEXICON['expenses_message'], reply_markup=expenses_keyboard())
