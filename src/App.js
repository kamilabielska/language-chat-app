import { useState } from 'react'
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
          if (apiKey.trim() !== '') {
            setShowPopup(false);
          }
      })
      .catch(error => {
        console.error(error);
      });
  };

  const handleInputChange = (event) => {
	  setInputText(event.target.value);
  };
  
  const handleSave = () => {
  	setMessages(messages => [...messages, { text: inputText, sender: "user" }]);
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
      });
  };

  function renderFormattedFeedback(txt, formattings, i) {
    return (
      <div className="feedback" key={`cor-div-${i}`}>
        <p key={`cor-p-${i}`}>
          {txt.map((word, j) => (
            formattings[i][j] === " " ? (
              <span key={`word-${i}-${j}`}>{word}</span>
            ) : (
              <span
                key={`word-${i}-${j}`}
                className={formattings[i][j] === "+" ? "correction" : "error"}
              >
                {word}
              </span>
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
              <div className="popup-content">
                <input
                  type="text"
                  value={apiKey}
                  onChange={handleApiKeyChange}
                  placeholder="Enter OpenAI key"
                />
                <input
                  type="text"
                  value={language}
                  onChange={handleLangChange}
                  placeholder="Enter language"
                />
                <button onClick={handleConfigSubmit}>submit</button>
              </div>
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
    		  </div>
    		  <div className="send-message-box">
                <textarea
                  className="input-field"
                  placeholder="Type your message here..."
                  rows="3"
                  wrap="soft"
                  value={inputText}
                  onChange={handleInputChange}
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
