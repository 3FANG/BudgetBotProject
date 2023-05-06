from CryptoPayAPI.AioCryptoPay import AioCryptoPay
from CryptoPayAPI.types import Asset

import asyncio
import math

from bot.config import load_config

CFG = load_config()


def convert_rub_to_asset(amount: int, price_rub: int) -> float:
    rate_usdt = float(CFG.cryptopay.rate_asset)
    total = round(amount*price_rub / rate_usdt, 2)

    return total


async def create_bill(total_sum: float) -> dict:
    cryptopay = AioCryptoPay(token=CFG.cryptopay.api_token)

    invoice = await cryptopay.create_invoice(asset=CFG.cryptopay.asset, amount=total_sum)

    await cryptopay.close()

    return invoice


async def check_bill(invoice_id: int):
    cryptopay = AioCryptoPay(token=CFG.cryptopay.api_token)

    invoice = await cryptopay.get_invoices(invoice_ids=invoice_id)

    await cryptopay.close()

    return invoice[0].status == 'paid'
