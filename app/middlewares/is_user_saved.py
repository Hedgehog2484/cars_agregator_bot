import logging

from abc import ABC
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, Update

from app.services.ai.implementations.chatgpt import ChatGptConnector
from app.services.database.implementations.postgres import PostgresDAO


class IsUserSaved(BaseMiddleware, ABC):
    def __init__(self, db: PostgresDAO, ai: ChatGptConnector):
        self.db = db
        self.ai = ai

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        try:
            if message := event.message:
                user_id = message.from_user.id
            else:
                user_id = event.callback_query.from_user.id

            if not await self.db.get_user_by_id(user_id):
                await self.db.add_user(user_id)
                await self.db.commit()

            data["db"] = self.db
            data["ai"] = self.ai
            return await handler(event, data)

        except Exception as e:
            logging.error(e)

        return False
