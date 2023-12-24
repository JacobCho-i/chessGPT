from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/data')
def get_data():
    return jsonify({'data': 'Someone ban malzhar!'})

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
    return jsonify({'data': 'Data received successfully!'})

if __name__ == '__main__':
    app.run(debug=True)