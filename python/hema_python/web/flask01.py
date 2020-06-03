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

from flask import Flask
from flask import request, redirect, url_for

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    print("someone come in")
    # a = 1 / 0                      #用于测试读取配置文件
    return """
    <h1 style="font-family:verdana">home</h1>    

    <p style="background-color:green"> mystyle test.</p>
    <p style="font-family:verdana;color=red;font-size:40px;"> my font style test. </p>
    """


@app.route("/signin", methods=["GET"])
def sigin_form():
    return """
    <form action="signin" method="post">
    <p><input name="username"></p>
    <p><input name="password" type="password"></p>
    <p><button type="submit">Sign In</p>
    </form>
    """


@app.route("/signin", methods=["POST"])
def sigin():
    if request.form['username'] == 'admin' and request.form['password'] == 'admin':
        return "<p>hello,admin</p>"
    else:
        return "<h3>Bad username or password</h3>"


# 读取配置文件
app.config.from_pyfile("config.cfg")

# 重定向
from flask import redirect, url_for


@app.route("/registr", methods=["GET", "POST"])
def registr():
    url = url_for("sigin")
    return redirect(url)


# 动态url

# 默认只支持int, float, 字符串三种匹配
@app.route("/goods/<int:goods_id>")
def goods(goods_id):
    return "<>goods id is %s  </p>" % goods_id


# 其他类型匹配，需要自己定义规则
from werkzeug.routing import BaseConverter


class regex_converter(BaseConverter):

    def __init__(self, url_map):
        # 调用父类初始化方法
        super(regex_converter, self).__init__(url_map)
        # flask会使用这个属性来进行路由的正则匹配
        self.regex = r'1[34578]\d{9}'


app.url_map.converters["re"] = regex_converter


# /phone/13880039892
@app.route("/phone/<re:phone_num>")
def phone(phone_num):
    return "<>phone numbers is %s  </p>" % phone_num


def main():

    print(app.url_map)
    app.run()


if __name__ == '__main__':
    main()
