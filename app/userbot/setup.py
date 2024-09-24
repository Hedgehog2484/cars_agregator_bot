from pyrogram import Client, idle

from app.userbot.handlers import setup_handlers


async def setup_userbot(bot, ai, db, scheduler) -> Client:
    client = Client("agregator_userbot", api_id=20445262, api_hash="125f3038dbfc64326ba9ab2bdcf09e2b")
    setup_handlers(client, bot, ai, db, scheduler)
    return client


async def start_userbot(client: Client) -> None:
    await client.start()
    print("Userbot started!")
    await idle()
    await client.stop()
