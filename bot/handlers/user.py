import datetime
import asyncio
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
from bot.database import Users, Category, Aliases
from bot.keyboards import (
    start_keyboard,
    expenses_keyboard,
    statistics_keyboard,
    cancel_operation_in_expenses_sesction_keyboard,
    categories_keyboard,
    confirm_category_or_alias_keyboard
)
from bot.states import ExpensesStates


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


@router.callback_query(F.data == 'cancel_operation_in_expenses_section')
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
async def input_category_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ExpensesStates.confirm_adding_category)
    await callback.message.edit_text(
        text=RU_LEXICON['input_category_name_message'],
        reply_markup=cancel_operation_in_expenses_sesction_keyboard
    )


@router.message(StateFilter(ExpensesStates.confirm_adding_category))
async def confirm_adding_category(message: Message, session: AsyncSession, state: FSMContext):

    ''' Add a validation input data '''

    await state.update_data(name_of_category=message.text.title())
    await state.set_state(ExpensesStates.add_category)
    await message.answer(
        text=RU_LEXICON['confirm_adding_category_message'].format(message.text.title()),
        reply_markup=confirm_category_or_alias_keyboard('category')
    )


@router.callback_query(StateFilter(ExpensesStates.add_category), F.data == "add_category_confirm")
async def add_category_on_database(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    await state.clear()
    name_of_category = data['name_of_category']

    result = await session.execute(
        select(Category.name)\
        .where(Category.user_id == callback.from_user.id)\
        .where(Category.name == name_of_category)
    )
    result = result.fetchone()

    if result and result[0] == name_of_category:
        await callback.message.edit_text(text=RU_LEXICON['unsuccessful_category_addition_message'].format(name_of_category))
    else:
        session.add(Category(name=name_of_category, user_id=callback.from_user.id))
        await session.commit()

        await callback.message.delete()
        await callback.message.answer(text=RU_LEXICON['successful_category_addition_message'])

    # '''Нужно ли для UX?'''
    # #await asyncio.sleep(1)

    await callback.message.answer(text=RU_LEXICON['expenses_message'], reply_markup=expenses_keyboard())


@router.callback_query(F.data == 'add_alias')
async def select_category_on_keyboard(callback: CallbackQuery, session: AsyncSession):
    result = await session.execute(
        select(Category.name, Category.id)
        .where(Category.user_id == callback.from_user.id)
    )

    category = namedtuple("category", ['category_name', 'category_id'])
    categories = list(map(lambda x: category(x[0], x[1]), result.fetchall()))

    await callback.message.edit_text(text=RU_LEXICON['select_category_message'], reply_markup=categories_keyboard(categories))


@router.callback_query(F.data.startswith('add_alias_to'))
async def input_alias_to_category(callback: CallbackQuery, state: FSMContext):
    category_name, category_id = callback.data.split(':')[1], int(callback.data.split(':')[2])

    await state.set_state(ExpensesStates.add_alias)
    await state.update_data(category_name=category_name, category_id=category_id)
    await callback.message.edit_text(
        text=RU_LEXICON['input_alias_message'].format(category_name),
        reply_markup=cancel_operation_in_expenses_sesction_keyboard
    )


@router.message(StateFilter(ExpensesStates.add_alias))
async def confirm_adding_alias(message: Message, state: FSMContext, session: AsyncSession):

    ''' Add a validation input data '''

    await state.update_data(alias=message.text)
    data = await state.get_data()
    await state.set_state(ExpensesStates.confirm_adding_alias)
    await message.answer(
        text=RU_LEXICON['confirm_adding_alias_message'].format(message.text, data['category_name']),
        reply_markup=confirm_category_or_alias_keyboard('alias')
    )


@router.callback_query(StateFilter(ExpensesStates.confirm_adding_alias))
async def add_alias_on_database(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    await state.clear()
    name_of_alias = data['alias']
    category_id = data['category_id']

    result = await session.execute(
        select(Aliases)\
        .where(Aliases.name == name_of_alias)
    )
    result = result.fetchone()

    if result and result[0] == name_of_alias:
        await callback.message.edit_text(text=RU_LEXICON['unsuccessful_alias_addition_message'].format(name_of_alias))
    else:
        session.add(Aliases(name=name_of_alias, category_id=category_id))
        await session.commit()

        await callback.message.delete()
        await callback.message.answer(text=RU_LEXICON['successful_alias_addition_message'])

    # '''Нужно ли для UX?'''
    # #await asyncio.sleep(1)

    await callback.message.answer(text=RU_LEXICON['expenses_message'], reply_markup=expenses_keyboard())


