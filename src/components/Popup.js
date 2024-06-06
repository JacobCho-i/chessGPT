import React from 'react';
import './Popup.css'; 

const Popup = ({ onClose, win }) => {
  return (
    <div className="popup-overlay">
      <div className="popup-content">
        {win ? 
        <h2>You win!</h2>
        :
        <h2>You lost!</h2>
        }
        
        <button onClick={onClose}>Confirm</button>
      </div>
    </div>
  );
};

export default Popup;
