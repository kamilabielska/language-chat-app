# language chat app
Reasons for creating this app were threefold:
1. I wanted to create my first web app with React and Flask
2. I wanted to learn how to work with (Chat)GPT: I integrated it into the app (API) and tried using it as a coding assistant (OpenAI web client)
3. I wanted to make the language-learning conversation with ChatGPT smoother by displaying the errors in a visual manner and not having to paste the meta prompt every time

So maybe the reason was onefold: *I wanted to*.

# running the app
You need to have NodeJS installed. Create a virtual environment (called venv) in the `backend` folder and install dependencies from the `requirements.txt` file.

Then cd to the app folder and run
```
npm run start-backend
```
to start the Flask backend. After that, run
```
npm start
```
to start React frontend.

# demo
![language chat app demo](https://github.com/kamilabielska/language_chat_app/blob/master/lang_chat_app_demo.gif?raw=true)
