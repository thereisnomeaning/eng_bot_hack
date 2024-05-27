import requests
import json
from config import IAM_TOKEN, FOLDER_ID


def text_to_speech(text):
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    with open(FOLDER_ID, 'r') as file:
        data = {
            'text': text,  # текст, который нужно преобразовать в голосовое сообщение
            'lang': 'en-US',  # язык текста - русский
            'voice': 'john',
            'folderId': file.read()
        }

    with open(IAM_TOKEN, 'r') as f:
        file_data = json.load(f)
        iam_token = file_data["access_token"]
        headers = {'Authorization': f'Bearer {iam_token}'}
    response = requests.post(url=url, headers=headers, data=data)
    # Проверяем, не произошла ли ошибка при запросе
    if response.status_code == 200:
        return True, response.content  # возвращаем статус и аудио
    else:
        return False, "При запросе в SpeechKit возникла ошибка"


def speech_to_text(text, language):
    with open(IAM_TOKEN, 'r') as f:
        file_data = json.load(f)
        iam_token = file_data["access_token"]
        headers = {'Authorization': f'Bearer {iam_token}'}
    if language == 'english':
        with open(FOLDER_ID, 'r') as file:
            params = "&".join([
                "topic=general",  # используем основную версию модели
                f"folderId={file.read()}",
                "lang=en-US"  # распознаём голосовое сообщение на русском языке
            ])
        url = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?' + params
        response = requests.post(url=url, headers=headers, data=text)
    elif language == 'russian':
        with open(FOLDER_ID, 'r') as file:
            params = "&".join([
                "topic=general",  # используем основную версию модели
                f"folderId={file.read()}",
                "lang=ru-RU"  # распознаём голосовое сообщение на русском языке
            ])
            url = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?' + params

        response = requests.post(url=url, headers=headers, data=text)

    decoded_data = response.json()

    # Проверяем, не произошла ли ошибка при запросе
    if decoded_data.get("error_code") is None:
        return True, decoded_data.get("result")  # Возвращаем статус и текст из аудио
    else:
        return False, "При запросе в SpeechKit возникла ошибка"