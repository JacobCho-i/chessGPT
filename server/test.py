from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
index = 1

@app.route('/api/data')
def get_data():
    return jsonify({'data': 'remove garen'})

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