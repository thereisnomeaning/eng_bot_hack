import time
import json

HOME_DIR = 'C:/Users/ps/PycharmProjects/hackathon'  # путь к папке с проектом
LOGS = f'{HOME_DIR}/logging.txt'  # файл для логов
DB_FILE = f'{HOME_DIR}/database.db'  # файл для базы данных

IAM_TOKEN = f'{HOME_DIR}/creds/iam_token.txt'  # файл для хранения iam_token
FOLDER_ID = f'{HOME_DIR}/creds/folder_id.txt'  # файл для хранения folder_id
BOT_TOKEN = f'{HOME_DIR}/creds/bot_token.txt'  # файл для хранения bot_token

MAX_MODEL_TOKENS = 200
MAX_USERS = 100
MAX_STT_BLOCKS_PER_PERSON = 4
MAX_GPT_TOKENS_PER_PERSON = 2000
MAX_TTS_TOKENS_PER_PERSON = 2000
MAX_GPT_TOKENS_PER_MESSAGE = 500
MAX_TTS_TOKENS_PER_MESSAGE = 700

SYSTEM_PROMPT = '''Ты дружелюбный англичанин-ассистент. Развивай тему и задавай вопрос в конце. Не пиши много текста. Отвечай только на английском'''

SYSTEM_PROMPT_TRANSLATION = '''Переведи сообщение на русский.'''




class GPT:

    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'


    data = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt/latest",  # модель для генерации текста
        "completionOptions": {
            "stream": False,  # потоковая передача частично сгенерированного текста выключена
            "temperature": 0.3,  # чем выше значение этого параметра, тем более креативными будут ответы модели (0-1)
            "maxTokens": "100"  # максимальное число сгенерированных токенов
        },
        "messages": [
            {
                "role": "system",
                "text": None
            }
        ]
    }


class IEM:
    headers = {"Metadata-Flavor": "Google"}
    metadata_url = 'http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token'
