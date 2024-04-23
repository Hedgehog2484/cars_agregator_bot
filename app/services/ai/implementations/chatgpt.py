from openai import OpenAI

from app.services.ai.ai_connector import IAiConnector


class ChatGptConnector(IAiConnector):
    _api_key: str
    _base_url: str
    _client: OpenAI

    def __init__(self, api_key: str, base_url: str):
        self._api_key = api_key
        self._base_url = base_url

    def connect(self):
        self._client = OpenAI(
            api_key=self._api_key,
            base_url=self._base_url
        )

    def convert_text(self, prompt: str, original_text: str) -> str:
        chat_completion = self._client.chat.completions.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt + original_text}]
        )
        return chat_completion.choices[0].message.content
