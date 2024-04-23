from aiogram import Dispatcher

from .is_user_saved import IsUserSaved


def setup_middlewares(dp: Dispatcher, db, ai) -> None:
    dp.update.outer_middleware(IsUserSaved(db, ai))
