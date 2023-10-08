from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.lexicon import RU_LEXICON


def start_keyboard():
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


def expenses_keyboard():
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


def statistics_keyboard():
    today_statistics_button: InlineKeyboardButton = InlineKeyboardButton(
        text=RU_LEXICON['today_statistics_button'],
        callback_data='today_statistics'
    )

    current_month_statistics_button: InlineKeyboardButton = InlineKeyboardButton(
        text=RU_LEXICON['current_month_statistics_botton'],
        callback_data='current_month'
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
