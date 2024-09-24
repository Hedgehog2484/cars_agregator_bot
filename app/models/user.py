from datetime import date
from dataclasses import dataclass


@dataclass
class User:
    id: int
    is_admin: bool
    subscription_ends: date
    is_trial_used: bool
