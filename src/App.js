  import logo from './logo.svg';
  import './App.css';
  import React, { useEffect, useState } from 'react';

  function App() {

    const [data, setData] = useState('');
    const [status, setStatus] = useState('');
    const [champ, setChamp] = useState('');
    const [champdata, setChampdata] = useState('');

    useEffect(() => {
      fetch('http://localhost:5000/api/data')
        .then(response => response.json())
        .then(data => setData(data.data));
      const dataToSend = { key1: 'value1', key2: 'value2' };
      sendDataToPython(dataToSend);
    }, []);

    function sendDataToPython(data) {
      fetch('http://localhost:5000/process_data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
      .then(response => response.json())
      .then(data => setStatus(data.data))
      .catch(error => console.error('Error:', error));
    }

    function selectChamp(name) {
      setChamp(name);
      const dataToSend = {champion: name};
      fetch('http://localhost:5000/process_champion', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToSend),
      })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error('Error:', error));
    }

    return (
      <div>
        <p>Data from Python: {data}</p>
        <p>input received in Python: {status}</p>
        <p>Pick your champion. Your choice : {champ}</p>
        <button onClick={() => selectChamp("Malzhar")}>Malzhar</button>
        <button onClick={() => selectChamp("Garen")}>Garen</button>
        <button onClick={() => selectChamp("Sylas")}>Sylas</button>
      </div>
    );
  }

  export default App;
