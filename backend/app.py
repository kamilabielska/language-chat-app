import json
import shutil

from flask import Flask, request
from chat import get_response, correct_user_message


api = Flask(__name__)


@api.route('/set_config', methods=['POST'])
def save_config():
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(request.json, f, ensure_ascii=False, indent=4)
    return {'message': 'config saved'}


@api.route('/init_conv', methods=['POST'])
def init_conversation():
    shutil.copyfile('chat_init.json', 'chat_history.json')
    return {'message': 'conversation initialized'}


@api.route('/save_data', methods=['POST', 'GET'])
def save_and_respond():
    data = request.json
    correction, chatbot_message = get_response(data['message'])
    correction, formatting = correct_user_message(data['message'], correction)

    return {
        'message': chatbot_message,
        'correction': correction,
        'format': formatting
    }
