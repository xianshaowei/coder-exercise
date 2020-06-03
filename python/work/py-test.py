#!/usr/bin/python
# -*- coding: UTF-8 -*-



from pyCommon.color import colorPrint
import os
import argparse

def filedealwith():
    '''
    vxlan_4038_0: 
    slave 
    vxlan_4038_1: 
    vxlan_4037_0: 
    vxlan_4037_1: 
    slave
    :return: 
    '''
    mylist = []
    fp = open("/Users/netease/Documents/git/git-201808-newbie-xianwei01/python/test.txt","r")
    for i in fp.readlines():
        mylist.append(i.strip("\n"))
    print mylist


    for i in range(len(mylist)-1):
        line1=mylist[i]
        line2=mylist[i+1]
        if "vxlan" in line1 and "slave" in line2:
            print line1,line2


    def synchost(self, gid):
        """sync host for cube"""

        import requests
        if not self.is_role(self.admin_role):
            ret = 13  # role error
            return ret

        url = self.cube_api + '/sync/hosts'
        filepath = "/home/data/site/serverlist/region.json"
        with open(filepath) as f:
            regions = json.load(f)

        region = regions.get(str(gid), None)
        if region is None:
            return 1

        headers = {
            'X-Auth-Token': self.get_auth_token(),
            'X-Auth-Project': self.project,
            'X-Auth-Region': region,
            'Content-Type': 'application/json'
        }

        body = '{}'
        res = requests.post(url, headers=headers, data=body)
        if not str(res.status_code).startswith('20'):
            self.error("%s: %s" % (res.status_code, res.text))
            return 1
        self.info("sync host success for region:%s" % region)
        return 0


def dns_test():
    import dns.resolver
    import requests
    #self.gid = str(51)
    gid = 1005
    host_list = []
    host_prefix_list = ["cld-vnode1-","cld-dnode1-","cld-cnode1-"]
    for host in host_prefix_list:
        host_list.append(host + str(gid))
    print host_list

    dns_error_count = 0
    for domain in host_list:
        try:
           AAA = dns.resolver.query(domain, 'A')
        except Exception:
           #print "dns resolver error:"
           dns_error_count += 1
           pass
        else:
           for i in AAA.response.answer:
               for j in i.items:
                   host = j.address
    if dns_error_count == 3:
        print "all host unable to resolver!"
        return 1

    print host

    cube_api = 'http://test-api.cube.nie.netease.com/api/v2/cube'
    url = cube_api + '/version'
    headers = {
        'X-Auth-Token': 'TLGm7hQ%2FsskZedI2tYMdE2L116m0UTFZZh40tj00k2D1%2Bks0XYXMYSWtVDeWmPknAR9YSlAc1I4l%0A3yuL6j7VOzQd4EslRZAykC%2Fd1vwG8g8vwb3tFok%2BR9%2FIDtplOU1loq4JBmitRHdJZtzBoT72zNKE%0AhZQZKd6Su2ILQoEOje0%3D%0A',
        'X-Auth-Project': 'cld',
        'X-Auth-Region': 'cld_hz_fcy',
        'Content-Type': 'application/json'
    }


    res = requests.get(url,headers=headers,)
    print res
    print res.text
    print res.status_code




class Foo():
    def __init__(self):
        print 'init'

    def __call__(self):
        print 'call'

    def __del__(self):
        print 'bye Foo'


def color_test():
    col = colorPrint()
    col.redPrint("hello")
    col.fuchsiaPrint("hello")
    col.yelloPrint("hello")
    col.bluePrint("hello")

    host = '192.168.168.168 '
    x = 888
    col.greenPrint(host,x)


def arg_deal_with():
    pass

def printip():
    col= colorPrint()
    col.greenPrint("192.168.1.1")

def printip_oneline():
    col= colorPrint()
    col.greenPrint("192.168.1.1 oneline")

def printfile():
    col= colorPrint()
    col.greenPrint("/etc/init.d/networing")

# def main():
#     # 实例化一个对象
#     par = argparse.ArgumentParser(description='Process some integers.')
#     # 指定参数
#     par.add_argument('--ip', '-i', type=str,  help="special a ip")
#     # 保存到namespace
#     par.add_argument('--oneline', '-o', default=False, help="special a output in oneline", action="store_true")
#     par.add_argument('--file', '-f', type=str, help="special a filename")
#
#     # 指定参数
#     par.add_argument('--command', '-c', type=str, help="special a command")
#     #par.set_defaults(function=sayhi)
#     args = par.parse_args()
#
#     #args.function()
#     print args
#
#
#     if args.ip and args.oneline:
#         printip_oneline()
#     if args.ip and argparse == False :
#         printip()
#
#     '''
#     #python py-test.py  -i 192.168.1.1  -o
#     Namespace(command=None, file=None, ip='192.168.1.1', oneline=True)
#     192.168.1.1 oneline
#
#     '''

#import Queue
import multiprocessing
from multiprocessing import Queue,Process

def inputque(num,q):
    q.put(num)
    print("input  %d to queue:q") %num


def outputque(q):
    while not q.empty():
        print q.get()
    print "empty"


class student(object):

    def get_score(self):
        return self.score

    def set_score(self,score):
        self.score = score


class student2(object):

    @property
    def score(self):
        return self.sc

    @score.setter
    def score(self, value):
        self.sc = value



if __name__ == "__main__":
    s = student()
    s.set_score(40)
    print s.get_score()

    s2 = student2()
    s2.score = 70
    print s2.score

    #color_test()
    # que = Queue()
    # inputque(11,que)
    # inputque(22,que)
    # outputque(que)
    # outputque(que)
    # outputque(que)
    #
    #
    # mque = Queue()
    # process_list = []
    # for i in xrange(5):
    #     p = Process(target=inputque,args=(i, mque,))
    #     p.start()
    #     p.join()
    #
    # pout = Process(target=outputque,args=(mque,))
    # pout.start()
    # pout.join()
    #
    #
    # # while not mque.empty():
    # #     print mque.get()