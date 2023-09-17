import React from 'react';
import './FeedbackPanel.css';

function FeedbackPanel({ corrections, formattings }) {
  function renderFormattedFeedback(txt, formattings, i) {
    return (
      <div className="feedback-block" key={`cor-div-${i}`}>
        <p key={`cor-p-${i}`}>
          {txt.map((word, j) =>  (
            <>
              <span key={`word-${i}-${j}`} className={formattings[i][j]}>
                {word}
              </span>
              {' '}
            </>
          ))}
        </p>
      </div>
    );
  }

  return (
    <div className="feedback-panel">
          {corrections.map((txt, i) => renderFormattedFeedback(txt, formattings, i))}
    </div>
  );
}

export default FeedbackPanel;
