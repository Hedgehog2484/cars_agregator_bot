from aiogram import Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.text import Const

from app.bot import states


user_start_router = Router()


@user_start_router.message(CommandStart())
async def send_start_message(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(states.user.MainMenu.MAIN_STATE, mode=StartMode.RESET_STACK)


start_window = Window(
    Const("Добро пожаловать и бла-бла-бла"),
    state=states.user.MainMenu.MAIN_STATE
)


start_dialog = Dialog(
    start_window
)


def setup_start(dp: Dispatcher) -> None:
    dp.include_routers(user_start_router, start_dialog)
