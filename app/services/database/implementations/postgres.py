from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine, async_sessionmaker

from app.services.database.dao import IDAO
from app.models import User
from app.services.database.implementations.orm_models import (
    postgres_mapper_registry, users_table
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
        q = insert(users_table).values(tg_id=user_id, is_admin=is_admin)
        await self._session.execute(q)

    async def get_user_by_id(self, user_id: int) -> User | None:
        q = select(users_table.c).where(users_table.c.tg_id == user_id)
        res = await self._session.execute(q)
        u = res.fetchone()
        return User(*u) if u else None

    async def get_all_users(self) -> list[User]:
        q = select(users_table.c)
        res = await self._session.execute(q)
        users = []
        for user in res.all():
            users.append(User(*user))
        return users

    async def commit(self) -> None:
        await self._session.commit()
