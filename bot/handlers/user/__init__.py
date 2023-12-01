from aiogram import Router

from bot.handlers.user import alias, category, expense, main_menu, statistics

user_router: Router = Router()

user_router.include_router(alias.router)
user_router.include_router(category.router)
user_router.include_router(expense.router)
user_router.include_router(main_menu.router)
user_router.include_router(statistics.router)
