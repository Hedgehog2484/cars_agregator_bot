from .start import setup_start
from .subscription import setup_subscription
from .save_user_filters import setup_save_user_filters


def setup_user(dp) -> None:
    setup_save_user_filters(dp)
    setup_start(dp)
    setup_subscription(dp)
