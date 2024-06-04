import json
import logging
import aiohttp

from app.services.wallet.wallet_api import IWallet


class YoomoneyWallet(IWallet):
    _session: aiohttp.ClientSession

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            base_api_url: str,
            redirect_url: str,
            auth_token: str,
            receiver_number: str,
            payment_type: str,
    ):
        self._client_id = client_id
        self._client_secret = client_secret
        self._base_api_url = base_api_url
        self._redirect_url = redirect_url
        self._auth_token = auth_token
        self._receiver_number = receiver_number
        self._payment_type = payment_type

        self._session = aiohttp.ClientSession()

    async def authorize(self) -> None:
        """ Use only when new auth token is need. """
        params = {
            "client_id": self._client_id,
            "response_type": "code",
            "redirect_uri": self._redirect_url,
            "scope": "account-info operation-history operation-details",
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        async with aiohttp.ClientSession() as session:
            url = f"{self._base_api_url}/oauth/authorize"
            async with session.post(url, headers=headers, data=params) as resp:
                if resp.status != 200:
                    logging.error(await resp.text())
                    return
                print(resp.url)
                code = str(input("Enter code: "))

            params = {
                "code": code,
                "client_id": self._client_id,
                "grant_type": "authorization_code",
                "redirect_uri": self._redirect_url,
                "client_secret": self._client_secret,
            }
            url = f"{self._base_api_url}/oauth/token"
            async with session.post(url, data=params) as resp:
                data = json.loads(await resp.text())
                if token := data.get("access_token"):
                    print(token)
                else:
                    print(data.get("error"))

    async def close_session(self) -> None:
        await self._session.close()

    async def create_payment_form(self, sum: float, user_id: int, success_url: str | None) -> str | None:
        url = f"{self._base_api_url}/quickpay/confirm"

        params = {
            "receiver": self._receiver_number,
            "quickpay-form": "button",
            "paymentType": self._payment_type,
            "sum": str(sum),
            "label": "",
            "successURL": success_url,
        }

        async with self._session.post(url, data=params) as resp:
            if resp.status != 200:
                logging.error(await resp.text())
                return
        return str(resp.url)
