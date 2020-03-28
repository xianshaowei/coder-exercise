
from flask import request, Flask, abort

app=Flask(__name__)

@app.route('/login', methods=['GET'])
def login():
    name=""
    pwd=""
    if name != "zhangsan" or pwd != 'pwd':
        abort(404)

    return 'login success'

@app.errorhandler(404)
def hander_404_err(err):
    return "error 404, %s" %err

app.run(debug=True)