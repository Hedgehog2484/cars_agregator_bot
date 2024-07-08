from .start import setup_start
from .subscription import setup_subscription


def setup_user(dp) -> None:
    setup_start(dp)
    setup_subscription(dp)
