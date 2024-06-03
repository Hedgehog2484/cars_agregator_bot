from abc import ABC, abstractmethod


class IWallet(ABC):
    base_api_url: str

    @abstractmethod
    async def authorize(self):
        pass

    @abstractmethod
    async def create_form(self):
        pass
