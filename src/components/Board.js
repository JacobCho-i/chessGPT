import { data } from 'autoprefixer';
import React, { useEffect, useState } from 'react';
import Spinner from './Spinner';
/*
let board = [
    ['wr','wn','wb','wq','wk','wb','wn','wr'],
    ['wp','wp','wp','wp','wp','wp','wp','wp'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['bp','bp','bp','bp','bp','bp','bp','bp'],
    ['br','bn','bb','bq','bk','bb','bn','br']
];
*/

function Board({ responseState, updateResponseState, updatePopupState, black, white, refreshKey, setRefresh}) {
    const rows = [8, 7, 6, 5, 4, 3, 2, 1];
    const alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
    const cols = [0, 1, 2, 3, 4, 5, 6, 7];

    let [board, setBoard] = useState(
        [
            ['br','bn','bb','bq','bk','bb','bn','br'],
            ['bp','bp','bp','bp','bp','bp','bp','bp'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['.','.','.','.','.','.','.','.'],
            ['wp','wp','wp','wp','wp','wp','wp','wp'],
            ['wr','wn','wb','wq','wk','wb','wn','wr']
        ]
    )
    let [pawn, setPawn] = useState('.');
    let [loading, setLoading] = useState(false);
    let [pawnType, setPawnType] = useState('.');
    let [enemy, setEnemy] = useState('b');
    let [legal, setLegal] = useState(false);

    useEffect(() => {
        if (refreshKey === 1) {
            window.location.reload();
            setRefresh(0);
        }
      }, [refreshKey]);

    function showSpinner() {
        document.getElementById('spinner').style.display = 'block';
    }
      
    function hideSpinner() {
        document.getElementById('spinner').style.display = 'none';
    }
      
    
    function select(tile, selectePawn) {
        if (typeof selectePawn === 'undefined' || tile === selectePawn) {
            setPawn('.');
            setPawnType('.');
            return;
        }

        if (selectePawn === '.' || typeof selectePawn === 'string' && selectePawn.length > 0 && selectePawn.substring(0, 1) === enemy) { // selected tile first
            if (pawnType !== '.') {
                move(pawn, tile);
            }
            return;
        }
        
        if (typeof selectePawn === 'string' && selectePawn.length > 0 && selectePawn.substring(0, 1) === enemy) {
            return;
        }

        setPawn(tile);
        setPawnType(selectePawn);
    }

    async function validate(prev, next) {
        let moves = []; 
        const legal = await processMove(prev, next);
        console.log(legal)
        return legal;
    }
    
    async function processMove(prev, next) {
        const dataToSend = {prevMove: prev, nextMove: next};
        setLoading(true);
        const response = await fetch("http://localhost:5000/process_move", {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(dataToSend),
          });
        const data = await response.json();
        console.log(data)
        if (!data.legal) {
            setLoading(false);
            return false;
        }
        setBoard(data.board)
        var responses = [...responseState, "my move is " + data.response];
        updateResponseState(responses)
        if (data.result == "white won") {
            updatePopupState(1);
        }
        if (data.result == "black won") {
            updatePopupState(2);
        }
        black(data.black)
        white(data.white)
        setPawn('.');
        setPawnType('.');
        setLoading(false);
        return data.legal
      }

    async function move(prev, next) {
        const invalid = await validate(prev, next);
        console.log("prev: " + prev + " next: " + next)
        if (!invalid) {
            alert('Invalid move!'); 
            return;
        }
    }

    function getPawn(col, row) {
        return board[8-row][col];
    }

    function getImage(pawn_id) {
        var isprevious = false;
        if (typeof pawn_id === 'string' && pawn_id.length > 2) {
            isprevious = true;
            pawn_id = pawn_id.substring(0,2);
        }
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
                return isprevious ? <img className='opacity-75' src="/b_peasant.png"></img> : <img src="/b_peasant.png"></img>
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

    function getFirstChar(char) {
        if (typeof char === 'string' && pawn.length > 0) {
            return char.substring(0, 1);
        }
    }

    function getTypeofTile(col, row) {
        if (pawn === '.') {
            switch (getFirstChar(getPawn(col, row))) {
                case enemy: // enemy tiles
                case '.': // empty tiles
                    return 1;
                default: // pawn tiles
                    return 2;
            }
        } else {
            switch (getFirstChar(getPawn(col, row))) {
                case enemy: // enemy tiles
                case '.': // empty tiles
                    return 2;
                default: // pawn tiles
                    return 1;
            }
        }
    }
    
    
    function getTile(row, col) {
            if (pawn == '' + row + col) {
                return <button key={'' + row + col} onClick={() => select('' + row + col)} className="bg-yellow-500" style={{height:100, width:100}}> {
                    getImage(getPawn(col, row))
                } </button>;
            } else {

                if ((row % 2 === 0 && col % 2 === 0) || (row % 2 === 1 && col % 2 === 1)) {
                    // green tile
                    switch (getTypeofTile(col, row)) {
                        case 1:
                            return <button key={'' + row + col} style={{height:100, width:100}} className="bg-amber-700 hover:cursor-auto"> {
                                getImage(getPawn(col, row))
                            } </button>; 
                        case 2:
                            return <button key={'' + row + col} onClick={() => select('' + row + col, getPawn(col, row))} style={{height:100, width:100}} className="bg-amber-700 hover:bg-amber-900"> {
                                getImage(getPawn(col, row))
                            } </button>;
                    }
                } else {
                    // white tile
                    switch (getTypeofTile(col, row)) {
                        case 1:
                            return <button key={'' + row + col} style={{height:100, width:100}} className="bg-white hover:cursor-auto"> {
                                getImage(getPawn(col, row))
                            } </button>;
                        case 2:
                            return <button key={'' + row + col} onClick={() => select('' + row + col, getPawn(col, row))} style={{height:100, width:100}} className="bg-white hover:bg-gray-400"> {
                                getImage(getPawn(col, row))
                            } </button>;
                    }
                }
            }
        }


    return(
        <div className="bg-amber-700 px-3 py-3 rounded-md">
            {loading ? <Spinner /> : <></> }
            <div className='flex justify-center'>
            {alpha.map(col => (
                <button key={'' + col} style={{height:30, width:100}} className="bg-amber-700 hover:cursor-auto text-white">{col}</button>
            ))}
            </div>
            {rows.map(row => (
                <div key={'row-' + row} className="flex"> 
                <button key={'' + row + 'f'} style={{height:100, width:30}} className="bg-amber-700 hover:cursor-auto text-white">{row}
                </button>
                    {
                    cols.map(col => ((
                        getTile(row, col)
                        )))
                    }
                <button key={'' + row + 'b'} style={{height:100, width:30}} className="bg-amber-700 hover:cursor-auto text-white">{row}</button>
                </div>
            ))
            }
            <div className='flex justify-center'>
            {alpha.map(col => (
                <button key={'' + col} style={{height:30, width:100}} className="bg-amber-700 hover:cursor-auto text-white">{col}</button>
            ))}
            </div>
        </div>
    );
}

export default Board;