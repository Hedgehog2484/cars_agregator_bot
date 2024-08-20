from sqlalchemy import Table, Column, Integer, Boolean, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import registry

postgres_mapper_registry = registry()


users_table = Table(
    "users",
    postgres_mapper_registry.metadata,
    Column("tg_id", Integer, nullable=False, autoincrement=False, primary_key=True),
    Column("is_admin", Boolean, nullable=False),
    Column("subscription_ends", DateTime, nullable=True),
    Column("is_trial_used", Boolean, nullable=False)
)


filters_table = Table(
    "users_filters",
    postgres_mapper_registry.metadata,
    Column("user_tg_id", Integer, ForeignKey("users.tg_id"), nullable=False),
    Column("model", ARRAY(String), nullable=False, default=[]),
    Column("price_min", Integer, nullable=False, default=0),
    Column("price_max", Integer, nullable=False, default=100000000),
    Column("mileage_min", Integer, nullable=False, default=0),
    Column("mileage_max", Integer, nullable=False, default=10000000),
    Column("manufacture_year_min", Integer, nullable=False, default=1900),
    Column("manufacture_year_max", Integer, nullable=False, default=2024),
    Column("city", ARRAY(Integer), nullable=False, default=[])
)
