import { useState, useEffect } from 'react'
import axios from 'axios';
import './App.css';
import FeedbackPanel from './components/FeedbackPanel/FeedbackPanel';
import Popup from './components/Popup/Popup';
import ChatPanel from './components/ChatPanel/ChatPanel';

function App() {

  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState([]);

  const [corrections, setCorrections] = useState([]);
  const [formattings, setFormattings] = useState([]);

  const [showPopup, setShowPopup] = useState(true);
  const [apiKey, setApiKey] = useState('');

  const [isLoading, setIsLoading] = useState(false);

  const handleApiKeySubmit = (event) => {
    setApiKey(event.target.value);
  };

  const handleConfigSubmit = () => {
    axios.post('/set_config', { api_key: apiKey })
      .then(response => {
        console.log(response.data.message);
      })
      .catch(error => {
        console.error(error);
      });
    axios.post('/init_conv')
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
    const newMessage = inputText;
    setInputText('');
  	setMessages(messages => [...messages, { text: newMessage, sender: 'user' }]);
    setIsLoading(true);
  	axios.post('/save_data', { message: newMessage })
  	  .then(response => {
        console.log(response.data.message);
        setMessages(messages => [...messages, { text: response.data.message, sender: 'chatbot' }]);
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

  useEffect(() => {
    document.title = 'language chat app';
  }, []);

  return (
    <div className="app">
      {showPopup && <Popup
        apiKey={apiKey}
        onApiKeySubmit={handleApiKeySubmit}
        onConfigSubmit={handleConfigSubmit}
        />}
      <div className={`main-container ${showPopup ? 'blurred' : ''}`}>
        <ChatPanel
          messages={messages}
          inputText={inputText}
          isLoading={isLoading}
          onInputChange={handleInputChange}
          onKeyPress={handleKeyPress}
          onSave={handleSave}
        />
        <FeedbackPanel corrections={corrections} formattings={formattings} />
      </div>
    </div>
  );
}

export default App;
