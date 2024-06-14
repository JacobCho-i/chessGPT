import React, { useEffect, useState } from 'react';
import Board from './components/Board';
import Navbar from './components/NavBar';
import Footer from './components/Footer';
import Popup from "./components/Popup"
import './App.css';
import Spinner from './components/Spinner';

  console.log("hello");
  let messages = [];

  let knockedWhitePawns = ['wp', 'wp', 'wr'];
  let knockedBlackPawns = ['bp', 'bk', 'bb']; 

  function App() {
    
    const [data, setData] = useState('');
    const [status, setStatus] = useState('');
    const [champ, setChamp] = useState('');
    const [msg, setMsg] = useState('');
    const [isPopupVisible, setPopupVisible] = useState(0);
    const [knockedWhite, setKnockedWhite] = useState([]);
    const [knockedBlack, setknockedBlack] = useState([]);
    const [refreshKey, setRefreshKey] = useState(0);
    const [responseState, setResponseState] = useState([]);

    const updateBoardState = (newState) => {
      setResponseState(newState);
    };

    const updatePopupState = (newState) => {
      setPopupVisible(newState);
    };

    const updateKnockedBlackState = (newState) => {
      setknockedBlack(newState);
    };

    const updateRefresh = (newState) => {
      setRefreshKey(newState)
    };

    const updateKnockedWhiteState = (newState) => {
      setKnockedWhite(newState);
    };
    const showPopup = () => {
      setPopupVisible(true);
    };
  
    const closePopup = () => {
      setPopupVisible(false);
      fetch("http://localhost:5000/restart_game", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify('aaa'),
      });
      setResponseState([]);
      setRefreshKey(1);
    };

    useEffect(() => {
      fetch('http://localhost:5000/messages')
        .then(response => response.json())
        .then(data => {
          messages = data.data
        });
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

    function getImage(pawn_id) {
      switch(pawn_id) {
          case '.':
              break;
          case 'wp':
              return <img src="/w_peasant.png"></img>
          case 'wr':
              return <img src="/w_rook.png"></img>
          case 'wn':
              return <img src="/w_knight.png"></img>
          case 'wb':
              return <img src="/w_bishop.png"></img>
          case 'wq':
              return <img src="/w_queen.png"></img>
          case 'wk':
              return <img src="/w_king.png"></img>
          case 'bp':
              return <img src="/b_peasant.png"></img>
          case 'br':
              return <img src="/b_rook.png"></img>
          case 'bn':
              return <img src="/b_knight.png"></img>
          case 'bb':
              return <img src="/b_bishop.png"></img>
          case 'bq':
              return <img src="/b_queen.png"></img>
          case 'bk':
              return <img src="/b_king.png"></img>
      }
  }

  useEffect(() => {
    const handlePageRefresh = () => {
      console.log('Page refreshed!');
      fetch("http://localhost:5000/restart_game", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify('aaa'),
      });
    };

    handlePageRefresh();

    return () => {
    };
  }, []);

    return (
      <div className="flex flex-col min-h-screen">
        <Navbar/>
        <div className="flex flex-col bg-green-100 flex-grow">
          <div className="flex justify-between items-start h-[100px]">
            <div>
            </div>
            <div className='mx-16 max-h-[300px] overflow-y-auto w-[300px]'>
              <p class='kanit-regular'>Message from ChatGPT: </p>
              <ul class='kanit-small'>
                {responseState.map((message, index) => (
                  <li key={index}>{message}</li>
                ))}
              </ul>
            </div>
          </div>
          <div className="flex justify-center space-x-20">
            <div className='top-0 justify-center'>
              <div class="kanit-small" className='text-center'>
                ChatGPT    
              </div>
              {knockedBlack.map(pawn => ((
                <div className='mb-[-50px]'>
                  {getImage(pawn)}
                </div>
              )))}
            </div>
            <Board responseState={responseState} updateResponseState={updateBoardState} updatePopupState={updatePopupState} black={updateKnockedBlackState} white={updateKnockedWhiteState} 
            refreshKey={refreshKey} setRefresh={updateRefresh}/>
            <div> 
              {isPopupVisible == 1 && <Popup onClose={closePopup} win={true} />}
              {isPopupVisible == 2 && <Popup onClose={closePopup} win={false} />}
            </div>
            <div className='top-0'>
              <div class="kanit-small"  className='text-center'>
                You
              </div>
              {knockedWhite.map(pawn => ((
                  <div className='mb-[-50px]'>
                  {getImage(pawn)}
                </div>
              )))}
            </div>
          </div>
          <div className="flex justify-between items-start h-[100px]"/>
        </div>
        <Footer/>
      </div>
    );

    
  }

  export default App;
