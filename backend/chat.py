import json
import openai

from difflib import Differ


def get_response(user_message):
    with open('config.json', 'r', encoding='utf-8') as conf, \
         open('chat_history.json', 'r', encoding='utf-8') as conv:
        config = json.load(conf)
        chat_history = json.load(conv)

    openai.api_key = config['api_key']

    chat_history.append({'role': 'user', 'content': user_message})
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-0613',
        temperature=0.7,
        messages=list(chat_history)
    )
    chatbot_response = dict(response['choices'][0]['message'])
    chat_history.append(chatbot_response)

    with open('chat_history.json', 'w', encoding='utf-8') as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=4)

    if '\n---\n' in chatbot_response['content']:
        correction, chatbot_message = chatbot_response['content'].split('\n---\n')
    else:
        correction = None
        chatbot_message = chatbot_response['content']

    return correction, chatbot_message


def correct_user_message(user_txt, correct_txt):
    difference = Differ().compare(user_txt.split(), correct_txt.split())
    format_type = {' ': 'normal', '-': 'error', '+': 'correction'}

    text, formatting = [], []
    for word in difference:
        if word[0] != '?':
            text.append(word[2:])
            formatting.append(format_type[word[0]])

    start = 0
    text_concat, formatting_concat = [], []
    formatting.append('end')
    for i in range(1, len(formatting) + 1):
        if len(set(formatting[start:i])) != 1:
            text_concat.append(' '.join(text[start:(i-1)]))
            formatting_concat.append(formatting[start])
            start = i - 1

    return text_concat, formatting_concat
