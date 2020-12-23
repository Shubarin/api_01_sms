import logging
import os
import sys
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client


load_dotenv()
LOG_FILENAME = "programm.log"
VK_URL_API = "https://api.vk.com/method/users.get"
VK_ACCESS_TOKEN = os.getenv("VK_ACCESS_TOKEN")
VK_API_VERSION = 5.92
NUMBER_FROM = os.getenv("NUMBER_FROM")
NUMBER_TO = os.getenv("NUMBER_TO")
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

logging.basicConfig(level=logging.DEBUG,
                    filename=LOG_FILENAME,
                    filemode="a",
                    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s')

client = Client(ACCOUNT_SID, AUTH_TOKEN)


class HTTPError(Exception):
    pass


def get_status(user_id):
    params = {
        "user_ids": user_id,
        "fields": "online",
        "v": VK_API_VERSION,
        "access_token": VK_ACCESS_TOKEN
    }
    is_online = 0  # по-умолчанию считаем, что что-то пошло не так
    try:
        response = requests.post(VK_URL_API, params=params)
        response_json = response.json()
        # Проверяем что данные пришли
        if not response_json:
            raise HTTPError("Проблемы соединения")
        is_online = response_json.get("response")[0].get("online")
    except HTTPError as error:
        logging.error(error, exc_info=True)
    except KeyError as error:
        logging.error(error, exc_info=True)
    except IndexError as error:
        logging.error(error, exc_info=True)
    except Exception as error:
        logging.error(error, exc_info=True)
    finally:
        return is_online


def sms_sender(sms_text):
    message = client.messages \
        .create(
        body=sms_text,
        from_=NUMBER_FROM,
        to=NUMBER_TO
    )
    return message.sid


if __name__ == "__main__":
    try:
        vk_id = input("Введите id ")
        # Проверяем что пользователь ввел только цифры
        if not all([ch.isdigit() for ch in vk_id]):
            raise ValueError
    except ValueError as error:
        logging.error(error, exc_info=True)
        sys.exit()
    else:
        while True:
            if get_status(vk_id) == 1:
                sms_sender(f"{vk_id} сейчас онлайн!")
                break
            time.sleep(5)
