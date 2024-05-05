import logging
import asyncio

from pyrogram import Client
from aiogram import Dispatcher, Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import cfg
from app.utils.logger import setup_logger
from app.services.ai.implementations.chatgpt import ChatGptConnector
from app.services.database.implementations.postgres import PostgresDAO

from app.bot.setup import setup_bot, start_bot
from app.userbot.setup import setup_userbot, start_userbot


async def setup() -> tuple[Dispatcher, Bot, Client]:
    setup_logger(cfg.logger_level)
    db = PostgresDAO(cfg.database_url.get_secret_value())
    await db.create_db()
    ai = ChatGptConnector(cfg.ai_api_key.get_secret_value(), cfg.ai_base_url)
    ai.connect()

    scheduler = AsyncIOScheduler()
    scheduler.start()

    dp, bot = await setup_bot(cfg, db, ai)
    client = await setup_userbot(bot, ai, db, scheduler)
    return dp, bot, client


async def main() -> None:
    dp, bot, client = await setup()

    loop = asyncio.get_event_loop()
    loop.create_task(start_bot(dp=dp, bot=bot))
    # loop.create_task(start_userbot(client))
    await start_userbot(client)
    loop.run_forever()
