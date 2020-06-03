# -*- coding: utf-8 -*-
"""
-------------------------------------------------
 
   Description :
   Author :        xianwei
   Tel :           138 8067 5749
   date：          2019-10-29
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


def log_test():
    LOG.info("test")
    LOG.error("test2")


class Student(object):

    def __init__(self, name, age, score_list):
        self.name = name
        self.age = age
        self.language_score = score_list[0]
        self.math_score = score_list[1]
        self.English_score = score_list[2]

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def get_score(self):
        return max([self.language_score, self.math_score, self.English_score])


class Student2(object):
    '''使用@property'''
    def __init__(self, name, age, score_list):
        self.name = name
        self.age = age
        self.language_score = score_list[0]
        self.math_score = score_list[1]
        self.English_score = score_list[2]

    @property
    def get_name(self):
        return self.name
    @property
    def get_age(self):
        return self.age
    @property
    def get_score(self):
        return max([self.language_score, self.math_score, self.English_score])



def main():
    log_test()

    # 普通方式
    s1 = Student('zhangming', 20, [69, 88, 100])
    print(s1.get_name())
    print(s1.get_age())
    print(s1.get_score())

    # property方式，像访问对象属性一样访问对象的方法
    s2 = Student2('zhangming', 20, [69, 88, 100])
    print(s2.get_name)
    print(s2.get_age)
    print(s2.get_score)

if __name__ == '__main__':
    main()
