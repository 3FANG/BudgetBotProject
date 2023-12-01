import datetime
from collections import namedtuple

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.lexicon import RU_LEXICON
from bot.database import Category, Expense
from bot.keyboards import (
    expenses_keyboard,
    cancel_operation_in_expenses_sesction_keyboard,
    categories_keyboard,
    confirm_adding_keyboard
)
from bot.states import ExpensesStates
from bot.services import ParsedMessage, _parse_message


router = Router()


@router.callback_query(F.data == 'add_expense')
async def select_category_on_keyboard_for_adding_expense(callback: CallbackQuery, session: AsyncSession):
    result = await session.execute(
        select(Category.name, Category.id)
        .where(Category.user_id == callback.from_user.id)
    )

    category = namedtuple("category", ['category_name', 'category_id'])
    categories = list(map(lambda x: category(x[0], x[1]), result.fetchall()))

    await callback.message.edit_text(
        text=RU_LEXICON['select_category_message'],
        reply_markup=categories_keyboard(expense_or_alias='expense', categories=categories))


@router.callback_query(F.data.startswith('add_expense_to'))
async def input_expense_to_category(callback: CallbackQuery, state: FSMContext):
    category_name, category_id = callback.data.split(':')[1], int(callback.data.split(':')[2])

    await state.set_state(ExpensesStates.add_expense)
    await state.update_data(category_name=category_name, category_id=category_id)
    await callback.message.edit_text(
        text=RU_LEXICON['input_expense_message'].format(category_name),
        reply_markup=cancel_operation_in_expenses_sesction_keyboard
    )


@router.message(StateFilter(ExpensesStates.add_expense))
async def confirm_adding_expense(message: Message, state: FSMContext):
    parsed_message: ParsedMessage = _parse_message(message.text, inline=True)

    if not parsed_message:
        return await message.answer(
            text=RU_LEXICON['uncorrect_input_expense_message'],
            reply_markup=cancel_operation_in_expenses_sesction_keyboard)

    await state.update_data(raw_text=message.text, amount=parsed_message.amount, comment=parsed_message.comment)
    data = await state.get_data()
    await state.set_state(ExpensesStates.confirm_adding_expense)
    await message.answer(
        text=RU_LEXICON['confirm_adding_expense_message'].format(message.text, data['category_name']),
        reply_markup=confirm_adding_keyboard('expense')
    )

@router.callback_query(StateFilter(ExpensesStates.confirm_adding_expense), F.data == ('add_expense_confirm'))
async def add_expense_on_database(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    amount_of_expense = data['amount']
    comment_of_expense = data['comment']
    category_id = data['category_id']
    raw_text = data['raw_text']

    session.add(
        Expense(
            amount=amount_of_expense,
            created=datetime.datetime.now(),
            category_id=category_id,
            comment=comment_of_expense,
            raw_text=raw_text))
    await session.commit()

    await callback.message.delete()
    await callback.message.answer(text=RU_LEXICON['successful_expense_addition_message'])

    # '''Нужно ли для UX?'''
    # #await asyncio.sleep(1)

    await callback.message.answer(text=RU_LEXICON['expenses_message'], reply_markup=expenses_keyboard())
