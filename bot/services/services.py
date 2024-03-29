import re
import datetime
from zoneinfo import ZoneInfo
from typing import Optional
from datetime import date
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.row import Row
from sqlalchemy.engine import MappingResult
from sqlalchemy import text


@dataclass
class ParsedMessage:
    category_alias: Optional[str]
    amount: int
    comment: Optional[str]


@dataclass
class StatisticsMessage:
    period: str
    expenses_by_categories: str
    total_expenses_amount: int


def _parse_message(raw_message: str, inline: bool=False) -> ParsedMessage:
    if inline:
        pattern = re.compile(r"([\d]+) ([^\d]+)")
    else:
        pattern = re.compile(r"([\d]+) ([^\s\d]+)( .+)?")

    regexp_result = pattern.match(raw_message)

    if not regexp_result:
        return None

    amount = int(regexp_result.group(1))

    if inline:
        category_alias = None
        comment = regexp_result.group(2)
    else:
        category_alias = regexp_result.group(2)
        comment = regexp_result.group(3).strip() if regexp_result.group(3) else None

    return ParsedMessage(category_alias, amount, comment)


def _get_now_datetime() -> datetime.datetime:
    tz = ZoneInfo('Europe/Moscow')
    localized = datetime.datetime.now(tz=tz)
    return localized


'''Разобраться с асинхронностью. sqlalchemy.ext.asyncio.AsyncMappingResult.'''
async def get_month_statistics(session: AsyncSession, user_id: int) -> MappingResult:
    now = _get_now_datetime()
    # first_day_of_month = date.fromisoformat(f'{now.year:04d}-{now.month:02d}-01')
    first_day_of_month = date.fromisoformat(f'{now.year:04d}-11-01')

    result = await session.execute(text('''SELECT C.name, SUM(E.amount) \
FROM "Expense" E \
JOIN "Category" C ON C.id = E.category_id \
JOIN "Users" U ON U.id = C.user_id \
WHERE U.id = :user_id AND E.created >= :first_day_of_month \
GROUP BY C.id \
ORDER BY C.id'''), {'first_day_of_month': first_day_of_month, 'user_id': user_id})

    return result.mappings()


def converting_statistics_result_into_str(result: MappingResult) -> StatisticsMessage:
    now = _get_now_datetime()
    months = {
        '01': 'январь',
        '02': 'февраль',
        '03': 'март',
        '04': 'апрель',
        '05': 'май',
        '06': 'июнь',
        '07': 'июль',
        '08': 'август',
        '09': 'сентябрь',
        '10': 'октябрь',
        '11': 'ноябрь',
        '12': 'декабрь'
    }
    current_month = months[f'{now.month:02d}']
    data = result.all()
    expenses_by_categories = '\n'.join([f"{row.name}: {row.sum}" for row in data])
    total_expenses_amount = sum(map(lambda x: x.sum, data))

    return StatisticsMessage(current_month, expenses_by_categories, total_expenses_amount)
