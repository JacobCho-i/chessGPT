from flask import Flask, request, jsonify
from flask_cors import CORS
from GPT_move import *

app = Flask(__name__)
CORS(app)
index = 1
client = OpenAI()
b = board()
last_move = {'icon' : '.', 'distance' : 0, 'row' : 0, 'col' : 0}
response = []

@app.route('/messages')
def get_data():
    print("this is response: ")
    print(response)
    return jsonify({'data': response})

@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.json  # Get JSON data sent by the client
    # Process data here...
    print(data)
    return jsonify({'data': 'Data received successfully!'})

@app.route('/process_champion', methods=['POST'])
def process_champion():
    data = request.json  # Get JSON data sent by the client
    # Process data here...
    print(data)
    msg = 'My first move is ' + data['champion'] + '!'
    return jsonify({'data': msg})

@app.route('/process_move', methods=['POST'])    
def process_move():
    data = request.json
    print(type(data['prevMove']))
    prev = str(int(data['prevMove'][0:1]) - 1) + data['prevMove'][1]
    next = str(int(data['nextMove'][0:1]) - 1) + data['nextMove'][1]
    msg = 'My first move is from ' + prev + " " + next + '!'
    prevMove = (int(data['prevMove'][0:1]) - 1, int(data['prevMove'][1]))
    nextMove = (int(data['nextMove'][0:1]) - 1, int(data['nextMove'][1]))
    print(prevMove)
    print(nextMove)
    result = check_valid(client, b, prevMove, nextMove, last_move)
    print(result)
    b.print_board()
    if (result == False):
        print("this move is not legal")
        return jsonify({'legal': False}) 
    print("this move is legal")
    response.append("my move is " + result['response'])
    for i, sublist in enumerate(result['board']):
        for j, string in enumerate(sublist):
            match string:
                case "p":
                    result['board'][i][j] = "bp"
                case "r":
                    result['board'][i][j] = "br"
                case "n":
                    result['board'][i][j] = "bn"
                case "b":
                    result['board'][i][j] = "bb"
                case "k":
                    result['board'][i][j] = "bk"
                case "q":
                    result['board'][i][j] = "bq"
                case "P":
                    result['board'][i][j] = "wp"
                case "R":
                    result['board'][i][j] = "wr"
                case "N":
                    result['board'][i][j] = "wn"
                case "B":
                    result['board'][i][j] = "wb"
                case "K":
                    result['board'][i][j] = "wk"
                case "Q":
                    result['board'][i][j] = "wq"
    print(result['board'])
    print(response)
    for i, string in enumerate(result['disabled_black_pieces']):
        match string:
            case "p":
                result['disabled_black_pieces'][i] = "bp"
            case "r":
                result['disabled_black_pieces'][i] = "br"
            case "n":
                result['disabled_black_pieces'][i] = "bn"
            case "b":
                result['disabled_black_pieces'][i] = "bb"
            case "k":
                result['disabled_black_pieces'][i] = "bk"
            case "q":
                result['disabled_black_pieces'][i] = "bq"
    for i, string in enumerate(result['disabled_white_pieces']):
        match string:
            case "P":
                result['disabled_white_pieces'][i] = "wp"
            case "R":
                result['disabled_white_pieces'][i] = "wr"
            case "N":
                result['disabled_white_pieces'][i] = "wn"
            case "B":
                result['disabled_white_pieces'][i] = "wb"
            case "K":
                result['disabled_white_pieces'][i] = "wk"
            case "Q":
                result['disabled_white_pieces'][i] = "wq"
    return jsonify({'legal': True, 'result': result['result'], 'board': result['board'], 'prev': [result['previous'][0], result['previous'][1]], 'next': [result['next'][0], result['next'][1]], 'response': result['response'], 
                    'white': result['disabled_white_pieces'], 'black': result['disabled_black_pieces']})

# url = '/message' + str(index)
@app.route('/message', methods=['POST'])
def process_msg():
    data = request.json  # Get JSON data sent by the client
    # Process data here...
    print(data)
    msg = 'My first move is ' + data['champion'] + '!'
    # index = index + 1
    return jsonify({'data': msg})

if __name__ == '__main__':
    app.run(debug=True)
    

