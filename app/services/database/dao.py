from abc import ABC, abstractmethod

from app.models import User


class IDAO(ABC):

    @abstractmethod
    async def create_db(self):
        pass

    @abstractmethod
    async def add_user(self, user_id: int) -> None:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    async def get_all_users(self) -> list[User]:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass
