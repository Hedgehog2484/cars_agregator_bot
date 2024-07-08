from aiogram import Dispatcher

from .is_user_saved import IsUserSaved


def setup_middlewares(cfg, scheduler, dp: Dispatcher, db, ai, wallet) -> None:
    dp.update.outer_middleware(IsUserSaved(cfg, scheduler, db, ai, wallet))
