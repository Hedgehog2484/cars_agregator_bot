import datetime

from abc import ABC, abstractmethod

from app.models import User, UserFilters


class IDAO(ABC):

    @abstractmethod
    async def create_db(self):
        pass

    @abstractmethod
    async def add_user(self, user_id: int) -> None:
        pass

    @abstractmethod
    async def add_subscription(self, user_id: int, to_date: datetime.date) -> None:
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
    async def get_users_ids_by_subscription_end_date(self, subscription_end_date: datetime.date) -> list[int]:
        pass

    @abstractmethod
    async def get_all_users(self) -> list[User]:
        pass

    @abstractmethod
    async def create_user_filters(self, user_id: int) -> None:
        pass

    @abstractmethod
    async def update_user_filters(self, user_filters: UserFilters) -> None:
        pass

    @abstractmethod
    async def get_filters_by_user_id(self, user_id: int) -> UserFilters | None:
        pass

    @abstractmethod
    async def get_users_ids_by_filters(
            self,
            model: str | None = None,
            price: int | None = None,
            mileage: int | None = None,
            manufacture_year: int | None = None,
            city: list[str] | None = None
    ) -> list[int]:
        pass

    @abstractmethod
    async def delete_user_filters(self, user_id: int) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass
