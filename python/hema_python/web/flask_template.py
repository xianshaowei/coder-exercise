# -*- coding: utf-8 -*-
"""
-------------------------------------------------

   Description :
   Author :        xianwei
   Tel :           138 8067 5749
   date：          2019
-------------------------------------------------
   Change Activity:
                   2019
-------------------------------------------------
"""

import os, sys, re

reload(sys)
sys.setdefaultencoding("utf-8")


from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    print("someone come in")
    return render_template('home.html')


@app.route("/signin", methods=["GET"])
def sigin_form():
    return render_template('form.html')


@app.route("/signin", methods=["POST"])
def sigin():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'admin':
        return render_template('signin-ok.html', user=username)
    return render_template('form.html', message='Bad username or password', username=username)


def main():
    app.run()


if __name__ == '__main__':
    main()
