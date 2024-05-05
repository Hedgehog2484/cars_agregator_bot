from datetime import datetime
from dataclasses import dataclass


@dataclass
class User:
    id: int
    is_admin: bool
    subscription_ends: datetime
