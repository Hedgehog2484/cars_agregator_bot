import logging
import datetime

from sqlalchemy import insert, select, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine, async_sessionmaker

from app.services.database.dao import IDAO
from app.models import User, UserFilters
from app.services.database.implementations.orm_models import (
    postgres_mapper_registry,
    users_table,
    filters_table
)


class PostgresDAO(IDAO):
    _engine: AsyncEngine
    _session: AsyncSession

    def __init__(self, database_url: str):
        self._engine = create_async_engine(database_url)
        NewAsyncSession = async_sessionmaker(bind=self._engine)
        self._session = NewAsyncSession()

    async def create_db(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(postgres_mapper_registry.metadata.create_all)

    async def add_user(self, user_id: int, is_admin: bool = False) -> None:
        q = insert(users_table).values(tg_id=user_id, is_admin=is_admin, subscription_ends=None, is_trial_used=False)
        await self._session.execute(q)

    async def add_subscription(self, user_id: int, end_date: datetime.date) -> None:
        q = update(users_table).where(users_table.c.id == user_id).values(subscription_ends=end_date)
        await self._session.execute(q)

    async def reset_subscription(self, user_id: int) -> None:
        q = update(users_table).where(users_table.c.id == user_id).values(
            subscription_ends=datetime.date.today() - datetime.timedelta(days=1)
        )
        await self._session.execute(q)

    async def update_user_trial_status(self, user_id: int) -> None:
        q = update(users_table).where(users_table.c.tg_id == user_id).values(is_trial_used=True)

    async def get_user_by_id(self, user_id: int) -> User | None:
        q = select(users_table.c).where(users_table.c.tg_id == user_id)
        res = await self._session.execute(q)
        u = res.fetchone()
        return User(*u) if u else None

    async def get_users_ids_by_subscription_end_date(self, subscription_end_date: datetime.date) -> list[int]:
        q = select(users_table.c.id).where(users_table.c.subscription_ends == subscription_end_date)
        res = await self._session.execute(q)
        ids = []
        for user_id in res.all():
            ids.append(user_id[0])
        return ids

    async def get_all_users(self) -> list[User]:
        q = select(users_table.c)
        res = await self._session.execute(q)
        users = []
        for user in res.all():
            users.append(User(*user))
        return users

    async def create_user_filters(self, user_id: int) -> None:
        q = insert(filters_table).values(user_tg_id=user_id)
        await self._session.execute(q)

    async def update_user_filters(self, user_filters: UserFilters) -> None:
        q = update(filters_table).where(filters_table.c.user_tg_id == user_filters.user_id).values(
            model=user_filters.model,
            price_min=user_filters.price_min,
            price_max=user_filters.price_max,
            mileage_min=user_filters.mileage_min,
            mileage_max=user_filters.mileage_max,
            manufacture_year_min=user_filters.manufacture_year_min,
            manufacture_year_max=user_filters.manufacture_year_max,
            city=user_filters.city
        )
        await self._session.execute(q)

    async def get_filters_by_user_id(self, user_id: int) -> UserFilters | None:
        q = select(filters_table.c).where(filters_table.c.user_tg_id == user_id)
        res = await self._session.execute(q)
        uf = res.fetchone()
        return UserFilters(*uf) if uf else None

    async def get_users_ids_by_filters(
            self,
            model: str | None = None,
            price: int | None = None,
            mileage: int | None = None,
            manufacture_year: int | None = None,
            city: list[str] | None = None
    ) -> list[int]:
        q = select(filters_table.c.user_tg_id).where(
            and_(
                filters_table.c.price_min <= price,
                filters_table.c.price_max >= price,
                filters_table.c.mileage_min <= mileage,
                filters_table.c.mileage_max >= mileage,
                filters_table.c.manufacture_year_min <= manufacture_year,
                filters_table.c.manufacture_year_max >= manufacture_year
            )
        ).filter(filters_table.partners.any(model))
        res = await self._session.execute(q)
        ids = []
        for user_id in res.all():
            ids.append(user_id[0])
        return ids

    async def delete_user_filters(self, user_id: int) -> None:
        # TODO: don't forget to use this when subscription is ends.
        q = delete(filters_table).where(filters_table.c.user_tg_id == user_id)
        await self._session.execute(q)

    async def commit(self) -> None:
        await self._session.commit()
