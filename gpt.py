import requests
import time
import logging
import json
from config import IAM_TOKEN, FOLDER_ID


# Подсчитываем количество токенов в сообщении.
def gpt_tokenizer(user_prompt, sys_prompt):
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion'
    with open(FOLDER_ID, 'r') as file:
        data = {
            "modelUri": f"gpt://{file.read()}/yandexgpt/latest",
            "maxTokens": 200,
            "messages": []
        }
    data["messages"].append(
        {
            "role": 'user',
            "text": user_prompt
        })

    if sys_prompt:
        data['messages'].append(
            {
                "role": 'system',
                "text": sys_prompt
            }
        )
    with open(IAM_TOKEN, 'r') as f:
        file_data = json.load(f)
        iam_token = file_data["access_token"]
        headers = {
            'Authorization': f'Bearer {iam_token}',
            'Content-Type': 'application/json'
        }
    try:
        return True, len(requests.post(url=url, headers=headers, json=data).json()['tokens'])
    except Exception as e:
        logging.error(f'Error occured in gpt tokenizer')
        return False, None


# Отправляем промт модели.
def gpt(user_prompt, sys_prompt=None):
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    with open(FOLDER_ID) as file:
        data = {
            "modelUri": f"gpt://{file.read()}/yandexgpt/latest",  # модель для генерации текста
            "completionOptions": {
                "stream": False,  # потоковая передача частично сгенерированного текста выключена
                "temperature": 0.3,  # чем выше значение этого параметра, тем более креативными будут ответы модели (0-1)
                "maxTokens": "100"  # максимальное число сгенерированных токенов
            },
            "messages": [
                {
                    "role": "system",
                    "text": sys_prompt
                }
            ]
        }

    for i in user_prompt:
        data['messages'].append(i)
    with open(IAM_TOKEN, 'r') as f:
        file_data = json.load(f)
        iam_token = file_data["access_token"]
        headers = {
            'Authorization': f'Bearer {iam_token}',
            'Content-Type': 'application/json'}
    response = requests.post(url=url, headers=headers, json=data)
    print(response)
    if response.status_code < 200 or response.status_code >= 300:
        return False, f'Error code {response.status_code}'
    try:
        full_response = response.json()
    except:
        return False, f'Error receiving json file'
    if 'error' in full_response or 'result' not in full_response:
        return False, full_response
    result = full_response["result"]["alternatives"][0]["message"]["text"]
    if not result:
        return True, f'Объяснение закончено'
    return True, result


# Проверяем и создаем, если это необходимо, IEM ток