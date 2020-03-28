from flask import Flask, render_template

app = Flask(__name__)

@app.route('/index')
def index():
    data ={
        "city": "cd",
        "age": 18,
        "mydict":{"city": "cd"},
        "mylist": [1,2,3,4]
    }

    return render_template("index.html", **data)

app.run(debug=True)