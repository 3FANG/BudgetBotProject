import datetime

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot.services import _parse_message, ParsedMessage
from bot.lexicon import RU_LEXICON
from bot.database.models import Aliases, Category, Expense


router = Router()


@router.message(StateFilter(default_state))
async def add_expense_on_alias(message: Message, session: AsyncSession):
    parsed_message: ParsedMessage = _parse_message(message.text)

    if not parsed_message:
        return await message.answer(text=RU_LEXICON['uncorrect_input_expense_on_alias_message'])

    result = await session.execute(
        select(Aliases.name, Category.id)\
        .join(Category, Category.id == Aliases.category_id)\
        .where(Category.user_id == message.from_user.id)\
        .where(Aliases.name == parsed_message.category_alias)
    )
    result = result.fetchone()

    if not result:
        await message.answer(text=RU_LEXICON['input_alias_does_not_exist'].format(parsed_message.category_alias))
    else:
        session.add(
            Expense(
                amount=parsed_message.amount,
                created=datetime.datetime.now(),
                category_id=result[1],
                comment=parsed_message.comment if parsed_message.comment else parsed_message.category_alias,
                raw_text=message.text))
        await session.commit()
        await message.answer(text=RU_LEXICON['successful_expense_addition_message'])


