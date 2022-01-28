import json
from time import sleep
from utils.telegram import Telegram


def lambda_handler(evt, ctx):
    t = Telegram()
    req = json.loads(evt["body"])
    msg = evt["message"]
    chat_id = msg["chat"]["id"]

    if "from" in msg:
        if msg["text"] == "/start":




    return {"statusCode": 200}
