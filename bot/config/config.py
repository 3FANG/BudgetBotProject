from dataclasses import dataclass
from environs import Env

# @dataclass
# class YooMoney:
#     token: str
#     account_number: int
#     redirect_uri: str


# @dataclass
# class CryptoPay:
#     api_token: str
#     asset: str
#     rate_asset: int


# @dataclass
# class Payok:
#     shop: int
#     currency: str
#     secret: str
#     api_id: int
#     api_key: str


@dataclass
class DBConfig:
    host: str
    password: str
    user: str
    database: str
    port: str

@dataclass
class TgBot:
    token: str

@dataclass
class Config:
    tg_bot: TgBot
    db: DBConfig
    admins: list[int]
    # ym: YooMoney
    # payok: Payok
    # cryptopay: CryptoPay

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
            host=env('HOST'),
            password=env('PASSWORD'),
            user=env('USER'),
            database=env('DATABASE'),
            port=env('PORT')
        ),
        # ym=YooMoney(
        #     token=env('YOOMONEY_TOKEN'),
        #     account_number=env('YOOMONEY_ACCOUNT_NUMBER'),
        #     redirect_uri=env('REDIRECT_URI')
        # ),
        # payok=Payok(
        #     shop=int(env('SHOP_ID')),
        #     currency=env('CURRENCY'),
        #     secret=env('SECRET_KEY'),
        #     api_id=int(env('API_ID')),
        #     api_key=env('API_KEY')
        # ),
        # cryptopay=CryptoPay(
        #     api_token=env('CRYPTOBOT_API_TOKEN'),
        #     asset=env('ASSET'),
        #     rate_asset=env('RATE_ASSET')
        # )
    )
