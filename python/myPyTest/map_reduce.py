# -*- coding: UTF-8 -*-

"""
map, reduce, filter都接收2个参数，一个函数，一个序列

"""


def f(x):
    return x * x


"""
map()

map()函数接收两个参数，一个是函数，一个是Iterable，map将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator返回。
map()的结果是一个迭代器iterator,
Iterator是惰性序列，因此通过list()函数让它把整个序列都计算出来并返回一个list
"""
res = map(f, [1, 2, 3, 4])  # map()的结果是一个迭代器iterator,
print(list(res))

# 以上代码等价于
L = []
for i in [1, 2, 3, 4]:
    L.append(i * i)
print(L)
"""

"""
res2 = map(str, [1, 2, 3, 4])
print(list(res2))

"""
reduce()
reduce把一个函数作用在一个序列[x1, x2, x3, ...]上，这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算，
其效果就是：

reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)

"""


def add(x, y):
    return x + y


from functools import reduce

res = reduce(add, [1, 2, 3, 4])  # 计算过程：1+2=3, 3+3=6, 6+4=10
print(res)  # 结果为10

"""
filter()
作用： filter()把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素
      filter()函数返回的是一个Iterator，也就是一个惰性序列，所以要强迫filter()完成计算结果，
      需要用list()函数获得所有结果并返回list。

"""


def is_odd(n):
    if n % 2 == 1:
        return True
    else:
        return False


res_list = filter(is_odd, [1, 2, 3, 4, 5, 6])   # 把返回值为false的给过滤调
print(list(res_list))       # [1, 3, 5]
