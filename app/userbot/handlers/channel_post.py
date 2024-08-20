from functools import partial

from aiogram import Bot
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram.filters import channel_filter, caption_filter, \
    text_filter, photo_filter

from app.utils.process_posts import processing
from app.services.ai.ai_connector import IAiConnector
from app.services.database.dao import IDAO


async def new_post_handler(
        client: Client,
        message: Message,
        bot: Bot,
        ai: IAiConnector,
        db: IDAO,
        scheduler: AsyncIOScheduler
) -> None:
    if not message.caption and not message.text:
        return

    await processing(message, bot, ai, db, scheduler)


def setup_channel_post(
        client: Client,
        bot: Bot,
        ai: IAiConnector,
        db: IDAO,
        scheduler: AsyncIOScheduler
) -> None:
    client.add_handler(
        MessageHandler(
            partial(new_post_handler, bot=bot, ai=ai, db=db, scheduler=scheduler),
            filters=[
                channel_filter,
                caption_filter,
                photo_filter,
                not text_filter
            ]
        )
    )
