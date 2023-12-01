import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.middleware import DbSessionMiddleware
from bot.config.config_reader import config
from bot.handlers import admin, other #, user
from bot.handlers.user import user_router

logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s',
        )
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.INFO)
    logger.warning('Bot initialization...')

    engine = create_async_engine(url=config.db_url)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    bot: Bot = Bot(token=(config.bot_token.get_secret_value()))
    dp: Dispatcher = Dispatcher()

    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    # Automatically reply to all callbacks
    dp.callback_query.middleware(CallbackAnswerMiddleware())

    dp.include_router(admin.router)
    dp.include_router(user_router)
    dp.include_router(other.router)

    logger.warning('Bot started...')

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

def start_bot():
    try:
        asyncio.run(main())
    except KeyboardInterrupt as ex:
        logger.error("Bot stoped!")
