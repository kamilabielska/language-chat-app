import React from 'react';
import './Popup.css';

function Popup({ apiKey, onApiKeySubmit, onConfigSubmit }) {
  return (
    <div className="popup-background">
      <div className="popup">
        <div className="config-input">
          <label for="api-key">OpenAI api key:</label>
          <input
            id="api-key"
            type="text"
            value={apiKey}
            onChange={onApiKeySubmit}
            placeholder="xx-xxxxxxxxxxxx"
          />
        </div>
        <button className="submit-button" onClick={onConfigSubmit}>
          submit
        </button>
      </div>
    </div>
  );
}

export default Popup;
