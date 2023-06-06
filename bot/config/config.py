from dataclasses import dataclass
from environs import Env

from sqlalchemy import URL


@dataclass
class DBConfig:
    url_object: URL


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DBConfig
    admins: list[int]


def load_environment():
    env = Env()
    env.read_env()
    return env


def load_config():
    env = load_environment()
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN')
        ),
        admins=[int(id) for id in env.list('ADMIN_IDS')],
        db=DBConfig(
            url_object=URL.create(
                "postgresql+asyncpg",
                username=env('USER'),
                password=env('PASSWORD'),
                host=env('HOST'),
                port=env('PORT')
                )
        )
    )
