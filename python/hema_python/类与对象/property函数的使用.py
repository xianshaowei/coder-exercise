# -*- coding: utf-8 -*-


class Screen(object):

    def __init__(self):
        self.__heigh = None

    # 定义属性heigh的获取，修改，与删除

    def get_heigh(self):
        return self.__heigh

    def set_heigh(self, value):
        self.__heigh = value

    heigh = property(get_heigh, set_heigh)  # 实现 对象名.属性名 = value来赋值

    # 定义属性width
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
    s.width = 1024  # 使用的是@property
    s.heigh = 768   # 使用的是property()函数, 通过property函数找到set_heigh()方法
    print s.heigh   # 使用的是property()函数, 通过property函数找到get_heigh()方法
    print s.width
    print s.resolution


if __name__ == '__main__':
    main()
