import re
import _io
import logging
import datetime

from aiogram import Bot
from aiogram.types import BufferedInputFile, InputMediaPhoto
from pyrogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.services.ai.ai_connector import IAiConnector
from app.services.database.dao import IDAO


def get_filters_values_from_text(text: str) -> dict:
    lines = text.splitlines()

    res = {
        "model": re.findall(r"<b>(.*?)</b>", lines[0])[0].lower(),  # In this case model = vendor.
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


async def posts_mailing(users_ids: list, message_text: str, media: list[InputMediaPhoto], bot: Bot) -> None:
    logging.debug(f"ID пользователей для рассылки: {users_ids}")
    media[0].caption = message_text
    media[0].parse_mode = "HTML"
    for user_id in users_ids:
        try:
            await bot.send_media_group(
                chat_id=user_id,
                media=media
            )
        except Exception as e:
            logging.error(e)


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
    # img = await message.download(in_memory=True)  # LMAO it returns _io.BytesIO, not str.
    try:
        media = await message.get_media_group()
    except Exception as e:
        return
    if len(media) < 3:
        logging.info("Media in message < 3")
        return
    downloaded_media_list = []
    i = 0
    for img in media:
        i += 1
        b = BufferedInputFile(
            file=(await img.download(in_memory=True)).getvalue(), # Remember! download returns _io.BytesIO not str.
            filename="img" + str(i)
        )
        downloaded_media_list.append(
            InputMediaPhoto(media=b)
        )
    message_text = ai.convert_text(prompt=prompt, original_text=message.caption)
    if message_text == "РЕКЛАМА":
        logging.debug("реклама")
        return

    # TODO: выгружать пользователей частями (и скорее всего прям в ф-ии posts_mailing).
    users_ids = await db.get_users_ids_by_filters(**get_filters_values_from_text(message_text))
    logging.error(f"users: {users_ids}")
    await posts_mailing(users_ids, message_text, downloaded_media_list, bot)
    """
    scheduler.add_job(
        func=posts_mailing,
        trigger="date",
        run_date=datetime.datetime.now(),
        args=(users_ids, message_text, downloaded_media_list, bot)
    )
    """
