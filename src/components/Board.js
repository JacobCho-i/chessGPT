import React, { useEffect, useState } from 'react';

let board = [
    ['br','bn','bb','bq','bk','bb','bn','br'],
    ['bp','bp','bp','bp','bp','bp','bp','bp'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['.','.','.','.','.','.','.','.'],
    ['wp','wp','wp','wp','wp','wp','wp','wp'],
    ['wr','wn','wb','wq','wk','wb','wn','wr']
];

function Board() {
    const rows = [8, 7, 6, 5, 4, 3, 2, 1];
    const alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
    const cols = [0, 1, 2, 3, 4, 5, 6, 7];

    let [pawn, setPawn] = useState('.');
    let [enemy, setEnemy] = useState('b');

    
    function move(tile, pawn) {
        console.log(pawn);
        if (typeof pawn === 'undefined' || tile === pawn) {
            setPawn('.');
            return;
        }

        if (pawn === '.') {
            return;
        }
        
        if (typeof pawn === 'string' && pawn.length > 0 && pawn.substring(0, 1) === enemy) {
            return;
        }

        setPawn(tile);
    }

    function getPawn(col, row) {
        return board[8-row][col];
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

    function getFirstChar(char) {
        if (typeof char === 'string' && pawn.length > 0) {
            return char.substring(0, 1);
        }
    }
    
    
    function getTile(row, col) {
            if (pawn == '' + row + col) {
                return <button key={'' + row + col} onClick={() => move('' + row + col)} className="bg-yellow-500" style={{height:100, width:100}}> {
                    getImage(getPawn(col, row))
                } </button>;
            } else {
                if (row % 2 === 0) {
                    if (col % 2 === 0) {
                        switch (getFirstChar(getPawn(col, row))) {
                            case enemy: // enemy tiles
                            case '.': // empty tiles
                                return <button key={'' + row + col} onClick={() => move('' + row + col, getPawn(col, row))} style={{height:100, width:100}} className="bg-green-400 hover:cursor-auto"> {
                                    getImage(getPawn(col, row))
                                } </button>; 
                            default: // pawn tiles
                                return <button key={'' + row + col} onClick={() => move('' + row + col, getPawn(col, row))} style={{height:100, width:100}} className="bg-green-400 hover:bg-green-700"> {
                                    getImage(getPawn(col, row))
                                } </button>; 
                        }
                    } else {
                        switch (getFirstChar(getPawn(col, row))) {
                            case enemy: // enemy tiles
                            case '.': // empty tiles
                                return <button key={'' + row + col} onClick={() => move('' + row + col, getPawn(col, row))} style={{height:100, width:100}} className="bg-white hover:cursor-auto"> {
                                    getImage(getPawn(col, row))
                                } </button>;
                            default: // pawn tiles
                                return <button key={'' + row + col} onClick={() => move('' + row + col, getPawn(col, row))} style={{height:100, width:100}} className="bg-white hover:bg-gray-400"> {
                                    getImage(getPawn(col, row))
                                } </button>;
                        }
                    }
                } else {
                    if (col % 2 === 1) {
                        switch (getFirstChar(getPawn(col, row))) {
                            case enemy: // enemy tiles
                            case '.': // empty tiles
                                return <button key={'' + row + col} onClick={() => move('' + row + col, getPawn(col, row))} style={{height:100, width:100}} className="bg-green-400 hover:cursor-auto"> {
                                    getImage(getPawn(col, row))
                                } </button>;
                            default: // pawn tiles
                                return <button key={'' + row + col} onClick={() => move('' + row + col, getPawn(col, row))} style={{height:100, width:100}} className="bg-green-400 hover:bg-green-700"> {
                                    getImage(getPawn(col, row))
                                } </button>;
                        }
                        
                    } else {
                        switch (getFirstChar(getPawn(col, row))) {
                            case enemy: // enemy tiles
                            case '.': // empty tiles
                                return <button key={'' + row + col} onClick={() => move('' + row + col, getPawn(col, row))} style={{height:100, width:100}} className="bg-white hover:cursor-auto"> {
                                    getImage(getPawn(col, row))
                                } </button>;
                            default: // pawn tiles
                                return <button key={'' + row + col} onClick={() => move('' + row + col, getPawn(col, row))} style={{height:100, width:100}} className="bg-white hover:bg-gray-400"> {
                                    getImage(getPawn(col, row))
                                } </button>;
                        }
                        
                }
            }
        }
    }


    return(
        <div className="bg-green-400 px-2 py-2">
            {rows.map(row => (
                <div key={'row-' + row} className="flex"> {
                cols.map(col => (
                    (
                        getTile(row, col)
                    ))
                    )
                }
                </div>
            ))}
        </div>
    );
}

export default Board;