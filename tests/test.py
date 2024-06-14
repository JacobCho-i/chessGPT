from GPT_move import *

# call askGPT function and return true if this does not throw error
def testAskGPT():
    client = OpenAI()
    b = board()

# make a valid move in the board and check if the validity is true 
def testValidMove():
    client = OpenAI()
    b = board()

# make an invalid move in the board and check if the validity is false
def testInvalidMove():
    client = OpenAI()
    b = board()

# makes some several move and check each time if the visual board is in the correct format
def testVisualBoard():
    client = OpenAI()
    b = board()

# makes some several move and check each time if the response has every required fields
def testGPTResponse():
    client = OpenAI()
    b = board()

# take out black king and check if the result is white wins
def testWin():
    client = OpenAI()
    b = board()

# take out white king and check if the result is black wins
def testLose():
    client = OpenAI()
    b = board()

# add more tests here..

if __name__ == '__main__':
    testAskGPT()
    testValidMove()
    testInvalidMove()
    testVisualBoard()
    testGPTResponse()
    testWin()
    testLose()

