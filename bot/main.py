import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bot.middleware import DbSessionMiddleware
from bot.config.config import load_config, Config
from bot.handlers import user, admin, other

logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s',
        )
    logger.warning('Bot initialization...')

    config: Config = load_config()

    engine = create_engine(config.db.url_object, echo=True)

    Session = sessionmaker(engine)

    bot: Bot = Bot(token=(config.tg_bot.token))
    dp: Dispatcher = Dispatcher()

    dp.update.middleware(DbSessionMiddleware(session_pool=Session))
    # Automatically reply to all callbacks
    dp.callback_query.middleware(CallbackAnswerMiddleware())

    dp.include_router(admin.router)
    dp.include_router(user.router)
    dp.include_router(other.router)

    logger.warning('Bot started...')

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

def start_bot():
    try:
        asyncio.run(main())
    except KeyboardInterrupt as ex:
        logger.error("Bot stoped!")
