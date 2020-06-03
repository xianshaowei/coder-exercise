# -*- coding: utf-8 -*-
"""
-------------------------------------------------
 
   Description :    理解闭包的概念与原理
   Author :        xianwei
   Tel :           138 8067 5749
   date：          2019
-------------------------------------------------
   Change Activity:
                   2019
-------------------------------------------------

相关参数和变量都保存在返回的函数中，这种称为“闭包（Closure）”
"""


def outfunc(number):
    def infunc(number2):
        print("number is %d, number2 is %d" % (number, number2))
        print("number + number2 = %d" % (number + number2))

    return infunc


def main():
    ret = outfunc(100)  # ret是一个函数对象，指向infun()函数。变量100保存在返回的函数中
    print(ret)
    ret(10)             # number为outfunc()中的值
    ret(20)


if __name__ == '__main__':
    main()
