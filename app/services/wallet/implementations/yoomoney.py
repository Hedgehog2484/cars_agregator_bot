import json
import logging
import aiohttp

from app.services.wallet.wallet_api import IWallet


class YoomoneyWallet(IWallet):
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            base_api_url: str,
            redirect_url: str
    ):
        self._client_id = client_id
        self._client_secret = client_secret
        self._base_api_url = base_api_url
        self._redirect_url = redirect_url

    async def authorize(self):
        params = {
            "client_id": self._client_id,
            "response_type": "code",
            "redirect_uri": self._redirect_url,
            "scope": "account-info%20operation-history%20operation-details"
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self._base_api_url}/oauth/authorize", headers=headers, data=params) as resp:
                if resp.status != 200:  # TODO: добавить больше проверок на статус (мб когда-нибудь).
                    logging.error(await resp.text())
                    return
                print(resp.url)
                code = str(input("Enter code: "))

            params = {
                "code": code,
                "client_id": self._client_id,
                "grant_type": "authorization_code",
                "redirect_uri": self._redirect_url,
                "client_secret": self._client_secret
            }
            async with session.post(f"{self._base_api_url}/oauth/token", data=params) as resp:
                data = json.loads(await resp.text())
                if token := data.get("access_token"):
                    print(token)
                else:
                    print(data.get("error"))

    async def _get_token(self):
        pass

    async def create_form(self):
        pass
