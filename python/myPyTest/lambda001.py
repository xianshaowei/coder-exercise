# -*- cording: UTF-8 -*-

"""
lambda

关键字lambda表示匿名函数，冒号前面的x表示函数参数。

匿名函数有个限制，就是只能有一个表达式，不用写return，返回值就是该表达式的结果。

用匿名函数有个好处，因为函数没有名字，不必担心函数名冲突。

Python对匿名函数的支持有限，只有一些简单的情况下可以使用匿名函数。
"""


# 简单函数
def f(x):
    return x*x

print(f(2))

# 将简单函数转化为lambda函数
fun = lambda x: x*x
print(fun(3))
