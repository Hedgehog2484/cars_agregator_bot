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
    async def add_subscription(self, user_id: int, days: int) -> None:
        pass

    @abstractmethod
    async def reset_subscription(self, user_id: int) -> None:
        pass

    @abstractmethod
    async def update_user_trial_status(self, user_id: int) -> None:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    async def get_all_users(self) -> list[User]:
        pass

    @abstractmethod
    async def add_user_filters(self, user_id: int) -> None:
        pass

    @abstractmethod
    async def get_users_ids_by_filters(
            self,
            model: str = None,
            price_min: int = None,
            price_max: int = None,
            mileage_min: int = None,
            mileage_max: int = None,
            city: list[str] = None
    ) -> list[int]:
        pass

    @abstractmethod
    async def delete_user_filters(self, user_id: int) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass
