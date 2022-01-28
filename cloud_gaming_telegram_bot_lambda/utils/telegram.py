from json import dumps
from urllib3 import PoolManager
from os import getenv
import certifi


class Telegram:
    TOKEN: str = None
    HTTP_CLIENT: PoolManager = None
    API_URL_TEMPLATE: str = "https://api.telegram.org/bot{token}/{method}"

    def __init__(self):
        if getenv("LAMBDA_TELEGRAM_TOKEN") is False or None:
            self.TOKEN = ""
        else:
            self.TOKEN = getenv("LAMBDA_TELEGRAM_TOKEN")

        self.HTTP_CLIENT = PoolManager(ca_certs=certifi.where())

    def method_url(self, method: str) -> str:

        return self.API_URL_TEMPLATE.format(token=self.TOKEN, method=method)

    def send_payload(self, url: str, d: dict):
        self.HTTP_CLIENT.request(
            "POST", url, body=dumps(d), headers={"Content-Type": "application/json"}
        )

    def send_pending(self, chat_id: str) -> None:
        self.send_payload(
            self.method_url("sendChatAction"), {"chat_id": chat_id, "action": "typing"}
        )
