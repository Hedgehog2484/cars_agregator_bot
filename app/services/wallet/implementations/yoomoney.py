from app.services.wallet.wallet_api import IWallet


class YoomoneyWallet(IWallet):
    async def authorize(self):
        pass

    async def _get_token(self):
        pass

    async def create_form(self):
        pass
