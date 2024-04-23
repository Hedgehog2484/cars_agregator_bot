import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs


from app.config import cfg
from app.handlers import setup_handlers
from app.utils.logger import setup_logger
from app.middlewares import setup_middlewares
from app.services.ai.implementations.chatgpt import ChatGptConnector
from app.services.database.implementations.postgres import PostgresDAO


async def setup(dp: Dispatcher) -> None:
    setup_logger(cfg.logger_level)
    db = PostgresDAO(cfg.database_url.get_secret_value())
    await db.create_db()
    ai = ChatGptConnector(cfg.ai_api_key.get_secret_value(), cfg.ai_base_url)
    ai.connect()
    setup_middlewares(dp, db, ai)
    setup_dialogs(dp)
    setup_handlers(dp)


async def main() -> None:
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(cfg.bot_token.get_secret_value())
    await setup(dp)

    logging.info(f"Bot started: @{(await bot.get_me()).username}")
    await dp.start_polling(bot)
