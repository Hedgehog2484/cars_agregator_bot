import asyncio
import datetime
import logging

from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from app.bot import states
from app.models.operation import YoomoneyOperation
from app.services.wallet.wallet_api import IWallet
from app.services.database.dao import IDAO


async def finish_dialog(c: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.done()


async def payment_menu_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    cfg = dialog_manager.middleware_data["cfg"]
    amount = cfg.yoomoney_payment_amount
    wallet: IWallet = dialog_manager.middleware_data["wallet"]
    # payment_url = await wallet.create_payment_form(float(amount), dialog_manager.event.from_user.id, cfg.yoomoney_success_url)
    payment_url = await wallet.create_payment_form(10, dialog_manager.event.from_user.id, cfg.yoomoney_success_url)

    return {
        "payment_url": payment_url,
        "payment_amount": amount,
    }


async def check_paid(c: CallbackQuery, button: Button, dialog_manager: DialogManager):
    wallet: IWallet = dialog_manager.middleware_data["wallet"]
    db: IDAO = dialog_manager.middleware_data["db"]

    operations: list[YoomoneyOperation] = await wallet.get_operations_history(
        operations_type="deposition",
        label=str(c.from_user.id),
        records_count=1,
        # from_time=datetime.datetime.now() - datetime.timedelta(days=1),
        # till_time=datetime.datetime.now(),
    )
    operations = []
    logging.info(operations)
    if operations:
        await db.add_subscription(c.from_user.id, 30)
        await db.commit()
        await dialog_manager.switch_to(states.user.BuySubscription.PAYMENT_RECEIVED)
        return
    else:
        await c.answer("Возможно, платёж ещё не дошёл. Попробуйте нажать кнопку через одну минуту.", show_alert=True)
    # await dialog_manager.switch_to(states.user.BuySubscription.PAYMENT_CANCELED)


send_payment_url_window = Window(
    Format(
        "Какой-то текст про подписку и цену.\n"
        "Ваша ссылка для оплаты: {payment_url}\n"
    ),
    Button(Const("Оплатил"), id="paid_btn", on_click=check_paid),
    state=states.user.BuySubscription.PAYMENT,
    getter=payment_menu_getter,

)


payment_received_window = Window(
    Const("Подписка на 30 дней активирована!\n(тут должно быть пожелание)"),
    Button(Const("Вернуться в меню"), id="back_to_menu", on_click=finish_dialog),
    state=states.user.BuySubscription.PAYMENT_RECEIVED
)


payment_canceled_window = Window(
    Const("Мы не получили оплату за выделенное время, но вы всегда можете попробовать ещё раз."),
    Button(Const("Вернуться в меню"), id="back_to_menu", on_click=finish_dialog),
    state=states.user.BuySubscription.PAYMENT_CANCELED
)


buy_subscription_dialog = Dialog(
    send_payment_url_window,
    payment_received_window,
    payment_canceled_window,
)


def setup_buy_subscription(dp: Dispatcher) -> None:
    dp.include_routers(buy_subscription_dialog)
