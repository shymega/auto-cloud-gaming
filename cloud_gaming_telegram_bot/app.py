import json

from cloud_gaming_telegram_bot.modules.telegram import Telegram


def telegram_handler(evt: dict) -> dict:
    t = Telegram()
    body = json.loads(evt["body"])

    t.handle_update(body)

    return {"statusCode": 200}


def lambda_handler(evt: dict, _ctx: dict) -> dict:
    try:
        if "message" in json.loads(evt["body"]):
            # This is a call from Telegram
            return telegram_handler(evt)
        if "state" in json.loads(evt["body"])["payload"]:
            # This is a call from the AWS VM, but this isn't coded yet! TODO.
            return {"statusCode": 404}
    except KeyError:
        return {"statusCode": 500}

    return {"statusCode": 200}
