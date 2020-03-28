from flask import Flask, make_response

app=Flask(__name__)

@app.route('/index')
def index():
    # 1. 使用元组
    # 响应体   响应码     响应头
    #return "index test", "202", [("city","cd"), ("date", "20200301")]
    #return "index test", "202", {"city": "cd", "date": "20200301"}
    #return "index test", "202"
   # 2.
    rep = make_response("index test 2") # 实例化一个对象
    rep.status = "202"
    rep.headers["city"] = "cd"
    return rep
app.run(debug=True)