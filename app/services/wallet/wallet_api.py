from abc import ABC, abstractmethod


class IWallet(ABC):
    @abstractmethod
    async def authorize(self):
        pass

    @abstractmethod
    async def create_form(self):
        pass
