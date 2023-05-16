import asyncio
import logging

from aiogram import Dispatcher, Bot
from asyncpg import Pool
from asyncpg import create_pool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bot.middleware import DBMiddleware, OuterMiddleware
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

    engine = create_engine(config.db.url_object)

    Session = sessionmaker(engine)

    bot: Bot = Bot(token=(config.tg_bot.token))
    dp: Dispatcher = Dispatcher()

    pool: Pool = await create_pool(
        user=config.db.user,
        password=config.db.password,
        database=config.db.database,
        host=config.db.host,
        port=config.db.port
    )

    dp.include_router(admin.router)
    dp.include_router(user.router)
    dp.include_router(other.router)

    # dp.message.outer_middleware(OuterMiddleware())
    # dp.callback_query.outer_middleware(OuterMiddleware())

    # dp.message.middleware(DBMiddleware(pool))
    # dp.callback_query.middleware(DBMiddleware(pool))

    logger.warning('Bot started...')

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

def start_bot():
    try:
        asyncio.run(main())
    except Exception as ex:
        logger.error(ex)
