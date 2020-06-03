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
class Dog(object):

    def __init__(self, name):
        self.name = name

    def game(self):
        print("%s 蹦蹦跳跳的玩耍..." % self.name)


class XiaoTianDog(Dog):

    def game(self):
        print("%s 飞到天上去玩耍..." % self.name)


class Person(object):

    def __init__(self, name):
        self.name = name

    def game_with_dog(self, dog):

        print("%s 和 %s 快乐的玩耍..." % (self.name, dog.name))

        # 让狗玩耍
        dog.game()


def main():

    # 1. 创建一个狗对象
    wangcai = Dog("旺财")
    wangcai_fei = XiaoTianDog("飞天旺财")

    # 2. 创建一个小明对象
    xiaoming = Person("小明")

    # 3. 让小明调用和狗玩的方法
    xiaoming.game_with_dog(wangcai)
    # 输出： 小明 和 飞天旺财 快乐的玩耍...
    #       旺财 蹦蹦跳跳的玩耍...

    xiaoming.game_with_dog(wangcai_fei)
    # 输出：小明 和 飞天旺财 快乐的玩耍...
    #      飞天旺财 飞到天上去玩耍...

if __name__ == '__main__':
    main()
