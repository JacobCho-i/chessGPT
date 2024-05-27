import React from 'react';
import './Popup.css'; 

const Popup = ({ onClose }) => {
  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <h2>You win!</h2>
        <button onClick={onClose}>Confirm</button>
      </div>
    </div>
  );
};

export default Popup;
