from dataclasses import dataclass


@dataclass
class UserFilters:
    user_id: int
    model: str
    price_min: str
    price_max: str
    mileage_min: int
    mileage_max: int
    city: list[str]
