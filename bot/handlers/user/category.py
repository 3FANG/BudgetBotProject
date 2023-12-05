from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.lexicon import RU_LEXICON
from bot.database import Category
from bot.keyboards import (
    expenses_keyboard,
    cancel_operation_in_expenses_sesction_keyboard,
    confirm_adding_keyboard
)
from bot.states import ExpensesStates


router = Router()


@router.callback_query(F.data == 'cancel_operation_in_expenses_section')
@router.callback_query(F.data == 'expenses')
async def expenses_callback(callback: CallbackQuery, state: FSMContext):
    if state:
        await state.clear()
        '''Можно сделать не редактирование сообщения, а удаление для улучшения UX'''

    await callback.message.edit_text(text=RU_LEXICON['expenses_message'], reply_markup=expenses_keyboard())


@router.callback_query(F.data == "add_category")
async def input_category_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ExpensesStates.confirm_adding_category)
    await callback.message.edit_text(
        text=RU_LEXICON['input_category_name_message'],
        reply_markup=cancel_operation_in_expenses_sesction_keyboard
    )


@router.message(StateFilter(ExpensesStates.confirm_adding_category))
async def confirm_adding_category(message: Message, state: FSMContext):

    ''' Add a validation input data '''

    await state.update_data(name_of_category=message.text.title())
    await state.set_state(ExpensesStates.add_category)
    await message.answer(
        text=RU_LEXICON['confirm_adding_category_message'].format(message.text.title()),
        reply_markup=confirm_adding_keyboard('category')
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
