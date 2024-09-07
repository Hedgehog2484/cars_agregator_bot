import logging

from datetime import date, timedelta
from aiogram import Dispatcher, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.kbd import WebApp, Button, Start, Back
from aiogram_dialog.widgets.text import Const, Format

from app.bot import states
from app.services.database.implementations.postgres import PostgresDAO


user_start_router = Router()


@user_start_router.message(CommandStart())
async def send_start_message(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(states.user.MainMenu.MAIN_STATE, mode=StartMode.RESET_STACK)


async def menu_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    db: PostgresDAO = dialog_manager.middleware_data["db"]
    user = await db.get_user_by_id(dialog_manager.middleware_data["event_user_id"])
    is_subscribed = False
    # is_subscribed = True
    message_text = """
Добро пожаловать в наш сервис по поиску автомобилей по низу рынка!
Предлагаем вам попробовать пробную подписку — это отличный способ ознакомиться с нашими возможностями и оценить, как мы можем помочь вам.
Также вы можете приобрести подписку в любой момент по цене 299 рублей.
Если у вас возникнут вопросы или потребуется помощь, наша команда всегда готова вам помочь, аккаунт поддержки можете найти в описании бота.
Получите доступ к автомобилям, которых нет на досках объявлений уже сегодня!
С уважением,
команда ВсеТачки.ру
"""
    if user.subscription_ends is not None:
        is_subscribed = True
        days_left = (user.subscription_ends - date.today()).days
        if days_left > 0:
            message_text = f"""
Доброго времени суток!
Дней подписки осталось: <code>{days_left}</code>
"""
        else:
            message_text = f"""
К сожалению, срок действия вашей подписки истёк.
Чтобы продолжить пользоваться сервисом купите подписку, нажав соответствующую кнопку ниже:
"""

    return {
        "subscribed": is_subscribed,
        "is_trial_used": user.is_trial_used,
        "menu_message_text": message_text
    }


async def start_trial(c: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    db: PostgresDAO = dialog_manager.middleware_data["db"]
    user_id = int(c.from_user.id)
    await db.update_user_trial_status(user_id)
    await db.add_subscription(user_id, date.today() + timedelta(days=3))
    await db.commit()
    await dialog_manager.next()


def is_show_trial(data: dict, widget: Whenable, dialog_manager: DialogManager) -> bool:
    return not data["subscribed"] and not data["is_trial_used"]


def is_show_buy_subscription(data: dict, widget: Whenable, dialog_manager: DialogManager) -> bool:
    return not data["subscribed"]


def is_subscribed(data: dict, widget: Whenable, dialog_manager: DialogManager) -> bool:
    return data["subscribed"]


start_window = Window(
    Format("{menu_message_text}"),
    WebApp(Const("Open webapp"), Const("https://pepepu.ru"), id="webapp_btn", when=is_subscribed),
    Button(Const("Попробовать бесплатно"), id="start_trial_btn", on_click=start_trial, when=is_show_trial),
    Start(text=Const("Купить подписку"), id="buy_subscription", state=states.user.BuySubscription.PAYMENT, when=is_show_buy_subscription),
    state=states.user.MainMenu.MAIN_STATE,
    getter=menu_getter
)


trial_activated_window = Window(
    Const("Пробная подписка активирована! Не забудьте настроить фильтры.\nПо всем вопросам обращайтесь к администратору (ссылка в описании бота)"),
    Back(Const("Вернуться в меню"), id="back_btn"),
    state=states.user.MainMenu.TRIAL_STARTED
)


start_dialog = Dialog(
    start_window,
    trial_activated_window
)


def setup_start(dp: Dispatcher) -> None:
    dp.include_routers(user_start_router, start_dialog)
