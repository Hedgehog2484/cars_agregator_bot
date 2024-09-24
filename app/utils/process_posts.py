import re
import _io
import datetime

from aiogram import Bot
from aiogram.types import BufferedInputFile
from pyrogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.services.ai.ai_connector import IAiConnector
from app.services.database.dao import IDAO


def get_filters_values_from_text(text: str) -> dict:
    lines = text.splitlines()

    res = {
        "model": re.findall(r"<b>(.*?)</b>", lines[0])[0],  # In this case model = vendor.
        "manufacture_year": None,
        "mileage": None,
        "price": None,
        "city": None
    }

    try:
        year = int(re.findall(r"\d+", lines[3])[0])
        res["manufacture_year"] = year
    except IndexError:
        pass
    except ValueError:
        pass

    try:
        mileage = int("".join(re.findall(r"\d+", lines[4])[0]))
        res["mileage"] = mileage
    except IndexError:
        pass
    except ValueError:
        pass

    try:
        price = int("".join(re.findall(r"\d+", lines[8])[0]))
        res["price"] = price
    except IndexError:
        pass
    except ValueError:
        pass

    return res


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

Производитель: <b>{компания-производитель машины на английском}</b>
Модель: <b>{модель машины на английском}</b>

<b>Год выпуска:</b> {год выпуска}
<b>Пробег:</b> {информация о пробеге}
<b>Двигатель:</b> {характеристики двигателя}
<b>Тип КПП:</b> {тип кпп из текста}
<b>Владельцы:</b> {количество владельцев}
<b>Цена:</b> {цена на автомобиль}
<b>Город:</b> {тут указывай населенный пункт}
<b>Связь:</b> {тут укажи указанные в объявлении контакты для связи}

<b>Описание:</b>
{описание. Здесь напиши весь остальной текст без года выпуска, пробега, двигателя, номера телефона, ссылок}

Если в тексте не нашлось какой-то информации, то вместо неё пиши "информация отсутствует".
Если в тексте есть рекламные ссылки, реклама или розыгрыши, то отправь мне только слово "РЕКЛАМА".

Вот текст:\n
"""
    img = await message.download(in_memory=True)  # LMAO it returns _io.BytesIO, not str.
    message_text = ai.convert_text(prompt=prompt, original_text=message.caption)
    if message_text == "РЕКЛАМА":
        return

    # TODO: выгружать пользователей частями (и скорее всего прям в ф-ии posts_mailing).
    users_ids = await db.get_users_ids_by_filters(**get_filters_values_from_text(message_text))
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
