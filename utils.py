from collections import deque
from math import ceil
def get_markdownv2_text(input_text):
    output_text = ''
    for i in input_text:
        if i in ['_', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!', '\\']:
            output_text += "\\" + i
        else:
            output_text += i
    return output_text

# Варварским способом получаем слово из сообщения, которое конструирует функция translate
def get_word(message):
    return message.split()[2]


# Старался сделать как можно более оптимизированно, чтобы слова, которые пользователь обозначил, как те, которые он еще
# хочет повторить, мы брали и перемещали из левого края списка в правый, тем самым, самое раннее слово в списке, после
# того, как пользователь его повторит, автоматически перемещалось в самый правый край списка, делая это слово самым
# поздним. А слово, которое пользователь обозначил как уже выученное мы бы брали и удаляли из левого края.
# вот пример:
# words = ['horse', 'cat', 'cow', 'donkey'] слова раставлены в порядке их добавления(от самих ранних к самым поздним)
# пользователю выдается слово words[0] т.е. 'horse'
# пользователь говорит, что хочет повторить еще это слово в будущем.
# мы берем и перемещаем это слово из левого края в правый, т.е. words = ['cat', 'cow', 'donkey', 'horse'] и мы
# запоминаем слово 'horse' и добавляем его в bound_for_repeating_words, и, если мы на него натыкаемся в будущем, то мы
# знаем, что пользователь повторил все слова.
# А если же пользователь говорит, что он выучил это слово, то мы удаляем его, т.е. words = ['cat', 'cow', 'donkey']
# и потом также берем words[0].
# Так вот, для всех этих манипуляциий лучше всего подходит тип данных deque(), как описано внизу.
def deque_manipulation(array, operation=None):
    array = deque(array)
    if operation == 'stay':
        el = array.popleft()
        array.append(el)
    elif operation == 'remove':
        array.popleft()
    return array

# Удаляем ~ в пользовательском сообщении, так как это может нам подкосить базу данных
def deleting_tildas(text):
    output = ''
    for i in text:
        if i != '~':
            output += i
    return output



from vocab import get_info_of_word, get_translation
def translate(message, state='show_word'):

    #if not is_user_in_words(user_id):
        #add_user_to_words_table(user_id)

    translation, error = get_translation(message)
    definition, example, audio, error = get_info_of_word(message)
    resp = ''
    if state=='show_word':
        resp = f'📌 Слово {message} 📌\n'
    if error != None or (translation == None and definition == None and example == None and audio == None):

        return False, False

    #add_word(user_id, message)
    #print(get_words(user_id))

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


def print_result(seconds, know, dont_know, tests):
    resp = "📊 <b>Твои результаты</b> 📊\n\n"
    resp += f"⌛ С нейросетью ты разговаривал <em>{round(seconds / 60, 1)} минут(ы)</em>\n"
    resp += f"📚 Ты уже знаешь <em>{know} слов(о)</em>\n"
    resp += f"🔎 Тебе еще предстоит выучить <em>{dont_know} слов(о)</em> \n"
    resp += f"✅ Результаты тестов: \n"
    levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
    for i in range(len(levels)):
        resp += f"<b>{levels[i]}: </b>"
        state, current, right = tests[i]
        if state == "None":
            resp += "Не начат\n"
        elif state == "Start":
            resp += f"Вы остановились на {current}-ом(ем) вопросе, из них правильно <em>{right}</em>\n"
        else:
            resp += f"Тест завершен с результатом <em>{right}</em> из 10 \n"
    return resp


def user_words_stat(dont_know, know):
    cnt = 1
    resp = "<b>Новые слова</b>: \n"
    if dont_know == []:
        resp += "Вы еще не переводили новые слова. \n"
    else:
        for i in range(len(dont_know)):
            resp += f"{cnt}. {dont_know[i]}\n"
            cnt += 1

    resp += "\n<b>Слова, которые уже знаешь</b>: \n"
    cnt = 1
    if know == []:
        resp += "Вы еще не отметили выученным никакие слова"
    else:
        for i in range(len(know)):
            resp += f"{cnt}. {know[i]}\n"
            cnt += 1
    return resp