from .channel_post import setup_channel_post


def setup_handlers(client, bot, ai, db, scheduler) -> None:
    setup_channel_post(client, bot, ai, db, scheduler)
