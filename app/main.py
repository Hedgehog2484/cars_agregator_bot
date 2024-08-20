import logging
import asyncio

from pyrogram import Client
from aiogram import Dispatcher, Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import cfg
from app.utils.logger import setup_logger
from app.services.ai.implementations.chatgpt import ChatGptConnector
from app.services.database.implementations.postgres import PostgresDAO
from app.services.wallet.implementations.yoomoney import YoomoneyWallet

from app.bot.setup import setup_bot, start_bot
from app.userbot.setup import setup_userbot, start_userbot
from app.web import start_webapp


async def setup() -> tuple[Dispatcher, Bot, Client, PostgresDAO]:
    setup_logger(cfg.logger_level)
    db = PostgresDAO(cfg.database_url.get_secret_value())
    await db.create_db()
    ai = ChatGptConnector(cfg.ai_api_key.get_secret_value(), cfg.ai_base_url)
    ai.connect()

    yw = YoomoneyWallet(
        client_id=cfg.yoomoney_client_id.get_secret_value(),
        client_secret=cfg.yoomoney_client_secret.get_secret_value(),
        base_api_url=cfg.yoomoney_base_url,
        redirect_url=cfg.yoomoney_redirect_url,
        auth_token=cfg.yoomoney_auth_token.get_secret_value(),
        receiver_number=cfg.yoomoney_receiver_number,
        payment_type=cfg.yoomoney_payment_type,
    )

    scheduler = AsyncIOScheduler()
    scheduler.start()

    dp, bot = await setup_bot(cfg, scheduler, db, ai, yw)
    client = await setup_userbot(bot, ai, db, scheduler)
    return dp, bot, client, db


async def main() -> None:
    dp, bot, client, db = await setup()
    loop = asyncio.get_event_loop()
    await start_bot(dp=dp, bot=bot)
    # loop.create_task(start_bot(dp=dp, bot=bot))
    # loop.create_task(start_webapp(db=db))
    loop.create_task(start_userbot(client))
    await start_userbot(client)
    loop.run_forever()
