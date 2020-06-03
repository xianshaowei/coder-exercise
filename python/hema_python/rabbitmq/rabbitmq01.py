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

#reload(sys)
#sys.setdefaultencoding("utf-8")

# 定义日志输出

logfile = __file__ + '.log'
LOGFILE = os.path.expanduser(logfile)
LOG = logging.getLogger(__file__)
LOG.setLevel(logging.DEBUG)  # 控制台中输出DEBUG级别的日志
HANDLER1 = logging.StreamHandler(sys.stdout)
HANDLER2 = WatchedFileHandler(LOGFILE)  # WatchedFileHandler is a kind of filehandler
FMTER = logging.Formatter("%(asctime)s %(name)s [%(levelname)s]: %(message)s ", "%Y-%m-%d %H:%M:%S")
HANDLER1.setFormatter(FMTER)  # 日志输出格式
HANDLER2.setFormatter(FMTER)  # 日志输出格式
HANDLER1.setLevel(logging.DEBUG)
HANDLER2.setLevel(logging.INFO)
LOG.addHandler(HANDLER1)
LOG.addHandler(HANDLER2)


import pika

def log_test():
    LOG.info("test")
    LOG.error("test2")


class myclass():

    def __init__(self):
        pass


def main():
    # -*- coding: utf-8 -*-


    # 定义一个连接
    connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1',5672))
    channel = connection.channel()

    # 创建一个队列
    channel.queue_declare(queue='A')

    def callback(ch, method, properties, body):
        print(body)

    channel.basic_consume(callback, queue='A', no_ack=True)
    channel.start_consuming()



if __name__ == '__main__':
    main()
