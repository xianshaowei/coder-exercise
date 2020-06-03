# -*- coding: utf-8 -*-

def gety(a, b, x):
    ''' 坐标系中，输入变量x的值，得到y的值'''
    y = a * x + b
    return y


def gety2(a, b):
    ''' 实现闭包实现'''

    def infunc(x):
        y = a * x + b
        return y

    return infunc


def main():
    print(gety(1, 1, 1))  # 2，需要同时设置a,b常量和变量x的值
    print(gety(2, 2, 1))  # 4

    line1 = gety2(1, 1)  # 设置a,b常量
    print(id(line1))  # line1对象指向，内部函数的一个实例4448098496
    print(line1(1))  # 坐标系中第一条直线，设置变量x的值

    line2 = gety2(2, 2)  # 4
    print(line2(2))     # 坐标系中第一条直线, 2*2 + 2
    print(id(line2) )
     # line2对象指向，内部函数的另一个实例4448098616

    print(line1(3))
      # 1*3 + 1
    print(id(line1))



if __name__ == '__main__':
    main()
