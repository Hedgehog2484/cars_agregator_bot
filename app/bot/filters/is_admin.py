from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class IsAdminFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery, **kwargs):
        if (await kwargs["db"].get_user_by_id(callback.from_user.id)).is_admin:
            return True
        return False
