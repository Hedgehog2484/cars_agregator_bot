from sqlalchemy import Table, Column, Integer, Boolean, String, Float, DateTime
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
