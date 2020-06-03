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



from collections.abc import Iterable


mylist=[1,2,3,4]

print(isinstance(mylist, Iterable))

myiter=iter(mylist)


ret = next(myiter)  #1
print(ret)

ret = next(myiter)  #2
print(ret)

ret = next(myiter)  #3
print(ret)


# ret = next(myiter)  #raise,StopIteration
# print ret

print("end")
for i in mylist:
    print(i)


class Myiterator():

    def __iter__(self):
        pass

    def __next__(self):
        pass

myitr = Myiterator()

print(isinstance(myiter, Iterable))




