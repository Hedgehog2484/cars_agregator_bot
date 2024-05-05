from datetime import datetime
from aiogram import Dispatcher, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import WebApp, Button
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
    message_text = "Добро пожаловать! На данный момент у вас нет подписки, но вы можете попробовать пробный период"
    if user.subscription_ends is not None:
        is_subscribed = True
        days_left = (user.subscription_ends - datetime.now()).days
        message_text = f"Добро пожаловать, бла-бла.\nДней подписки осталось: <code>{days_left}</code>"

    return {
        "subscribed": is_subscribed,
        "not_subscribed": not is_subscribed,
        "menu_message_text": message_text
    }


async def start_trial(c: CallbackQuery, button: Button, dialog_manager: DialogManager) -> None:
    db: PostgresDAO = dialog_manager.middleware_data["db"]
    # TODO: add flag `is_used_trial`.
    await db.add_subscription(c.from_user.id, 3)
    await db.commit()
    await dialog_manager.switch_to(states.user.MainMenu.MAIN_STATE)


start_window = Window(
    Format("{menu_message_text}"),
    WebApp(Const("Open webapp"), Const("https://0.0.0.0:8432"), "id_wa", when="subscribed"),
    Button(Const("Попробовать бесплатно"), id="start_trial", on_click=..., when="not_subscribed"),
    state=states.user.MainMenu.MAIN_STATE,
    getter=menu_getter
)


start_dialog = Dialog(
    start_window
)


def setup_start(dp: Dispatcher) -> None:
    dp.include_routers(user_start_router, start_dialog)
