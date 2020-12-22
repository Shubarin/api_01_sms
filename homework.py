import time
import requests

from twilio.rest import Client


def get_status(user_id):
    params = {
        ...
    }
    ...
    return ...  # Верните статус пользователя в ВК


def send_sms(sms_text, client):
    ...
    return ...  # Верните sid отправленного сообщения из Twilio


if __name__ == '__main__':
    # тут происходит инициализация Client
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            send_sms(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
