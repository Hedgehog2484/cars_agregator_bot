from .user import setup_user


def setup_handlers(dp) -> None:
    setup_user(dp)
