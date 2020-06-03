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

# reload(sys)
# sys.setdefaultencoding("utf-8")

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


def log_test():
    LOG.info("test")
    LOG.error("test2")


class myclass():

    def __init__(self):
        pass


import pika


def main():
    log_test()
    connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
    channel = connection.channel()

    # 创建一个exchange
    channel.exchange_declare(exchange='first', type='topic')

    # 创建两个queue
    channel.queue_declare(queue='A')
    channel.queue_declare(queue='B')

    # 将exchange与queue绑定
    # topic方式中，*表号匹配一个 word，#匹配多个 word 和路径，路径之间通过.隔开。
    channel.queue_bind(exchange='first', queue='A', routing_key='a.*.*')
    channel.queue_bind(exchange='first', queue='B', routing_key='a.#')

    # 向指定的 Exchange（交换器）发送一条消息
    channel.basic_publish(exchange='first', routing_key='a', body='hello world 01')  # 消息a只会被a.#匹配到
    channel.basic_publish(exchange='first', routing_key='a.b.c', body='hello world 02')  #a.b.c会被两个都匹配到


if __name__ == '__main__':
    main()
