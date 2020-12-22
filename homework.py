import os
import time
import requests

from dotenv import load_dotenv
from twilio.rest import Client


load_dotenv()
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)


def get_status(user_id):
    params = {
        "user_ids": user_id,
        "fields": "online",
        "v": 5.92,
        "access_token": os.getenv("VK_ACCESS_TOKEN")
    }
    is_online = requests.post("https://api.vk.com/method/users.get",
                              params=params).json().get("response")[0].get("online")
    return is_online


def sms_sender(sms_text):
    message = client.messages \
        .create(
        body=sms_text,
        from_=os.getenv("NUMBER_FROM"),
        to=os.getenv("NUMBER_TO")
    )
    return message.sid


if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f"{vk_id} сейчас онлайн!")
            break
        time.sleep(5)
