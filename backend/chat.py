import json
import openai

from difflib import Differ


def get_response(user_message):
    """
    Generate a response from a chatbot using OpenAI's GPT-3.5 Turbo model.

    This function takes a user's message as input, adds it to the chat history,
    and retrieves a response from the chatbot model. It also handles the splitting
    of the chatbot's response if it contains a correction.

    Parameters
    ----------
    user_message : str
        The user's message to be included in the conversation.

    Returns
    -------
    tuple
        A tuple containing two elements:
        correction : str or None
            If the chatbot's response contains a correction, this will be the corrected message.
            Otherwise, it will be None.
        chatbot_message : str
            The chatbot's response to the user's message.
    """
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

    with open('chat_history.json', 'w', encoding='utf-8') as conv:
        json.dump(chat_history, conv, ensure_ascii=False, indent=4)

    if '\n---\n' in chatbot_response['content']:
        correction, chatbot_message = chatbot_response['content'].split('\n---\n', 1)
    else:
        correction = None
        chatbot_message = chatbot_response['content']

    return correction, chatbot_message


def correct_user_message(user_txt, correct_txt):
    """
    Compare two texts and generate formatted corrections.

    Parameters
    ----------
    user_txt : str
        The user's input text to be compared for corrections.
    correct_txt : str
        The corrected text to compare against.

    Returns
    -------
    tuple
        A tuple containing two lists:
        text_concat : list of str
            A list of corrected text segments, where corrections are applied.
        formatting_concat : list of str
            A list of formatting indicators for each text segment, where formatting
            types are 'normal', 'error', or 'correction'.

    Notes
    -----
    This function compares two input texts using the difflib.Differ class to find
    the differences between the two texts. It then extracts the corrected segments
    and their associated formatting types ('normal', 'error', or 'correction').
    """
    difference = Differ().compare(user_txt.split(), correct_txt.split())
    format_type = {' ': 'normal', '-': 'error', '+': 'correction'}

    text, formatting = [], []
    for diff in difference:
        if diff[0] in format_type:
            tag, word = format_type[diff[0]], diff[2:]
            if len(formatting) != 0 and tag == formatting[-1]:
                text[-1] += ' ' + word
            else:
                text.append(word)
                formatting.append(tag)

    return text, formatting
