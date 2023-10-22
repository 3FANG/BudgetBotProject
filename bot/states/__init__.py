from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class ExpensesStates(StatesGroup):
    add_category: State = State()
    confirm_adding_category: State = State()

    add_alias: State = State()
    confirm_adding_alias : State = State()


# class AdminStates(StatesGroup):
#     pass
