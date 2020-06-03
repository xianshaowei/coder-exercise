# -*- coding: utf-8 -*-


class Screen(object):

    name = "screen"
    def __init__(self):
        self.heigh = 5

# python是一种动态语言
def area(self):
    return self.heigh * self.width

@classmethod
def area2(cls):
    print("----area2----")
    print("name is %s" % cls.name)  # 类方法只能访问类变量

@staticmethod
def area3():
    print("----only can call by class----")


def main():
    s = Screen()
    # 修改

    print(s.heigh)
    Screen.width = 10   # 为类动态添加一个属性， 为公共属性
    print(s.width)

    s.lenght = 8        # 为对象动态添加一个属性
    print(s.lenght)

    #s.area = area() # 报错， area() missing 1 required positional argument: 'self'
    #s.area()

    import types

    s.area = types.MethodType(area, s)  # 将函数添加到对象s中，成为对象的一个方法. 把函数绑定到s对象的area属性
    print(s.area())
    print(type(area))   #<class 'function'>

    func = types.MethodType(area, s)  # 将函数添加到对象s中，成为对象的一个方法
    print(func())
    print(type(func))   #<class 'method'>

    Screen.area2 = area2    # 动态添加类方法
    s2 = Screen()
    s2.area2()

    Screen.area3 = area3    # 动态绑定静态方法
    s3 = Screen()
    s3.area3()

if __name__ == '__main__':
    main()
