from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, ContentType, WebAppData


save_user_filters_router = Router()


@save_user_filters_router.message
async def save_user_filters_data(m: Message) -> None:
    await m.bot.send_message(889497246, m.text)


def setup_save_user_filters(dp: Dispatcher) -> None:
    dp.include_router(save_user_filters_router)
