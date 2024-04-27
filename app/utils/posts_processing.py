import _io

from aiogram import Bot
from aiogram.types import BufferedInputFile
from pyrogram.types import Message

from app.services.ai.ai_connector import IAiConnector
from app.services.database.dao import IDAO


async def processing(message: Message, bot: Bot, ai: IAiConnector, db: IDAO) -> None:
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
    img = await message.download(in_memory=True)  # LMAO it returns _io.BytesIO, not str.
    # message_text = ai.convert_text(prompt=prompt, original_text=message.caption)

    await bot.send_photo(
        chat_id=889497246,
        photo=BufferedInputFile(file=img.getvalue(), filename="filename"),
        caption=message.caption,
        parse_mode="HTML"
    )
