import random
import hashlib
import requests
import string
from typing import Union
import logging

from bot.config import load_config

logger = logging.getLogger(__name__)

SYMBOLS = string.ascii_lowercase + '0123456789'
PAY_LINK = "https://payok.io/pay"
TRANSACTION_LINK = "https://payok.io/api/transaction"
CFG = load_config()

def get_pay_params(price: int, amount: int, desc: str) -> dict[Union[str, int]]:
    shop = CFG.payok.shop
    secret = CFG.payok.secret
    payment = ''.join(random.sample(SYMBOLS, 25))
    currency = CFG.payok.currency
    total_price = price * amount
    raw_sign = '|'.join((str(total_price), payment, str(shop), currency, desc, secret))
    sign = hashlib.md5(raw_sign.encode()).hexdigest()
    params = dict(
        shop=shop,
        amount=total_price,
        desc=desc,
        payment=payment,
        sign=sign,
        currency=currency
    )
    return payment, params

async def create_payment_form(price: int, amount: int, desc: str) -> str:
    payment, params = get_pay_params(price, amount, desc)
    res = requests.get(PAY_LINK, params=params)
    return payment, res.url

def get_transaction_params(payment: int) -> dict[Union[str, int]]:
    api_id = CFG.payok.api_id
    api_key = CFG.payok.api_key
    shop = CFG.payok.shop
    params = dict(API_ID=api_id, API_KEY=api_key, shop=shop, payment=payment)
    return params

async def check_payment(payment: int) -> bool:
    params = get_transaction_params(payment)
    res = requests.post(TRANSACTION_LINK, data=params)
    try:
        transaction_status = int(res.json()['1']['transaction_status'])
    except KeyError:
        logger.critical(f"{res.json()['text']}")
    return transaction_status == 1
