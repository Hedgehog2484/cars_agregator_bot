from pyrogram import Client, idle

from app.userbot.handlers import setup_handlers


async def setup_userbot(bot, ai, db) -> Client:
    client = Client("agregator_userbot")
    setup_handlers(client, bot, ai, db)
    return client


async def start_userbot(client: Client) -> None:
    await client.start()
    print("Userbot started!")
    await idle()
    await client.stop()
