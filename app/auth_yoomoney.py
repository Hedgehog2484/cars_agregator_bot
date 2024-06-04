import asyncio

from config import cfg
from services.wallet.implementations.yoomoney import YoomoneyWallet


if __name__ == "__main__":
    yw = YoomoneyWallet(
        client_id=cfg.yoomoney_client_id.get_secret_value(),
        client_secret=cfg.yoomoney_client_secret.get_secret_value(),
        base_api_url=cfg.yoomoney_base_url,
        redirect_url=cfg.yoomoney_redirect_url,
        auth_token=""
    )
    asyncio.run(yw.authorize())
    print("Authorization is ended.")
