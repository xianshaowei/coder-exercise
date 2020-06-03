# -*- coding: utf-8 -*-

def get_key_from_value(dic, x):
    for i in dic.keys():
        print("key is %d" %i)
        if dic[i] == x:
            return i
    return None
class myclass():

    def __init__(self):
        pass

    def get_sum_of_two_numbers(self, numlist, target):
        ''' 暴力求解法 O(n^2)'''
        for i in range(len(numlist)):
            for j in range(len(numlist)):
                if numlist[j] == target - numlist[i] and i != j:
                    return (i, j)
        return None

    def get_sum_of_two_numbers_by_hash(self, numlist, target):
        '''hash表法， O(n)'''
        # 1. 把数放进hash表()
        numsdict = {}
        for i in range(len(numlist)):
            if numlist[i] not in numsdict:
                numsdict[numlist[i]] = 1

        # 2. 从hash表中查找
        for i in range(len(numsdict)):
            res = target - numlist[i]
            if res in numsdict.keys():
                index = numlist.index(res)
                return (i, index)

def main():


    nums = [11, 2, 7, 15]
    target = 9
    m = myclass()
    print(m.get_sum_of_two_numbers(nums, target))

    print(m.get_sum_of_two_numbers_by_hash(nums, target))





if __name__ == '__main__':
    main()
