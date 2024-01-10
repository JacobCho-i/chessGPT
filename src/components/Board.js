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

    let [pawn, setPawn] = useState('');

    
    function move(tile) {
        if (tile === pawn) {
            setPawn('');
            return;
        }
        setPawn(tile);
    }

    function getPawn(col, row) {
        return board[8-row][col];
    }

    function getImage(pawn_id) {
        console.log(pawn_id)
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

    return(
        <div className="bg-blue-400 px-2 py-2">
            {rows.map(row => (
                <div key={'row-' + row} className="flex"> {
                cols.map(col => (
                    ((pawn == '' + row + col) ? // selected tile
                        <button key={'' + row + col} onClick={() => move('' + row + col)} className="bg-yellow-500 py-12 px-12"> {
                            getImage(getPawn(col, row))
                        } </button> 
                    : (row % 2 === 0 // not selected tile
                        ? ((col % 2 === 0) // odd columns
                        ? <button key={'' + row + col} onClick={() => move('' + row + col)} className="bg-blue-400 hover:bg-blue-700 py-12 px-12"> {
                            getImage(getPawn(col, row))
                        } </button> 
                        : <button key={'' + row + col} onClick={() => move('' + row + col)} className="bg-white hover:bg-gray-400 py-12 px-12"> {
                            getImage(getPawn(col, row))
                        } </button>
                        ) 
                        : ((col % 2 === 1) // even columns
                        ? <button key={'' + row + col} onClick={() => move('' + row + col)} className="bg-blue-400 hover:bg-blue-700 py-12 px-12"> {
                            getImage(getPawn(col, row))
                        } </button> 
                        : <button key={'' + row + col} onClick={() => move('' + row + col)} className="bg-white hover:bg-gray-400 py-12 px-12"> {
                            getImage(getPawn(col, row))
                        } </button>
                    ))))
                    )
                }
                </div>
            ))}
        </div>
    );
}

export default Board;