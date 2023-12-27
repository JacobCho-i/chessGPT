import React, { useEffect, useState } from 'react';

function Board() {
    const rows = [0, 1, 2, 3, 4, 5, 6, 7];
    const cols = [0, 1, 2, 3, 4, 5, 6, 7];
    return(
        <div className="bg-blue-400 px-2 py-2">
            {rows.map(row => (
                <div key={'row-' + row} className="flex"> {
                cols.map(col => (
                    row % 2 === 0
                    ? ((col % 2 === 0) 
                    ? <button key={row + ',' +col} className="bg-blue-400 hover:bg-blue-700 text-white font-bold py-12 px-12"/> 
                    : <button key={row + ',' +col} className="bg-white hover:bg-gray-400 text-white font-bold py-12 px-12"/>) 
                    : ((col % 2 === 1) 
                    ? <button key={row + ',' +col} className="bg-blue-400 hover:bg-blue-700 text-white font-bold py-12 px-12"/> 
                    : <button key={row + ',' +col} className="bg-white hover:bg-gray-400 text-white font-bold py-12 px-12"/>)
                ))
                } 
                </div>
            ))}
        </div>
    );
}

export default Board;