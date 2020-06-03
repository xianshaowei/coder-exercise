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


class MyList(object):

    def __init__(self):
        self.items = []
        self.index = 0

    # 对外提供迭代器功能
    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.items):
            v = self.items[self.index]
            self.index += 1
            return v
        else:
            # 停止迭代
            self.index = 0
            raise StopIteration

    def additems(self, item):
        self.items.append(item)

    def print_mylist(self):
        for i in self.items:
            print(i)


def main():
    from collections.abc import Iterable

    mylist = MyList()
    mylist.additems("zhangsan")
    mylist.additems("lishi")
    mylist.additems("wangwu")

    # mylist.print_mylist()

    print(isinstance(mylist, Iterable))

    my_itor = iter(mylist)
    print(my_itor)
    print(next(my_itor))
    print(next(my_itor))


    print("--------for 1")
    for i in mylist:
        print(i)

    print("--------for 2")
    for i in mylist:
        print(i)




if __name__ == '__main__':
    main()
