from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/index')
def index():
    data = {
        "city" : 'cd',
        "age": '3000'
    }
    # json_str = json.dumps(data)
    # return json_str, "200", {"Content-Type:": "application/json"}

    return jsonify(data)

app.run(debug=True)