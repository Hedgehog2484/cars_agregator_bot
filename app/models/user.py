from dataclasses import dataclass


@dataclass
class User:
    id: int
    is_admin: bool
