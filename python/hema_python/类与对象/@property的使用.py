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
    print s.heigh
    print s.width
    print s.resolution


if __name__ == '__main__':
    main()
