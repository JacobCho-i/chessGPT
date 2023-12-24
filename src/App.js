import logo from './logo.svg';
import './App.css';
import React, { useEffect, useState } from 'react';

function App() {

  const [data, setData] = useState('');

  useEffect(() => {
    fetch('http://localhost:5000/api/data')
      .then(response => response.json())
      .then(data => setData(data.data));
  }, []);

  return (
    <div>
      <p>Data from Python: {data}</p>
    </div>
  );
}

export default App;
