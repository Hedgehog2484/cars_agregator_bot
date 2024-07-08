from sqlalchemy import Table, Column, Integer, Boolean, String, Float, DateTime, ForeignKey
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

# TODO: прописать дефолтные значения.
filters_table = Table(
    "users_filters",
    postgres_mapper_registry.metadata,
    Column("user_tg_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("model", ARRAY(String), nullable=True),
    Column("price_min", Integer, nullable=True),
    Column("price_max", Integer, nullable=True),
    Column("mileage_min", Integer, nullable=True),
    Column("mileage_max", Integer, nullable=True),
    Column("city", ARRAY(Integer), nullable=True)
)
