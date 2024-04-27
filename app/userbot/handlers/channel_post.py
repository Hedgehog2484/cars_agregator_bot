from functools import partial

from aiogram import Bot
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from pyrogram.filters import channel_filter, caption_filter, \
    text_filter, photo_filter

from app.utils.posts_processing import processing
from app.services.ai.ai_connector import IAiConnector
from app.services.database.dao import IDAO


async def new_post_handler(client, message: Message, bot: Bot, ai: IAiConnector, db: IDAO):
    if not message.caption and not message.text:
        return

    await processing(message, bot, ai, db)


def setup_channel_post(client: Client, bot: Bot, ai: IAiConnector, db: IDAO) -> None:
    client.add_handler(
        MessageHandler(
            partial(new_post_handler, bot=bot, ai=ai, db=db),
            filters=[
                channel_filter,
                caption_filter,
                photo_filter,
                not text_filter
            ]
        )
    )
