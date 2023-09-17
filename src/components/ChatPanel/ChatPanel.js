import React from 'react';
import './ChatPanel.css';

function ChatPanel({ messages, inputText, isLoading, onInputChange, onKeyPress, onSave }) {
  return (
    <div className="chat-panel">
      <div className="chat">
        {messages.map((message, index) => (
          <div key={index} className={`${message.sender}-message`}>
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
          onChange={onInputChange}
          onKeyPress={onKeyPress}
        />
        <button className="send-button" onClick={onSave}>
          send
        </button>
      </div>
    </div>
  );
}

export default ChatPanel;
