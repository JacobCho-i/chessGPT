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
    let [pawnType, setPawnType] = useState('.');
    let [enemy, setEnemy] = useState('b');

    
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

    function validate(prev, next) {
        //add back end code here to verify the movement
        return true;
    }
    

    function move(prev, next) {
        if (!validate(prev, next)) {
            alert('Invalid move!'); 
            return;
        }
        let temp = board[8-prev.charAt(0)][prev.charAt(1)];
        let nextPawn = board[8-next.charAt(0)][next.charAt(1)];
        if (typeof nextPawn === 'string' && nextPawn.length > 0 && nextPawn.substring(0, 1) === enemy) {
            board[8-next.charAt(0)][next.charAt(1)] = board[8-prev.charAt(0)][prev.charAt(1)];
            board[8-prev.charAt(0)][prev.charAt(1)] = ".";
        }
        else {
            board[8-prev.charAt(0)][prev.charAt(1)] = board[8-next.charAt(0)][next.charAt(1)];
            board[8-next.charAt(0)][next.charAt(1)] = temp;
        }
        setPawn('.');
        setPawnType('.');
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
                            return <button key={'' + row + col} style={{height:100, width:100}} className="bg-green-400 hover:cursor-auto"> {
                                getImage(getPawn(col, row))
                            } </button>; 
                        case 2:
                            return <button key={'' + row + col} onClick={() => select('' + row + col, getPawn(col, row))} style={{height:100, width:100}} className="bg-green-400 hover:bg-green-700"> {
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