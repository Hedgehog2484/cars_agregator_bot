import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pydantic_settings import BaseSettings
from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from aiogram.fsm.storage.memory import MemoryStorage

from app.bot.handlers import setup_handlers
from app.bot.middlewares import setup_middlewares

from app.services.database.dao import IDAO
from app.services.ai.ai_connector import IAiConnector
from app.services.wallet.wallet_api import IWallet


async def setup_bot(cfg: BaseSettings, scheduler: AsyncIOScheduler, db: IDAO, ai: IAiConnector, wallet: IWallet) -> tuple[Dispatcher, Bot]:
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(cfg.bot_token.get_secret_value())

    setup_handlers(dp)
    setup_middlewares(cfg, scheduler, dp, db, ai, wallet)
    setup_dialogs(dp)
    return dp, bot


async def start_bot(dp: Dispatcher, bot: Bot) -> None:
    logging.info(f"Bot started: @{(await bot.get_me()).username}")
    await dp.start_polling(bot)
