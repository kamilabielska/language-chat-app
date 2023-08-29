import { useState, useEffect } from 'react'
import axios from "axios";
import './App.css';


function App() {

  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState([]);

  const [corrections, setCorrections] = useState([]);
  const [formattings, setFormattings] = useState([]);

  const [showPopup, setShowPopup] = useState(true);
  const [apiKey, setApiKey] = useState('');
  const [language, setLanguage] = useState('');

  const [isLoading, setIsLoading] = useState(false);

  const handleApiKeyChange = (event) => {
    setApiKey(event.target.value);
  };

  const handleLangChange = (event) => {
    setLanguage(event.target.value);
  };

  const handleConfigSubmit = () => {
    axios.post('/set_config', { api_key: apiKey, language: language })
      .then(response => {
          console.log(response.data.message);
      })
      .catch(error => {
        console.error(error);
      });
    axios.post('/init_conv', { language: language })
      .then(response => {
          console.log(response.data.message);
      })
      .catch(error => {
        console.error(error);
      });
    if (apiKey.trim() !== '') {
      setShowPopup(false);
    }
  };

  const handleInputChange = (event) => {
	  setInputText(event.target.value);
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      handleSave();
    }
  };
  
  const handleSave = () => {
  	setMessages(messages => [...messages, { text: inputText, sender: "user" }]);
    setIsLoading(true);
  	axios.post('/save_data', { message: inputText })
  	  .then(response => {
          console.log(response.data.message);
          setInputText('');
          setMessages(messages => [...messages, { text: response.data.message, sender: "chatbot" }]);
          setCorrections(corrections => [...corrections, response.data.correction]);
          setFormattings(formattings => [...formattings, response.data.format]);
      })
  	  .catch(error => {
  	    console.error(error);
      })
      .finally(() => {
          setIsLoading(false);
      });
  };

  useEffect(() => {
    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: 'smooth',
    });
  }, [messages]);

  function renderFormattedFeedback(txt, formattings, i) {
    return (
      <div className="feedback" key={`cor-div-${i}`}>
        <p key={`cor-p-${i}`}>
          {txt.map((word, j) => (
            formattings[i][j] === " " ? (
              <>
              <span key={`word-${i}-${j}`}>{word}</span>
              {' '}
              </>
            ) : (
              <>
              <span
                key={`word-${i}-${j}`}
                className={formattings[i][j] === "+" ? "correction" : "error"}
              >
                {word}
              </span>
              {' '}
              </>
            )
          ))}
        </p>
      </div>
    );
  }

  return (
    <div className="app">
      <div>
        {showPopup && (
          <div className="popup-background">
            <div className="popup">
              <div className="config-input">
                <label for="api-key">OpenAI api key:</label>
                <input
                  id="api-key"
                  type="text"
                  value={apiKey}
                  onChange={handleApiKeyChange}
                  placeholder="xx-xxxxxxxxxxxx"
                />
              </div>
              <div className="config-input">
                <label for="lang">Language:</label>
                <input
                  id="lang"
                  type="text"
                  value={language}
                  onChange={handleLangChange}
                  placeholder="Italian, German, English..."
                />
              </div>
              <button className="submit-button" onClick={handleConfigSubmit}>
                submit
              </button>
            </div>
          </div>
        )}
      </div>
      <div className={`main-container ${showPopup ? 'blurred' : ''}`}>
    		<div className="chat-panel">
    		  <div className="chat">
    			  {messages.map((message, index) => (
              <div
                key={index}
                className={message.sender === "user" ? "user-message" : "chatbot-message"}
              >
                <p>{message.text}</p>
              </div>
            ))}
            {isLoading && (
               <div className="loading-animation">
                  <div className="dot dot1"></div>
                  <div className="dot dot2"></div>
                  <div className="dot dot3"></div>
              </div>
            )}
    		  </div>
    		  <div className="send-message-box">
                <textarea
                  className="input-field"
                  placeholder="Type your message here..."
                  rows="3"
                  wrap="soft"
                  value={inputText}
                  onChange={handleInputChange}
                  onKeyPress={handleKeyPress}
                />
                <button className="send-button" onClick={handleSave}>
                  send
                </button>
    			</div>
    		</div>
    		<div className="feedback-panel">
    		  {corrections.map((txt, i) => renderFormattedFeedback(txt, formattings, i))}
    		</div>
      </div>
    </div>
  );
}

export default App;
