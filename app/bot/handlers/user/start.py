from datetime import datetime
from aiogram import Dispatcher, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.kbd import WebApp, Button, Start
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
    # is_subscribed = False
    is_subscribed = True
    message_text = "Добро пожаловать! На данный момент у вас нет подписки, но вы можете попробовать пробный период"
    if user.subscription_ends is not None:
        is_subscribed = True
        days_left = (user.subscription_ends - datetime.now()).days
        message_text = f"Добро пожаловать, бла-бла.\nДней подписки осталось: <code>{days_left}</code>"

    return {
        "subscribed": is_subscribed,
        "is_trial_used": user.is_trial_used,
        "menu_message_text": message_text
    }


async def start_trial(c: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    db: PostgresDAO = dialog_manager.middleware_data["db"]
    user_id: int = c.from_user.id
    await db.update_user_trial_status(user_id)
    await db.add_subscription(user_id, 3)
    await db.commit()
    await dialog_manager.switch_to(states.user.MainMenu.MAIN_STATE)


async def buy_subscription(c: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    pass


def is_show_trial(data: dict, widget: Whenable, dialog_manager: DialogManager) -> bool:
    return not data["subscribed"] and not data["is_trial_used"]


def is_show_buy_subscription(data: dict, widget: Whenable, dialog_manager: DialogManager) -> bool:
    return not data["subscribed"]


start_window = Window(
    Format("{menu_message_text}"),
    WebApp(Const("Open webapp"), Const("https://pepepu.ru"), "id_wa", when="subscribed"),
    Button(Const("Попробовать бесплатно"), id="start_trial", on_click=start_trial, when=is_show_trial),
    # Button(Const("Купить подписку"), id="buy_subscription", on_click=buy_subscription, when=is_show_buy_subscription),
    Start(text=Const("Купить подписку"), id="buy_subscription", state=states.user.BuySubscription.PAYMENT, when=is_show_buy_subscription),
    state=states.user.MainMenu.MAIN_STATE,
    getter=menu_getter
)


start_dialog = Dialog(
    start_window
)


def setup_start(dp: Dispatcher) -> None:
    dp.include_routers(user_start_router, start_dialog)
