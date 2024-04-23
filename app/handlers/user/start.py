from aiogram import Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import MessageInput

from app import states
from app.services.ai.implementations.chatgpt import ChatGptConnector


user_start_router = Router()


@user_start_router.message(CommandStart())
async def send_start_message(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(states.user.MainMenu.MAIN_STATE, mode=StartMode.RESET_STACK)


async def test(message: Message, widget: MessageInput, dialog_manager: DialogManager) -> None:
    if not message.caption and not message.text:
        return
    await message.answer("Обрабатываю...")
    ai: ChatGptConnector = dialog_manager.middleware_data["ai"]

    prompt = """
Найди в этом тексте модель машины, основные характеристики и прочее описание.
Отправь найденную информацию строго в формате ниже, вставив её вместо фигурных скобок.
Сохраняй HTML-теги. ОБЯЗАТЕЛЬНО УДАЛИ ВСЕ ЭМОДЗИ.
Если какой-то информации нет в тексте - просто пропусти это поле.

Модель: <b>{модель машины}</b>

<b>Год выпуска:</b> {год выпуска}
<b>Пробег:</b> {информация о пробеге}
<b>Двигатель:</b> {характеристики двигателя}
<b>Тип КПП:</b> {тип кпп из текста}
<b>Владельцы:</b> {количество владельцев}
<b>Цена:</b> {цена на автомобиль}
<b>Город:</b> {тут указывай населенный пункт}
<b>Связь:</b> {тут укажи номер телефона или указанную в объявлении ссылку}

<b>Описание:</b>
{описание. Здесь напиши весь остальной текст без года выпуска, пробега, двигателя, номера телефона, ссылок}

Если в тексте не нашлось какой-то информации, то вместо неё пиши "информация отсутствует".
Если в тексте есть ссылки, реклама или розыгрыши, то пришли мне слово "РЕКЛАМА".

Вот текст:\n
"""

    await message.answer_photo(
        photo=message.photo[0].file_id,
        caption=ai.convert_text(prompt=prompt, original_text=message.caption),
        parse_mode="HTML"
    )


start_window = Window(
    Const("Добро пожаловать и бла-бла-бла"),
    MessageInput(test),
    state=states.user.MainMenu.MAIN_STATE
)


start_dialog = Dialog(
    start_window
)


def setup_start(dp: Dispatcher) -> None:
    dp.include_routers(user_start_router, start_dialog)
