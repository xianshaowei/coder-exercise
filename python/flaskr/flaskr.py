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
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

reload(sys)
sys.setdefaultencoding("utf-8")


app = Flask(__name__)
#app.config.from_envvar(‘FLASKR_SETTINGS’, silent=True)

def connect_db():
    '''connect to specific db'''
    rv = sqlite3.connect('DATABASE')
    rv.row_factory = sqlite3.Row
    return rv

# Flask 提供了两种环境（Context）：应用环境（Application Context）和 请求环境（Request Context）
# g 是与当前应用环境有关的通用变量
# request 变量与当前请求的请求对象有关
def get_db():

    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

#teardown_appcontext() 标记的函数会在每次应用环境 销毁时调用
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    # with app.app_context() 语句为我们建立了应用环境, g 对象会与 app 关联
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route("/", methods = ["GET"])
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = []
    for row in cur.fetchall():
        entries.append(dict(title=row[0], text=row[1]))
    return render_template('show_entries.html', entries=entries)


if __name__ == '__main__':
    init_db()
    app.run()
