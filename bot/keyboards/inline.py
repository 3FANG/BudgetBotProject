from collections import namedtuple

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.lexicon import RU_LEXICON


def start_keyboard() -> InlineKeyboardMarkup:
    expenses_button: InlineKeyboardButton = InlineKeyboardButton(
        text=RU_LEXICON['expenses_button'],
        callback_data='expenses'
    )

    statistics_button: InlineKeyboardButton = InlineKeyboardButton(
        text=RU_LEXICON['statistics_button'],
        callback_data='statistics'
    )

    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[expenses_button, statistics_button]]
    )

    return keyboard

def expenses_keyboard() -> InlineKeyboardMarkup:
    add_category_button: InlineKeyboardButton = InlineKeyboardButton(
        text=RU_LEXICON['add_category_button'],
        callback_data='add_category'
    )

    add_alias_button: InlineKeyboardButton = InlineKeyboardButton(
        text=RU_LEXICON['add_alias_button'],
        callback_data='add_alias'
    )

    add_expense_button: InlineKeyboardButton = InlineKeyboardButton(
        text=RU_LEXICON['add_expense_button'],
        callback_data='add_expense'
    )

    main_menu_button: InlineKeyboardButton = InlineKeyboardButton(
        text=RU_LEXICON['main_menu_button'],
        callback_data='main_menu'
    )

    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [add_category_button],
            [add_alias_button],
            [add_expense_button],
            [main_menu_button]
        ]
    )

    return keyboard

def statistics_keyboard() -> InlineKeyboardMarkup:
    today_statistics_button: InlineKeyboardButton = InlineKeyboardButton(
        text=RU_LEXICON['today_statistics_button'],
        callback_data='today_statistics'
    )

    current_month_statistics_button: InlineKeyboardButton = InlineKeyboardButton(
        text=RU_LEXICON['current_month_statistics_botton'],
        callback_data='current_month_statistics'
    )

    select_period_button: InlineKeyboardButton = InlineKeyboardButton(
        text=RU_LEXICON['select_period_statistics_button'],
        callback_data='select_period_statistics'
    )

    main_menu_button: InlineKeyboardButton = InlineKeyboardButton(
        text=RU_LEXICON['main_menu_button'],
        callback_data='main_menu'
    )

    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [today_statistics_button],
            [current_month_statistics_button],
            [select_period_button],
            [main_menu_button]
        ]
    )

    return keyboard


cancel_operation_in_expenses_sesction_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(
        text=RU_LEXICON['cancel_operation_button'],
        callback_data='cancel_operation_in_expenses_section'
    )]]
)

def confirm_adding_keyboard(category_or_alias_or_expense: str) -> InlineKeyboardMarkup:
    confirm_button: InlineKeyboardButton = InlineKeyboardButton(
        text=RU_LEXICON['confirm_button'],
        callback_data=f'add_{category_or_alias_or_expense}_confirm'
    )
    cancel_button: InlineKeyboardButton = InlineKeyboardButton(
        text=RU_LEXICON['cancel_operation_button'],
        callback_data='cancel_operation_in_expenses_section'
    )
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[confirm_button, cancel_button]]
    )
    return keyboard


def categories_keyboard(expense_or_alias: str, categories: list[namedtuple]) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for category in categories:
        builder.add(
            InlineKeyboardButton(
                text=category.category_name,
                callback_data=f"add_{expense_or_alias}_to:{category.category_name}:{category.category_id}"
            )
        )
    builder.adjust(1)
    builder.row(InlineKeyboardButton(
        text=RU_LEXICON['cancel_operation_button'],
        callback_data='cancel_operation_in_expenses_section'
    ))
    return builder.as_markup()
