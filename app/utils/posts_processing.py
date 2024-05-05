import _io
import datetime

from aiogram import Bot
from aiogram.types import BufferedInputFile
from pyrogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.services.ai.ai_connector import IAiConnector
from app.services.database.dao import IDAO


async def posts_mailing(users_ids: list, message_text: str, photo: _io.BytesIO, bot: Bot) -> None:
    for user_id in users_ids:
        try:
            await bot.send_photo(
                chat_id=889497246,
                photo=BufferedInputFile(file=photo.getvalue(), filename="filename"),
                caption=message_text,
                parse_mode="HTML"
            )
        except:
            pass


async def processing(
        message: Message,
        bot: Bot,
        ai: IAiConnector,
        db: IDAO,
        scheduler: AsyncIOScheduler
) -> None:
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
    message_text = ""

    users_ids = await db.get_users_ids_by_filters()  # TODO: как достать данные из объявления???
    scheduler.add_job(
        func=posts_mailing,
        trigger="date",
        run_date=datetime.datetime.now(),
        args=(users_ids, message_text, img, bot)
    )
    """
    await bot.send_photo(
        chat_id=889497246,
        photo=BufferedInputFile(file=img.getvalue(), filename="filename"),
        caption=message.caption,
        parse_mode="HTML"
    )
    """
