import logging

from abc import ABC
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, Update

from app.services.ai.ai_connector import IAiConnector
from app.services.wallet.wallet_api import IWallet
from app.services.database.implementations.postgres import PostgresDAO


class IsUserSaved(BaseMiddleware, ABC):
    def __init__(self, cfg, scheduler, db: PostgresDAO, ai: IAiConnector, wallet: IWallet):
        self.cfg = cfg
        self.scheduler = scheduler
        self.db = db
        self.ai = ai
        self.wallet = wallet

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

            data["cfg"] = self.cfg
            data["scheduler"] = self.scheduler
            data["db"] = self.db
            data["ai"] = self.ai
            data["wallet"] = self.wallet
            data["event_user_id"] = user_id
            return await handler(event, data)

        except Exception as e:
            logging.error(e)

        return False
