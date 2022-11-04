import json
from utils.telegram import Telegram


def telegram_handler(evt: dict):
    t = Telegram()
    body = json.loads(evt["body"])

    t.handle_update(body)


def lambda_handler(evt: dict, _ctx: dict) -> dict:
    if "message" in json.loads(evt["body"]):
        # This is a call from Telegram
        telegram_handler(evt)
    elif "state" in json.loads(evt["body"])["payload"]:
        # This is a call from the Azure VM, but this isn't coded yet! TODO.
        return {"statusCode": 400}
    else:
        pass

    return {"statusCode": 200}
