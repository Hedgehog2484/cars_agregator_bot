from app.services.database.implementations.postgres import PostgresDAO
from app.models import UserFilters


async def save_user_settings(data: dict, db: PostgresDAO):
    filters = UserFilters(
        user_id=int(data.get("user_id")),
        model=data.get("model"),
        price_min=data.get("price_min"),
        price_max=data.get("price_max"),
        mileage_min=data.get("mileage_min"),
        mileage_max=data.get("mileage_max"),
        manufacture_year_min=data.get("manufacture_year_min"),
        manufacture_year_max=data.get("manufacture_year_max"),
        city=[]
    )
    await db.update_user_filters(filters)
    await db.commit()
