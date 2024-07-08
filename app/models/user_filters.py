from dataclasses import dataclass


@dataclass
class UserFilters:
    user_id: int
    model: list[str]
    price_min: int
    price_max: int
    mileage_min: int
    mileage_max: int
    city: list[str]
