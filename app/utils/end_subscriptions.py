import datetime

from aiogram import Bot

from app.services.database.dao import IDAO


async def check_end_subscriptions(bot: Bot, db: IDAO) -> None:
    msg_text = """
Приветствуем!
К сожалению, ваша подписка подошла к концу. Чтобы продолжить пользоваться данным сервисом необходимо купить подписку заново.
Спасибо, что выбрали нас!
<i>С уважением, команда ВсеТачки.Ру</i>
"""
    for user_id in await db.get_users_ids_by_subscription_end_date(datetime.date.today()):
        await bot.send_message(user_id, msg_text, parse_mode="HTML")
        await db.delete_user_filters(user_id)
    await db.commit()
