from abc import ABC, abstractmethod


class IWallet(ABC):
    _base_api_url: str

    @abstractmethod
    async def authorize(self):
        pass

    @abstractmethod
    async def create_payment_form(self, sum: float, user_id: int, success_url: str | None) -> str | None:
        pass
