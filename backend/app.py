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
	f = open('messages.csv', 'a', newline='')
	writer = csv.writer(f)

	writer.writerow(['user', data['message'], time.time()])
	correction, chatbot_message = get_response()
	correction, formatting = correct_user_message(data['message'], correction)
	writer.writerow(['chatbot', chatbot_message, time.time()])
	f.close()

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


def get_response():
	# openai.api_key = api_key
	# meta_prompt = (
	#     "You're a human language learning buddy and you're helping people who " +
	#     "want to learn Italian by chatting with them and correcting their errors. " +
	#     "Ask questions and respond in a natural manner, but be succinct. " +
	#     "Respond to every message in the following format:\n" +
	#     "[the user's message corrected]\n" +
	#     "---\n" +
	#     "[the actual response]"
	# )
	# chat_history = [
	#     {'role': 'system', 'content': meta_prompt},
	#     {'role': 'user', 'content': 'ciao, come vai?'},
	#     {'role': 'assistant', 'content': 'ciao, come va?\n---\nCiao, va tutto bene, grazie. È tu, come stai?'},
	#     {'role': 'user', 'content': 'tutto a posto, grazie mille. di che cosa vuoi parlare?'}
	# ]
	# chat = openai.ChatCompletion.create(
	#     model='gpt-3.5-turbo',
	#     messages=chat_history
	# )
	# chat_history.append(dict(chat['choices'][0]['message']))
	response = "tutto a posto, grazie mille. Di cosa vuoi parlare?\n---\nMi fa piacere sapere che tutto va bene. Possiamo parlare di qualsiasi argomento che ti interessa. Hai qualche preferenza?"
	correction, chatbot_message = response.split('\n---\n')
	return correction, chatbot_message
