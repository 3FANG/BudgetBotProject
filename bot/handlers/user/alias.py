from collections import namedtuple

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.lexicon import RU_LEXICON
from bot.database import Category, Aliases
from bot.keyboards import (
    expenses_keyboard,
    cancel_operation_in_expenses_sesction_keyboard,
    categories_keyboard,
    confirm_adding_keyboard
)
from bot.states import ExpensesStates

router = Router()


@router.callback_query(F.data == 'add_alias')
async def select_category_on_keyboard_for_adding_alias(callback: CallbackQuery, session: AsyncSession):
    result = await session.execute(
        select(Category.name, Category.id)
        .where(Category.user_id == callback.from_user.id)
    )

    category = namedtuple("category", ['category_name', 'category_id'])
    categories = list(map(lambda x: category(x[0], x[1]), result.fetchall()))

    await callback.message.edit_text(
        text=RU_LEXICON['select_category_message'],
        reply_markup=categories_keyboard(expense_or_alias='alias', categories=categories))


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

    await state.update_data(alias=message.text.lower())
    data = await state.get_data()
    await state.set_state(ExpensesStates.confirm_adding_alias)
    await message.answer(
        text=RU_LEXICON['confirm_adding_alias_message'].format(message.text, data['category_name']),
        reply_markup=confirm_adding_keyboard('alias')
    )


@router.callback_query(StateFilter(ExpensesStates.confirm_adding_alias), F.data == ('add_alias_confirm'))
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
