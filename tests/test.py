import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../server')))

from GPT_move import *

# call askGPT function and return true if this does not throw error
def testAskGPT():
    client = OpenAI()
    b = board()
    try:
        print(ask_gpt(client, "", b))
        return True
    except:
        return False

# make a valid move in the board and check if the validity is true 
def testValidMove():
    client = OpenAI()
    b = board()
    last_move = {'icon' : '.', 'distance' : 0, 'row' : 0, 'col' : 0}
    return legal_move(b, "W", 0, 1, 2, 2, last_move)

# make an invalid move in the board and check if the validity is false
def testInvalidMove():
    client = OpenAI()
    b = board()
    last_move = {'icon' : '.', 'distance' : 0, 'row' : 0, 'col' : 0}
    return legal_move(b, "W", 0, 1, 2, 3, last_move)

# makes some several move and check each time if the visual board is in the correct format
def testVisualBoard():
    client = OpenAI()
    b = board()
    last_move = {'icon' : '.', 'distance' : 0, 'row' : 0, 'col' : 0}
    b.board[0][1].move_piece(2, 2, last_move)
    print("testVisualBoard: ")
    print("(0, 1) to (2, 2)")
    b.print_board()
    print("(1, 4) to (3, 4)")
    b.board[1][4].move_piece(3, 4, last_move)
    b.print_board()

# makes some several move and check each time if the response has every required fields
def testGPTResponse():
    client = OpenAI()
    b = board()
    last_move = {'icon' : '.', 'distance' : 0, 'row' : 0, 'col' : 0}
    print("testGPTResponse: ")
    print(check_valid(client, b, (0, 1), (2, 2), last_move))

# take out black king and check if the result is white wins
def testWin():
    client = OpenAI()
    b = board()
    last_move = {'icon' : '.', 'distance' : 0, 'row' : 0, 'col' : 0}
    b.remove_piece((7, 4))
    return king_removed(b, "B")

# take out white king and check if the result is black wins
def testLose():
    client = OpenAI()
    b = board()
    last_move = {'icon' : '.', 'distance' : 0, 'row' : 0, 'col' : 0}
    b.remove_piece((0, 4))
    return king_removed(b, "W")

# add more tests here..

if __name__ == '__main__':
    print("ask_gpt test: ", testAskGPT())
    print("valid_move test: ", testValidMove())
    print("invalid_move test: ", testInvalidMove())
    testVisualBoard()
    testGPTResponse()
    print("Win test: ", testWin())
    print("Lose test: ", testLose())

