import json
import shutil
import random

from flask import Flask, request
from chat import get_response, correct_user_message


api = Flask(__name__)


@api.route('/set_config', methods=['POST'])
def save_config():
    """
    Save configuration data to a JSON file.

    This route handles HTTP POST requests to save configuration data received in JSON format
    to a 'config.json' file. The configuration data is expected to be in the request body.

    Returns
    -------
    dict
        A dictionary containing a success message indicating that the configuration data
        has been saved.
    """
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(request.json, f, ensure_ascii=False, indent=4)
    return {'message': 'config saved'}


@api.route('/init_conv', methods=['POST'])
def init_conversation():
    """
    Initialize a conversation by copying an initial chat history.

    This route handles HTTP POST requests to initialize a conversation by copying
    an initial chat history file ('chat_init.json') to the current chat history file
    ('chat_history.json'). The copied chat history serves as the starting point for
    the conversation as it contains a system message and some examples that the chatbot
    should follow.

    Returns
    -------
    dict
        A dictionary containing a success message indicating that the conversation
        has been initialized.
    """
    names = [
        "James", "Ethan", "Liam", "Benjamin", "Noah", "Alexander", "Mason", "Caleb",
        "Emma", "Olivia", "Ava", "Sophia", "Isabella", "Mia", "Emily", "Abigail",
        "Taylor", "Jordan", "Alex", "Casey", "Jamie", "Morgan", "Cameron", "Riley"
    ]
    adjectives = [
        "kind", "empathetic", "honest", "optimistic", "humble", "diligent", "cheery",
        "enthusiastic", "sincere", "open-minded", "thoughtful", "reserved", "practical",
        "cautious", "independent", "skeptical", "detached", "pragmatic", "observant",
        "rational", "analytical", "nonchalant", "quirky", "chill", "tech-savvy", "trendy",
        "ambitious", "spirited", "witty", "playful", "engaging", "expressive", "articulate",
        "shy", "bold", "self-assured"
    ]
    with open('chat_init.json', 'r', encoding='utf-8') as init:
        chat_init = json.load(init)
        
    personality = random.choices(adjectives, k=2)
    chat_init[0]['content'] = chat_init[0]['content'].format(
        name=random.choice(names),
        adj1=personality[0],
        adj2=personality[1]
    )
    
    with open('chat_history.json', 'w', encoding='utf-8') as conv:
        json.dump(chat_init, conv, ensure_ascii=False, indent=4)
    # shutil.copyfile('chat_init.json', 'chat_history.json')
    return {'message': 'conversation initialized'}


@api.route('/save_data', methods=['POST', 'GET'])
def save_and_respond():
    """
    Process user input, generate responses, and provide correction information.

    This route handles HTTP POST and GET requests to process user input and provide responses.
    It expects a JSON object in the request body containing a user message ('message'). The
    route then generates a response using the 'get_response' function and provides correction
    information using the 'correct_user_message' function.

    Returns
    -------
    dict
        A dictionary containing the following elements:
        - 'message': The chatbot's response to the user's message.
        - 'correction': A list of corrected text segments (if available), or an error message.
        - 'format': A list of formatting indicators for each text segment (if available), or
          'no-feedback' if no correction was provided.

    """
    data = request.json
    correction, chatbot_message = get_response(data['message'])
    if correction is None:
        correction, formatting = ['Error: no correction provided'], ['no-feedback']
    else:
        correction, formatting = correct_user_message(data['message'], correction)

    return {
        'message': chatbot_message,
        'correction': correction,
        'format': formatting
    }
