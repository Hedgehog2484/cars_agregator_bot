from aiogram.filters.state import State, StatesGroup


class MainMenu(StatesGroup):
    MAIN_STATE = State()
    TRIAL_STARTED = State()


class BuySubscription(StatesGroup):
    PAYMENT = State()
    PAYMENT_RECEIVED = State()
    PAYMENT_CANCELED = State()
