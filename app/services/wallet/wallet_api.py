from datetime import datetime
from abc import ABC, abstractmethod


class IWallet(ABC):
    _base_api_url: str

    @abstractmethod
    async def authorize(self):
        pass

    @abstractmethod
    async def create_payment_form(self, sum: float, user_id: int, success_url: str | None) -> str | None:
        pass

    @abstractmethod
    async def get_operations_history(
            self,
            operations_type: str | None,
            label: str | None,
            from_time: datetime | None,
            till_time: datetime | None,
            offset: int | None,
            records_count: int | None,
            **kwargs
    ) -> list:
        pass
