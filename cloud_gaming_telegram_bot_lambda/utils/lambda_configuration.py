from os import getenv
from typing import Optional


class LambdaConfiguration:
    def __init__(self):
        pass

    @staticmethod
    def get_telegram_token() -> Optional[str]:
        try:
            return getenv("LAMBDA_FUNC_TELEGRAM_TOKEN")
        except KeyError:
            raise SystemError("We have no Telegram token! Bailing...")

    @staticmethod
    def get_azure_compute_token() -> Optional[str]:
        try:
            return getenv("LAMBDA_FUNC_AZURE_COMPUTE_TOKEN")
        except KeyError:
            raise SystemError("We have no Telegram token! Bailing...")

    @staticmethod
    def get_telegram_owner_id() -> Optional[str]:
        try:
            return getenv("LAMBDA_FUNC_TELEGRAM_OWNER_ID")
        except KeyError:
            raise SystemError("We have no Telegram token! Bailing...")
