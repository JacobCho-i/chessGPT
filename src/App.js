import React, { useEffect, useState } from 'react';
import Board from './components/Board';
import Navbar from './components/NavBar';
import Footer from './components/Footer';

  console.log("hello");
  let messages = [];

  function App() {
    
    const [data, setData] = useState('');
    const [status, setStatus] = useState('');
    const [champ, setChamp] = useState('');
    const [msg, setMsg] = useState('');

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
    

    function processMessage(name) {
      console.log(messages)
      setChamp(name);
      const dataToSend = {champion: name};
      //let url = "http://localhost:5000/message" + index;
      fetch("http://localhost:5000/message", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToSend),
      })
      .then(response => response.json())
      .then(data => compareAndAppend(data.data))
      .catch(error => console.error('Error:', error));
      // setIndex(index + 1);
    }

    function compareAndAppend(message) {
      if (msg !== message) {
        messages.push(message);
        console.log(messages)
        setMsg(message)
      }
    }

    return (
      <div className="flex flex-col min-h-screen">
        <Navbar/>
        <div className="flex flex-col flex-grow">
          <div className="flex justify-between items-start h-[100px]">
            <div>
            </div>
            <div className='mx-16 max-h-[300px] overflow-y-auto w-[300px]'>
              <p>Message from ChatGPT: </p>
              <ul>
                {messages.map((message, index) => (
                  <li key={index}>{message}</li>
                ))}
              </ul>
            </div>
          </div>
          <div className="flex justify-center items-center">
            <Board/>
          </div>
          <div className="flex justify-between items-start h-[100px]"/>
        </div>
        <Footer/>
      </div>
    );

    
  }

  export default App;
