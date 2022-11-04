from json import dumps
from urllib3 import PoolManager
from certifi import where as cert_where
from time import sleep
from utils.lambda_configuration import LambdaConfiguration


class Telegram:
    TELEGRAM_TOKEN: str = ""
    HTTP_CLIENT: PoolManager = PoolManager(ca_certs=cert_where())
    API_URL_TEMPLATE: str = "https://api.telegram.org/bot{token}/{method}"
    LAMBDA_CONF: LambdaConfiguration = LambdaConfiguration()

    def __init__(self):
        self.TELEGRAM_TOKEN = self.LAMBDA_CONF.get_telegram_token()

    def handle_update(self, update_json: dict) -> None:
        if "message" in update_json:
            self.__handle_message(update_json["message"])
        elif "callback_query" in update_json:
            self.__handle_callback(update_json["callback_query"])

    def __handle_message(self, message: dict) -> None:
        if message["chat"]["id"] != self.LAMBDA_CONF.get_telegram_owner_id():
            return

        if "from" in message:
            if message["text"] == "/start":
                chat_id: str = message["from"]["id"]
                self.send_typing(chat_id)
                sleep(1)
                self.send_message(chat_id, "Hey!")
                self.send_message(
                    chat_id, "Please confirm your decision to start the VM:"
                )
                # send kb

    def __handle_callback(self, cb: dict) -> None:
        if "from" in cb:
            chat_id: str = cb["from"]["id"]
            # cb_response: str = cb["data"].split(":")
            self.send_message(chat_id, "Processing your callback..")

    def __method_url(self, method: str) -> str:
        return self.API_URL_TEMPLATE.format(token=self.TELEGRAM_TOKEN, method=method)

    def __send_payload(self, url: str, body: dict) -> None:
        self.HTTP_CLIENT.request(
            "POST", url, body=dumps(body), headers={"Content-Type": "application/json"}
        )

    def send_typing(self, chat_id: str) -> None:
        self.__send_payload(
            self.__method_url("sendChatAction"),
            {"chat_id": chat_id, "action": "typing"},
        )

    def send_message(self, user: str, text: str) -> None:
        self.__send_payload(
            self.__method_url("sendMessage"),
            {
                "chat_id": user,
                "text": text,
            },
        )
