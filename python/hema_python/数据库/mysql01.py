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
import logging
from logging.handlers import WatchedFileHandler

import mysql.connector
reload(sys)
sys.setdefaultencoding("utf-8")


def main():

    conn = mysql.connector.connect(user='root', password='fai', database='test', host='127.0.0.1')

    cursor = conn.cursor()

    #cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
    #cursor.execute('insert into user (id, name) values (%s, %s)', ['1', 'Michael'])
#    cursor.rowcount
#   conn.commit()


    cursor.execute('select * from user')
    value = cursor.fetchall()
    print(value)
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
