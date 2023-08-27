import time
import csv
import json
import random
import openai

from flask import Flask, request
from difflib import Differ


api = Flask(__name__)


@api.route('/save_data', methods=['POST'])
def save_and_respond():
    data = request.json
    # f = open('messages.csv', 'a', newline='')
    # writer = csv.writer(f)

    # writer.writerow(['user', data['message'], time.time()])
    correction, chatbot_message = get_response(data['message'])
    correction, formatting = correct_user_message(data['message'], correction)
    # writer.writerow(['chatbot', chatbot_message, time.time()])
    # f.close()

    return {
        "message": chatbot_message,
        "correction": correction,
        "format": formatting
    }

@api.route('/set_config', methods=['POST'])
def save_config():
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(request.json, f, ensure_ascii=False, indent=4)
    return {"message": "config saved"}

@api.route('/init_conv', methods=['POST'])
def init_conversation():
    # meta_prompt = (
    #     "You're a language learning buddy and you're helping people who want to learn "
    #     f"{request.json['language'].capitalize()} by chatting with them and correcting their errors. "
    #     # "Ask questions and respond in a natural manner, but be succinct. "
    #     "Respond to every message in the following format:\n"
    #     "[the user's message corrected]\n"
    #     "---\n"
    #     "[the actual response]"
    # )
    meta_prompt = (
        "You're a pattern-following language learning buddy and you're helping people who "
        "want to learn a language by chatting with them and correcting their errors. "
        "Ask questions and respond in a natural manner, so that the conversation runs smoothly, "
        "but don't be too verbose. Respond to every message in the following format:\n"
        "[the user's message corrected]\n"
        "---\n"
        "[the actual response]"
    )
    chat_history = [
        {'role': 'system', 'content': meta_prompt},
        {"role": "system", "name":"example_user", "content": "Ciao, come stai?"},
        {"role": "system", "name": "example_assistant", "content": "Ciao, come stai?\n---\nCiao! Sto bene, grazie! E tu?"},
        {"role": "system", "name":"example_user", "content": "Anch'io sto bene, grazie. Cosa ha fatto di interessante ogg?"},
        {"role": "system", "name": "example_assistant", "content": "Anch'io sto bene, grazie. Cosa hai fatto di interessante oggi?\n---\nMi fa piacere sapere che stai bene! Oggi ho studiato un po' di italiano e ho fatto una passeggiata nel parco. E tu?"},
        {"role": "system", "name":"example_user", "content": "Ho disegnato, schiacchiato una pisolina e programmato un'po. E poi ho guardato il film Scream. L'hai visto?"},
        {"role": "system", "name": "example_assistant", "content": "Ho disegnato, schiacciato un pisolino e programmato un po'. E poi ho guardato il film Scream. L'hai visto?\n---\nWow, hai fatto un po' di cose interessanti oggi! Sì, ho visto il film Scream. È un classico dell'horror. Ti è piaciuto?"},
    ]
    with open('chat_history.json', 'w', encoding='utf-8') as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=4)
    return {"message": "conversation initialized"}


def correct_user_message(user_txt, correct_txt):
    difference = Differ().compare(
        user_txt.split(),
        correct_txt.split()
    )

    text, formatting = [], []
    for word in difference:
        if word[0] != '?':
            text.append(word[2:])
            formatting.append(word[0])

    start = 0
    text_concat, formatting_concat = [], []
    formatting.append('end')
    for i in range(1, len(formatting) + 1):
        if len(set(formatting[start:i])) != 1:
            text_concat.append(' '.join(text[start:(i-1)]))
            formatting_concat.append(formatting[start])
            start = i-1

    return text_concat, formatting_concat


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
        correction = user_message
        chatbot_message = chatbot_response['content']

    return correction, chatbot_message
