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

reload(sys)
sys.setdefaultencoding("utf-8")


class myclass(object):
    '''test class myclass'''
    __slots__ = ("name", "age")

    def __init__(self):
        pass

    # def __len__(self):
    #     return  3

    def fn(self):
        pass


def func():
    pass


class man(object):

    @property
    def birth(self):
        return self.__birth

    @birth.setter
    def birth(self, value):
        if value > 0 and value < 100:
            self.__birth = value
        else:
            raise ValueError("birth value error")

    @property
    def age(self):  # 只读属性
        self.__age = 10
        return self.__age


class Screen(object):

    def __init__(self):
        pass

    # 定义属性heigh的获取，修改，与删除
    @property
    def heigh(self):
        return self.__heigh

    @heigh.setter
    def heigh(self, value):
        self.__heigh = value

    @heigh.deleter
    def heigh(self):
        del self.__heigh

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        self.__width = value

    @width.deleter
    def width(self):
        del self.__width

    @property
    def resolution(self):
        return self.__heigh * self.__width


def main():
    s = Screen()
    # 修改
    s.width = 1024
    s.heigh = 768

    # 获取
    print(s.heigh)
    print(s.width)
    print(s.resolution)
    # 删除
    del s.heigh
    del s.width


    oneman = man()
    oneman.birth = 10
    print(oneman.birth)

    m2 = man()
    m2.birth = 11
    print(m2.birth)
    # print(oneman.age)

    # nums = [2,7,11,15]
    # target = 21
    # for i in range(len(nums)):
    #     j = i + 1
    #     for x in range(i+1,len(nums)):
    #         if nums[i] + nums[j] == target:
    #             print("i,j is %d,%d",i,j)
    #             sys.exit(0)
    # print("no result")

    m = myclass()
    m.name = "instance_name01"  # 动态的给对象绑定一个属性
    print m.name

    # m.score = 100  # 被限定了，不能动态绑定
    # print m.score

    print type(m)
    print type(func)

    import types

    print types.FunctionType

    print(isinstance(m, myclass))
    print(isinstance(1, int))

    print(dir(myclass))
    print(myclass.__doc__)


if __name__ == '__main__':
    main()
