import requests


def get_info_of_word(word):
    url = 'https://api.dictionaryapi.dev/api/v2/entries/en/' + word.strip()
    response = requests.get(url)
    if response.status_code < 200 or response.status_code >= 300:
        return None, None, None, f'Error code {response.status_code}'
    try:
        info = response.json()[0]
    except:
        return None, None, None, f'Error receiving json file'
    try:
        definition = info["meanings"][0]['definitions'][0]['definition']
    except:
        definition = None

    try:
        example = info["meanings"][0]['definitions'][0]['example']
    except:
        example = None

    try:
        audio_url = info['phonetics'][0]['audio']
        audio = requests.get(audio_url)
        if audio.status_code < 200 or audio.status_code >= 300:
            return definition, example, None, None
        audio = audio.content
    except:
        audio = None

    return definition, example, audio, None


def get_translation(word):
    api_key = 'dict.1.1.20240521T085550Z.901d788f40379d0a.92dcfb820583245007a6c2651a64129c75c4bb50'
    url = f'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={api_key}&lang=en-ru&text=' + word
    response = requests.get(url)

    if response.status_code < 200 or response.status_code >= 300:
        return None, f'Error code {response.status_code}'

    response = response.json()
    trans = []
    try:
        for tr in response['def'][0]['tr']:
            trans.append(tr['text'])
    except:
        trans = None

    '''examples = []
    try:
        for tr in response['def'][0]['tr']:
            example = tr.get('ex')
            if example != None:
                for ex in example:
                    examples.append(ex['text'])
    except:
        examples = None'''
    return trans, None


def translate(message, state='show_word'):

    translation, error = get_translation(message)
    if error:
        return 'Error', 'Error'
    definition, example, audio, error = get_info_of_word(message)
    resp = ''
    if state=='show_word':
        resp = f'📌 Слово {message} 📌\n'

    if not translation and not definition and not example and not audio:

        return False, False

    if translation:
        trans = ", ".join(translation)
        resp += f'*Meaning*: {trans}\n'

    if definition:
        resp += f'*Definition*: {definition}\n'

    if example:
        resp += f'*Example*: {example}\n'

    if audio:
        return resp, audio
    return resp, False